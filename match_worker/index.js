const Redis = require('ioredis');
const { createServer } = require("http");
const { Server } = require("socket.io");

const redis = new Redis({ host: process.env.REDIS_HOST || 'redis' });
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

redis.subscribe('ride_requests', (err, count) => {
  if (err) console.error('subscribe error', err);
  else console.log('subscribed to ride_requests');
});

redis.on('message', async (channel, message) => {
  if (channel === 'ride_requests') {
    try {
      const req = JSON.parse(message);
      const nearby = await redis.georadius('drivers:geo', req.pickup_lng, req.pickup_lat, 5, 'km', 'WITHDIST', 'COUNT', 10);
      for (const entry of nearby) {
        const driverId = entry[0];
        const driverSocketId = await redis.hget(`driver:${driverId}`, 'socketId');
        if (driverSocketId) {
          io.to(driverSocketId).emit('ride_offer', req);
        }
      }
    } catch (e) {
      console.error('error processing ride_requests', e);
    }
  }
});

httpServer.listen(3001, () => {
  console.log('Socket server listening on 3001');
});
