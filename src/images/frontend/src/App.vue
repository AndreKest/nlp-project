<template>
  <v-app>
    <Header/>
    <v-main class="mx-2 mt-2">
      <!-- Übergangsanimation -->
      <transition name="fade" mode="out-in">
        <!-- Routing, das zwischen den verschiedenen Seiten schalten kann -->
        <router-view></router-view>
      </transition>
    </v-main>
    <BottomNav/>
  </v-app>
</template>

<script>
import Header from './components/HeaderComponent';
import BottomNav from './components/BottomNavComponent.vue';

export default {
  name: 'App',

  components: {
    Header,
    BottomNav
  },

  created () {
    document.title = "Studienarbeit NLP-Anwendungsentwicklung WiSe 2021";
  }
};
</script>