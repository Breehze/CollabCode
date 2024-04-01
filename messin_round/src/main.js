import { createApp } from 'vue'
import { createRouter, createWebHistory } from "vue-router";
import App from './App.vue'

import Landing from './views/Landing.vue'
import CodeWfriends from './views/CodeWfriends.vue'
import "./css/output.css"


const router = createRouter({
    history : createWebHistory(),
    routes:[
        {path : '/', component : Landing },
        {path : '/collab', component : CodeWfriends },
    ]
})

createApp(App).use(router).mount('#app')
