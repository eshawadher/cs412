import React from 'react';
import { SymbolView } from 'expo-symbols';
import { Link, Tabs } from 'expo-router';
import { Platform, Pressable } from 'react-native';

import Colors from '@/constants/Colors';
import { useColorScheme } from '@/components/useColorScheme';
import { useClientOnlyValue } from '@/components/useClientOnlyValue';

//defines the bottom tab navigation for the app
export default function TabLayout() {
  const colorScheme = useColorScheme();

  return (
    // Tabs component creates the bottom navigation bar
    <Tabs
      screenOptions={{
        // Show the header bar
        tabBarActiveTintColor: Colors[colorScheme].tint,
        headerShown: useClientOnlyValue(false, true),
      }}>
        {/* home tab */}
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          // tabBarIcon: ({ color }) => (
          //   <SymbolView
          //     name={{
          //       ios: 'chevron.left.forwardslash.chevron.right',
          //       android: 'code',
          //       web: 'code',
          //     }}
          //     tintColor={color}
          //     size={28}
          //   />
          // ),
          // headerRight: () => (
          //   <Link href="/modal" asChild>
          //     <Pressable style={{ marginRight: 15 }}>
          //       {({ pressed }) => (
          //         <SymbolView
          //           name={{ ios: 'info.circle', android: 'info', web: 'info' }}
          //           size={25}
          //           tintColor={Colors[colorScheme].text}
          //           style={{ opacity: pressed ? 0.5 : 1 }}
          //         />
          //       )}
          //     </Pressable>
          //   </Link>
          // ),
        }}
      />
      {/* Destinations tab */}
      <Tabs.Screen
        name="detail"
        options={{
          title: 'Destinations',
          // tabBarIcon: ({ color }) => (
          //   <SymbolView
          //     name={{
          //       ios: 'chevron.left.forwardslash.chevron.right',
          //       android: 'code',
          //       web: 'code',
          //     }}
          //     tintColor={color}
          //     size={28}
          //   />
          // ),
        }}
      />
      {/* about tab  */}
      <Tabs.Screen
        name="about"
        options={{
          title: 'About',
        }}
      />
    </Tabs>
  );
}
