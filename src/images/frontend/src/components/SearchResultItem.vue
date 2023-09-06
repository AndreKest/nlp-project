<template>
  <v-card
    class="mx-auto mb-4"
    max-width="900"
    elevation=15
    shaped
  >
    <v-card-text>
      <v-row>
         <v-col cols=2>
           Dokument:<br>
           {{id}}
        </v-col>
        <v-col cols=9 v-html="sentenceFormatted">
          
        </v-col>
        <v-col>
          <v-row>
            <v-col>
              <v-btn fab x-small v-on:click="parse">
                <v-icon>
                  mdi-graph-outline
                </v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn fab x-small v-on:click="viewDoc">
                <v-icon>
                  mdi-text-box-search-outline
                </v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'SearchResultItem',

    props: {
      sentence: String,
      sentenceFormatted: String,
      docId: String,
      id: String,
      sentenceNumber: String
    },

    methods: {
      /**
       * Sendet einen Satz an das Backend und öffnet ein neues Fenster mit 
       * dem gerenderten Dependenzbaum.
       * 
       */
      parse: function(){
        axios.get('http://localhost:5000/parse?text=' + this.sentence)
          .then(function (response){
            var wnd = window.open("about:blank", "Dependenzbaum", "_blank");
            wnd.document.write(response.data);
          })
          .catch(function (error){
            console.log(error)
          })
      },
      /**
       * Sendet eine Dokument-ID an das Backend und öffnet ein neues Fenster mit
       * dem Dokument.
       * 
       */
      viewDoc: function(){
        axios.get('http://localhost:5000/viewDoc?docId=' + this.docId)
          .then(response => {
            var wnd = window.open("about:blank", "Dependenzbaum", "_blank");
            wnd.document.write(`<h2>Dokument: ${this.docId}</h2>`)

            response.data.forEach(sentence => {
              if(/^\d/.test(sentence.rawText)){
                wnd.document.write("<br>");
              } 
              if(sentence.sentenceNumber == this.sentenceNumber){
                wnd.document.write("<span style=\"background-color: yellow\">");
                wnd.document.write(sentence.rawText);
                wnd.document.write("</span>");
              }
              else{
                wnd.document.write(sentence.rawText);
              }

              if(/(^\S*$)/.test(sentence.rawText)){
                wnd.document.write("<br>");
              } 

              wnd.document.write("<br>");
            });
          })
          .catch(function (error){
            console.log(error)
          })
      }
    },

    data: () => ({
      isLoading: false,
    }),
  }
</script>

<style>
  hlquery {
    background:rgb(202, 34, 118) !important
  }
</style>