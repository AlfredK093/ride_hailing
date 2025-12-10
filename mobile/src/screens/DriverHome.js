import React, { useEffect } from 'react';
import { View, Text } from 'react-native';
import { socket } from '../services/socket';

export default function DriverHome() {
  useEffect(() => {
    socket.on('connect', () => {
      console.log('socket connected', socket.id);
      socket.emit('register_driver', { driverId: 'driver1', lat: -15.78, lng: 35.00 });
    });

    socket.on('ride_offer', (req) => {
      alert('New ride offer: ' + JSON.stringify(req));
    });

    return () => {
      socket.off('connect');
      socket.off('ride_offer');
    };
  }, []);

  return (
    <View style={{ padding: 16 }}>
      <Text>Driver Home (demo)</Text>
    </View>
  );
}
