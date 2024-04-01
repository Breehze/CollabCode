import { createRouter, createWebHistory } from 'vue-router';
import Landing from '../views/Landing.vue';
import CollabWfriends from '../views/CodeWfriends.vue';

const routes = [
  {
    path: '/',
    name: 'Land',
    component: Landing,
  },
  {
    path: '/collab',
    name: 'Collab',
    component: CollabWfriends,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;

