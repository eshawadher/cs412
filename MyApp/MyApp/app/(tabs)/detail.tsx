// File: detail.tsx
// Author: Esha Wadher (eshaaw@bu.edu), 3/27/2026
// Description: Destinations screen for the travel app, displaying
// a scrollable list of travel destinations with images and descriptions.

import { Text, Image, ScrollView } from 'react-native';
import { styles } from '../../assets/my_styles';

export default function DetailScreen() {
  return (
    // ScrollView allows the user to scroll through all destinations
    <ScrollView contentContainerStyle={styles.scrollContainer}>
      {/* title of the screen */}
      <Text style={styles.titleText}>Top Destinations</Text>
        {/* Paris destination*/}
      <Text style={styles.bodyText}>
        Paris, France — The City of Light dazzles visitors with the Eiffel Tower, 
        world-class cuisine, and timeless art at the Louvre.
      </Text>
      <Image
        style={styles.destinationImage}
        source={{ uri: 'https://choosewhere.com/public/images/fQpK5xb/945_630/shutterstock_710380270.webp' }}
      />
        {/* Japan destination*/}
      <Text style={styles.bodyText}>
        Kyoto, Japan — A city of ancient temples, cherry blossoms, 
        and traditional tea ceremonies that transport you back in time.
      </Text>
      <Image
        style={styles.destinationImage}
        source={{ uri: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-lqxsSZEStBsEWnF1zZZqUxv1rcIJ9TFlMw&s' }}
      />
        {/* Greece destination*/}
      <Text style={styles.bodyText}>
        Santorini, Greece — Famous for its stunning sunsets, white-washed 
        buildings, and crystal-clear blue waters of the Aegean Sea.
      </Text>
      <Image
        style={styles.destinationImage}
        source={{ uri: 'https://d2rdhxfof4qmbb.cloudfront.net/wp-content/uploads/2023/11/santorini-4825173_1280-1024x675.jpg' }}
      />
    </ScrollView>
  );
}
