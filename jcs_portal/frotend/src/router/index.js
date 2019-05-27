import Vue from 'vue'
import Router from 'vue-router'
import cloud from '../components/cloud/cloud.vue'
import map from '../components/data/map.vue'
import list from '../components/data/list.vue'
import login from '../components/user/login.vue'
import user from '../components/user/user.vue'
import register from '../components/user/register.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: '/user/login'
    },
    {
      path: '/user/login',
      component:login
    },
    {
      path: '/cloud',
      component: cloud
    },
    {
      path: '/data/map',
      component: map
    },
    {
      path: '/data/list',
      component: list
    },
    {
      path: '/user/user',
      component: user
    },
    {
      path: '/user/register',
      component: register
    }
  ]
})
