import IndexView from '../views/IndexView.vue'
import SearchFieldsView from '../views/SearchFieldsView.vue'
import SearchSentenceView from '../views/SearchSentenceView.vue'
import SearchTextView from '../views/SearchTextView.vue'

// Routen, die verwendet werden
export const publicRoutes = [
    {
        path: "/",
        name: 'index',
        component: IndexView
    },
    {
        path: "/search-fields",
        name: 'searchFields',
        component: SearchFieldsView
    },
    {
        path: "/search-sentence",
        name: 'searchSentence',
        component: SearchSentenceView
    },
    {
        path: "/search-text",
        name: 'searchText',
        component: SearchTextView
    },
]