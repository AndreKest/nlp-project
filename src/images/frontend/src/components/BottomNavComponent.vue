<template>
  <v-bottom-navigation
    app
    fixed
    grow
    color="orange"
    dark
    background-color="#221934"
    style="z-Index: 9000"
  >
    <!-- Button Home -->
    <v-btn value="index" :to="{ path: '/'}">
      <span>Home</span>
      <v-icon>mdi-home</v-icon>
    </v-btn>

    <!-- Button Volltextsuche -->
    <v-btn value="searchText" :to="{ path: '/search-text'}">
      <span>Volltextsuche</span>
      <v-icon>mdi-text-search</v-icon>
    </v-btn>

    <!-- Button Feldersuche -->
    <v-btn value="searchFields" :to="{ path: '/search-fields'}">
      <span>Feldersuche</span>
      <v-icon>mdi-table-search</v-icon>
    </v-btn>

    <!-- Button Struktursuche -->
    <v-btn value="searchSentence" :to="{ path: '/search-sentence'}">
      <span>Struktursuche</span>
      <v-icon>mdi-database-search-outline</v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>

<script>
  export default {
    name: 'BottomNavComponent',
  }
</script>