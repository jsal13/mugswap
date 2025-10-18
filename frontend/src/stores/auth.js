import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        token: localStorage.getItem('token'),
        isLoading: false,
        error: null
    }),

    getters: {
        isAuthenticated: (state) => !!state.token && !!state.user
    },

    actions: {
        async login(email, password) {
            this.isLoading = true
            this.error = null

            try {
                const response = await axios.post(`${API_BASE_URL}/auth/login`, {
                    email,
                    password
                })

                const { access_token, user } = response.data
                this.token = access_token
                this.user = user

                localStorage.setItem('token', access_token)
                axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

                return true
            } catch (error) {
                this.error = error.response?.data?.detail || 'Login failed'
                return false
            } finally {
                this.isLoading = false
            }
        },

        async register(userData) {
            this.isLoading = true
            this.error = null

            try {
                const response = await axios.post(`${API_BASE_URL}/auth/register`, userData)

                const { access_token, user } = response.data
                this.token = access_token
                this.user = user

                localStorage.setItem('token', access_token)
                axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

                return true
            } catch (error) {
                this.error = error.response?.data?.detail || 'Registration failed'
                return false
            } finally {
                this.isLoading = false
            }
        },

        logout() {
            this.user = null
            this.token = null
            this.error = null

            localStorage.removeItem('token')
            delete axios.defaults.headers.common['Authorization']
        },

        async loadProfile() {
            if (!this.token) return

            try {
                axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
                const response = await axios.get(`${API_BASE_URL}/profile`)
                this.user = response.data
            } catch (error) {
                console.error('Failed to load profile:', error)
                this.logout()
            }
        }
    }
})