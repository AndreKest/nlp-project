<template>
  <v-form>
    <v-container fluid>
      <v-row class="fill-height" dense>
        <!-- Tile Volltextsuche -->
        <v-col>
          <v-card 
            class="mx-auto d-flex flex-column"
            color="#70762E"
            dark
            height="350"
          >
            <v-card-title>
              <v-icon
                large
                left
              >
                mdi-text-search
              </v-icon>
              <span class="text-h6 font-weight-light">Volltextsuche</span>
            </v-card-title>

            <v-card-text class="text-h5 font-weight-bold">
              Durchsucht die Datenbank nach Satzfragmenten.
            </v-card-text>
            
            <v-spacer></v-spacer>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                class="ml-2 mt-5"
                outlined
                rounded
                small
                href="/search-text"
              >
                ZUR SUCHE
                <v-icon>
                  mdi-magnify
                </v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <!-- Tile Feldersuche -->
        <v-col>
          <v-card 
            class="mx-auto d-flex flex-column"
            color="#3D2D06"
            dark
            height="350"
          >
            <v-card-title>
              <v-icon
                large
                left
              >
                mdi-table-search
              </v-icon>
              <span class="text-h6 font-weight-light">Feldersuche</span>
            </v-card-title>

            <v-card-text class="text-h5 font-weight-bold">
              Durchsucht die Datenbank nach Feldern (subj, verb, iobj, dobj, rest).
            </v-card-text>
            
            <v-spacer></v-spacer>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                class="ml-2 mt-5"
                outlined
                rounded
                small
                href="/search-fields"
              >
                ZUR SUCHE
                <v-icon>
                  mdi-magnify
                </v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <!-- Tile Struktursuche -->
        <v-col>
          <v-card 
            class="mx-auto d-flex flex-column"
            color="#98824E"
            dark
            height="350"
          >
            <v-card-title>
              <v-icon
                large
                left
              >
                mdi-database-search-outline
              </v-icon>
              <span class="text-h6 font-weight-light">Struktursuche</span>
            </v-card-title>

            <v-card-text class="text-h5 font-weight-bold">
              Durchsucht die Datenbank nach der Struktur des gesuchten Satzes.
            </v-card-text>
            
            <v-spacer></v-spacer>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                class="ml-2 mt-5"
                outlined
                rounded
                small
                href="/search-sentence"
              >
                ZUR SUCHE
                <v-icon>
                  mdi-magnify
                </v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
  export default {
  }
</script>