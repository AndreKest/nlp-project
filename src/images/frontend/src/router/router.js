import Vue from "vue";
import Router from "vue-router";

import { publicRoutes } from "./config"

const routes = publicRoutes

// Router zu Vue hinzufügen
Vue.use(Router);

// Router erstellen
let router = new Router({
    mode: 'history',
    routes
})

export default router