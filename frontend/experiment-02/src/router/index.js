

import { createRouter, createWebHistory } from 'vue-router';
import PersonalInformationView from '../views/PersonalInformationView.vue';
import WelcomePageView from '../views/WelcomePageView.vue';
import ExperimentViewUno from '../views/ExperimentViewUno.vue';
import EndView from '../views/EndView.vue';
import EndPoll from "../views/EndPoll.vue";

const routes = [
  { path: '/', name: 'welcome', component: WelcomePageView },
  { path: '/personal-info', component: PersonalInformationView },
  { path: '/experiment/:participantData', name: 'ExperimentUno', component: ExperimentViewUno },
  {path: '/end-poll/:participantData', name: 'EndPoll', component: EndPoll},
  { path: '/end-view', component: EndView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
