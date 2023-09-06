/* eslint-disable vue/no-mutating-props */
<template>
    <v-combobox
      v-model="searchData"
      :items="items"
      :search-input.sync="search"
      :label="label"

      hide-no-data
      hide-selected
    ></v-combobox>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'SearchInputField',

    props: {
      data: String,
      suggestField: String
    },

    data: () => ({
      isLoadingAutocomplete: false,
      entries: [],
      search: null,
    }),

    computed: {
      label: function() {
        return "Suchbegriff"
      },

      items () {
        return this.entries.map(entry => {
          return entry
        })
      },

      searchData: {
        get: function() {
          return this.data
        },
        set: function(value) {
          this.$emit('update:data', value)
        }
      }
    },

    watch: {
      /**
       * Wenn der Benutzer die Eingabe ändert,
       * wird eine neue Anfrage an das Backend geschickt,
       * um Autocompletion-Verschläge zu erhalten.
       */
      search (value) {
        if (value === undefined || !value) {
          return
        }

        this.searchData = value

        // Items wurden bereits angefordert
        if (this.isLoadingAutocomplete)
          return

        this.isLoadingAutocomplete = true
        axios.post('http://localhost:5000/predict', {
            text: value,
            fieldType: this.suggestField
          })
          .then(response => {
            this.entries = response.data
          })
          .catch(() => {
            this.entries = []
          })
          .finally(() => {
            this.isLoadingAutocomplete = false
          })
      },
    }
  }
</script>

<style>
  .v-autocomplete__content {
    z-index: 50 !important
  }
</style>