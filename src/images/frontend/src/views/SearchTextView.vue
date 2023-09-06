<template>
  <v-form>
    <v-container>
      <v-row>
        <v-col
          cols="12"
          class="pa-0"
        >
          <!-- Anzeige der Sucheingabe -->
          <SearchInputGroup 
            :fieldsData="this.$root.$data.store.queryData.title"
            suggestField="rawText"
            title="Suche nach Text"
            group="text"
          ></SearchInputGroup>
        </v-col>
      </v-row>

      <!-- Anzeige der Suchbox -->
      <SearchBox
        callApi="search/text"
        :apiParameter="this.readDataInitSearch"
        :callback="this.callback" 
        :resetPagination="this.resetPagination"
      />
    </v-container>

    <!-- Anzeige der Suchergebnisse -->
    <v-pagination 
      v-model="page" 
      :length="pages"
      total-visible="9"
      @input="changePage"
      v-if="pages > 1"
    >
    </v-pagination>
    <v-col>
      <v-card
        class="mx-auto mb-4"
        max-width="900"
        elevation=15
        shaped
        v-if="message != undefined && message.length == 0"
      >
        <v-card-text>
          Kein Ergebnis gefunden.
        </v-card-text>
      </v-card>
      <SearchResultItem 
        v-for="result in message" 
        :key="result.id" 
        :sentence="result.rawText"
        :sentenceFormatted="result.textFormatted" 
        :docId="result.docId" 
        :sentenceNumber="result.sentenceNumber"
        :id="result.id">
      </SearchResultItem>
    </v-col>
  </v-form>
</template>

<script>
  import SearchInputGroup from '../components/SearchInputGroup.vue'
  import SearchBox from '../components/SearchBox.vue'
  import SearchResultItem from '../components/SearchResultItem.vue'
  import axios from 'axios'

  export default {
    components: {
      SearchInputGroup,
      SearchBox,
      SearchResultItem
    },

    methods: {
      /**
       * Verarbeitet die Rückgabe der Suche.
       * 
       * @param {Object} result Suchergebnisse und Anzahl der gefunden Suchergebnisse
       */
      callback(result) {
        this.message = result.data.sentences
        this.pages = Math.ceil(result.data.numFound / 10)
      },
      /**
       * Nachladen der Suchergebnisse beim Auslösen der Pagination
       * 
       */
      changePage() {
        axios.post("http://localhost:5000/search/text", this.readData).then((res) => {
          this.callback(res)
        });
      },
      /**
       * Zurücksetzen der Pagination
       * 
       */
      resetPagination() {
        this.page = 1
      }
    },

    data: () => ({
      message: undefined,
      page: 1,
      pages: 0,
    }),

    computed: {
      /**
       * Initiales Auslesen der einzelnen Felder
       * 
       */
      readDataInitSearch() {
        return {
          text: this.$root.$data.store.queryData.title[1].data,
          currPage: 1
        }
      },
      /**
       * Auslesen der einzelnen Felder für die Pagination
       * 
       */
      readData() {
        return {
          text: this.$root.$data.store.queryData.title[1].data,
          currPage: this.page
        }
      }
    },
  }
</script>


