<template>
  <v-card
    class="mx-auto mb-4 pa-0"
    elevation=15
    shaped
  >
    <!-- Titel -->
    <v-card-title class="lime darken-2">
      <v-icon left>mdi-cloud-search</v-icon>
      {{title}}
      <v-spacer/>
    </v-card-title>

    <!-- Anzeige der Suchanfragen -->
    <v-list-item class="lime accent-4 px-4 py-2"
      v-for="(field, key) in fieldsData"
      :key="key"
    >
      <v-row>
        <!-- Eingabefeld -->
        <v-col cols="12" md="12" sm="12" xs="12" class="d-flex">
          <SearchInputField v-bind:data.sync="field.data" :suggestField="suggestField" />     
        </v-col>
      </v-row>
    </v-list-item>
  </v-card>
</template>

<script>
  import SearchInputField from '../components/SearchInputField.vue'

  export default {
    name: 'SearchInputGroup',

    components: {
      SearchInputField,
    },

    props: {
      fieldsData: Object,
      title: String,
      group: String,
      suggestField: String,
    },

    methods: {
    },
  }
</script>