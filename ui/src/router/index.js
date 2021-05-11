import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Endpoint from '../views/Endpoint.vue'
import NotFound from '../views/NotFound.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/notfound/',
    name: 'NotFound',
    component: NotFound
  },
  {
    path: '/:Endpoint/',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: Endpoint
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
