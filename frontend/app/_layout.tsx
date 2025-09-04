import React from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

// LCA TV Theme colors
const colors = {
  primary: '#2d5016',
  primaryLight: '#22c55e',
  white: '#ffffff',
};

export default function RootLayout() {
  return (
    <>
      <StatusBar style="light" backgroundColor={colors.primary} />
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: colors.white },
        }}
      >
        <Stack.Screen name="index" />
        <Stack.Screen name="login" />
        <Stack.Screen name="register" />
        <Stack.Screen name="live" />
        <Stack.Screen name="replay" />
        <Stack.Screen name="news" />
        <Stack.Screen name="publicity" />
        <Stack.Screen name="profile" />
        <Stack.Screen name="favorites" />
        <Stack.Screen name="video/[id]" />
        <Stack.Screen name="category/[category]" />
      </Stack>
    </>
  );
}