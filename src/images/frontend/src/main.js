import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router/router'

// Icons
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.config.productionTip = false

// Zentraler Speicher für die Anwendung
// auf der Client-Seite (Frontend) - SPA
// https://vuejs.org/v2/guide/state-management.html
var store = {
  queryResults: [],
  queryData: {
    title: { 
      1: {
        data: "",
        group: "title",
      }, 
    },
    root: { 
      1: {
        data: "",
        group: "root",
      }, 
    },
    nsubj: { 
      1: {
        data: "",
        group: "nsubj",
      }, 
    },
    da: { 
      1: {
        data: "",
        group: "da",
      }, 
    },
    oa: { 
      1: {
        data: "",
        group: "oa",
      }, 
    },
    rest: { 
      1: {
        data: "",
        group: "rest",
      }, 
    },
  }
}

new Vue({
  router,
  vuetify,
  data: {
    store
  },
  render: h => h(App)
}).$mount('#app')