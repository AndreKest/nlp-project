<template>
  <v-app-bar
    app
    color="#221934"
    background-color="#221934"
    dark
    outlined
    style="z-Index: 90000"
  >
    <!-- Icon -->
    <div class="d-flex align-center">
      <v-img
        alt="Logo"
        min-width="32"
        src="favicon.ico"
        width="32"
      />
    </div>
    <v-spacer></v-spacer>

    <h4 class="ml-2 mr-2 font-weight-thin">Studienarbeit NLP</h4>
  </v-app-bar>
</template>

<script>
  export default {
    name: 'HeaderComponent',
  }
</script>
