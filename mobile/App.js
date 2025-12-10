import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import RiderHome from './src/screens/RiderHome';
import DriverHome from './src/screens/DriverHome';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="RiderHome">
        <Stack.Screen name="RiderHome" component={RiderHome} />
        <Stack.Screen name="DriverHome" component={DriverHome} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
