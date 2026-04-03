// File: my_styles.ts
// Author: Esha Wadher (eshaaw@bu.edu), 3/27/2026
// Description: Stylesheet for the travel app, defining reusable
// styles for all three screens.

import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#fff',
  },
  titleText: {
    fontSize: 28,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 10,
    textAlign: 'center',
    color: '#2c3e50',
  },
  bodyText: {
    fontSize: 16,
    textAlign: 'center',
    color: '#555',
    marginBottom: 20,
    lineHeight: 24,
  },
  mainImage: {
    width: 320,
    height: 220,
    borderRadius: 12,
  },
  scrollContainer: {
    padding: 20,
  },
  destinationImage: {
    width: '100%',
    height: 200,
    borderRadius: 10,
    marginVertical: 10,
  },
});