// File: index.tsx
// Author: Esha Wadher eshaaw@bu.edu, 3/27/2026
// Description: Home screen for the travel app, displaying a title, 
// description text, and a travel image.

import { Text, View, Image } from 'react-native';
import { styles } from '../../assets/my_styles';
// IndexScreen is the main home screen of the travel app
export default function IndexScreen() {
  return (
    <View style={styles.container}>
        {/* Main title*/}
      <Text style={styles.titleText}>Explore the World</Text>

      {/* description encouraging the user to explore */}
      <Text style={styles.bodyText}>
        Travel is the only thing you buy that makes you richer. 
        Discover breathtaking destinations, hidden gems, and 
        unforgettable experiences from around the globe.
      </Text>
      <Image
        style={styles.mainImage}

        source={{ uri: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZpAwRRpPP1O3_H6vqsjtS6QhHsuGOhH4GOw&s' }}
      />
    </View>
  );
}