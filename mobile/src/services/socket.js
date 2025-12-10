import { io } from 'socket.io-client';
const SOCKET_URL = 'http://10.0.2.2:3001';
export const socket = io(SOCKET_URL, { transports: ['websocket'] });
