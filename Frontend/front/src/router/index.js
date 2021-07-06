/* eslint-disable indent */
import Vue from 'vue'
import Router from 'vue-router'
import home from '../view/home'
// import unknown from '@/view/unknown'

Vue.use(Router)

export default new Router({
    // mode: history,
    routes: [
        {
            path: '/',
            redirect: '/home',
        },
        {
            path: '/home',
            name: 'home',
            component: home
        },
    ]
})
