<template>
  <v-row justify='end'>
    <!-- Button Suchen -->
    <v-col class="text-right pr-0">
      <v-btn
        text
        @click="searchQuery"
        class="lime accent-4"
        color="black"
        height="60"
        width="200"
      >
        <v-icon left>mdi-cloud-search</v-icon>
        <v-spacer />
        Suchen
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
  import axios from 'axios'

  export default {
  components: { },
    name: 'SearchBox',

    methods: {
        /**
         * Schickt eine Suchabfrage an die API (Backend) ab
         * Mit dem Ergebnis werden Ergebnisse berechnet
         */
        searchQuery() {
          this.resetPagination()
          axios.post("http://localhost:5000/" + this.callApi, this.apiParameter).then((res) => {
            this.callback(res)
          });
        },
    },

    props: {
      callApi: String,
      apiParameter: Object,
      callback: { type: Function },
      resetPagination: { type: Function }
    },
  }
</script>