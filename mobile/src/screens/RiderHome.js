import React, { useState } from 'react';
import { View, Text, Button } from 'react-native';
import axios from '../services/api';

export default function RiderHome() {
  const [pickupLat] = useState(-15.78);
  const [pickupLng] = useState(35.00);
  const [dropLat] = useState(-15.80);
  const [dropLng] = useState(35.01);

  const requestRide = async () => {
    try {
      const res = await axios.post('/rides/request', {
        pickup_lat: parseFloat(pickupLat),
        pickup_lng: parseFloat(pickupLng),
        dropoff_lat: parseFloat(dropLat),
        dropoff_lng: parseFloat(dropLng)
      }, { params: { rider_id: 1 }});
      alert('Ride requested: ' + res.data.id);
    } catch (e) {
      alert('Error: ' + e.message);
    }
  };

  return (
    <View style={{ padding: 16 }}>
      <Text>Rider Home (demo)</Text>
      <Button title="Request Ride" onPress={requestRide} />
    </View>
  );
}
