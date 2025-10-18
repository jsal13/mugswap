import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './stores/auth'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Swipe from './views/Swipe.vue'
import Matches from './views/Matches.vue'
import Profile from './views/Profile.vue'

const routes = [
    {
        path: '/',
        redirect: '/swipe'
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { requiresGuest: true }
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
        meta: { requiresGuest: true }
    },
    {
        path: '/swipe',
        name: 'Swipe',
        component: Swipe,
        meta: { requiresAuth: true }
    },
    {
        path: '/matches',
        name: 'Matches',
        component: Matches,
        meta: { requiresAuth: true }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile,
        meta: { requiresAuth: true }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()

    // Load profile if token exists but user is not loaded
    if (authStore.token && !authStore.user) {
        authStore.loadProfile()
    }

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login')
    } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
        next('/swipe')
    } else {
        next()
    }
})

export default router