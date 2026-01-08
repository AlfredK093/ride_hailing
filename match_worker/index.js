const Redis = require('ioredis');
const { createServer } = require("http");
const { Server } = require("socket.io");

const redis = new Redis({ host: process.env.REDIS_HOST || 'redis' });
// separate client for subscriptions (subscriber mode) to avoid "subscriber mode" errors
const sub = new Redis({ host: process.env.REDIS_HOST || 'redis' });
const httpServer = createServer();

const io = new Server(httpServer, {
  cors: { origin: "*" }
});

io.on('connection', (socket) => {
  console.log('client connected', socket.id);

  socket.on('register_driver', async ({ driverId, lat, lng }) => {
    console.log('register_driver', driverId, lat, lng);
    socket.join(`driver:${driverId}`);
    // store driver location in redis GEO (lon, lat)
    await redis.geoadd('drivers:geo', lng, lat, driverId);
    await redis.hset(`driver:${driverId}`, 'socketId', socket.id);
  });

  socket.on('disconnect', async () => {
    console.log('disconnect', socket.id);
  });
});

sub.subscribe('ride_requests', (err, count) => {
  if (err) {
    console.error('subscribe error', err && err.stack ? err.stack : err);
  } else {
    console.log('subscribed to ride_requests');
  }
});

sub.on('message', async (channel, message) => {
  if (channel !== 'ride_requests') return;

  let req;
  try {
    req = JSON.parse(message);
  } catch (e) {
    console.error('ride_requests: invalid JSON message', e && e.stack ? e.stack : e, message);
    return;
  }

  if (!req || typeof req.pickup_lng !== 'number' || typeof req.pickup_lat !== 'number') {
    console.error('ride_requests: missing or invalid pickup coordinates', req);
    return;
  }

  try {
  const nearby = await redis.georadius('drivers:geo', req.pickup_lng, req.pickup_lat, 5, 'km', 'WITHDIST', 'COUNT', 10);
    if (!Array.isArray(nearby) || nearby.length === 0) {
      // no drivers nearby
      return;
    }

    for (const entry of nearby) {
      const driverId = entry[0];
      try {
        const driverSocketId = await redis.hget(`driver:${driverId}`, 'socketId');
        if (!driverSocketId) {
          console.log('no socketId for driver', driverId);
          continue;
        }

        // check if socket is currently connected to this server
        const socketObj = io.sockets.sockets.get(driverSocketId);
        if (!socketObj) {
          console.log('stale socketId for driver, cleaning up', driverId, driverSocketId);
          // remove stale socketId from redis
          await redis.hdel(`driver:${driverId}`, 'socketId');
          continue;
        }

        console.log('notifying driver', driverId, 'socketId=', driverSocketId);
        try {
          socketObj.emit('ride_offer', req);
        } catch (emitErr) {
          console.error('failed to emit to socket', driverId, driverSocketId, emitErr && emitErr.stack ? emitErr.stack : emitErr);
        }
      } catch (innerErr) {
        console.error('ride_requests: error notifying driver', driverId, innerErr && innerErr.stack ? innerErr.stack : innerErr);
      }
    }
  } catch (e) {
    console.error('error processing ride_requests', e && e.stack ? e.stack : e);
  }
});

httpServer.listen(3001, () => {
  console.log('Socket server listening on 3001');
});
