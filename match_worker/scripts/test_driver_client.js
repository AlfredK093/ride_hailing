const { io } = require('socket.io-client');

const SERVER = process.env.SOCKET_SERVER || 'http://socket:3001';
const DRIVER_ID = process.env.DRIVER_ID || 'driver123';
const LAT = parseFloat(process.env.LAT || '-1.2921');
const LNG = parseFloat(process.env.LNG || '36.8219');

console.log('Connecting to', SERVER);

const socket = io(SERVER, { transports: ['websocket'], reconnection: false });

socket.on('connect', () => {
  console.log('connected as', socket.id);
  socket.emit('register_driver', { driverId: DRIVER_ID, lat: LAT, lng: LNG });
});

socket.on('ride_offer', (req) => {
  console.log('received ride_offer', req);
});

socket.on('disconnect', (reason) => {
  console.log('disconnected', reason);
});

socket.on('connect_error', (err) => {
  console.error('connect_error', err && err.message ? err.message : err);
  process.exit(1);
});
