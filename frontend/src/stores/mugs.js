import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

export const useMugStore = defineStore('mugs', {
    state: () => ({
        mugs: [],
        currentMugIndex: 0,
        matches: [],
        isLoading: false,
        error: null
    }),

    getters: {
        currentMug: (state) => state.mugs[state.currentMugIndex] || null,
        hasMoreMugs: (state) => state.currentMugIndex < state.mugs.length
    },

    actions: {
        async fetchMugs() {
            this.isLoading = true
            this.error = null

            try {
                const response = await axios.get(`${API_BASE_URL}/mugs`)
                this.mugs = response.data
                this.currentMugIndex = 0
            } catch (error) {
                this.error = error.response?.data?.detail || 'Failed to fetch mugs'
            } finally {
                this.isLoading = false
            }
        },

        async swipe(mugId, isLike) {
            try {
                await axios.post(`${API_BASE_URL}/swipe`, {
                    mug_id: mugId,
                    is_like: isLike
                })

                this.currentMugIndex++

                if (isLike) {
                    // Add to matches for demo purposes
                    const mug = this.mugs.find(m => m.id === mugId)
                    if (mug && !this.matches.find(m => m.id === mugId)) {
                        this.matches.push(mug)
                    }
                }

                return true
            } catch (error) {
                this.error = error.response?.data?.detail || 'Swipe failed'
                return false
            }
        },

        async fetchMatches() {
            this.isLoading = true
            this.error = null

            try {
                const response = await axios.get(`${API_BASE_URL}/matches`)
                this.matches = response.data
            } catch (error) {
                this.error = error.response?.data?.detail || 'Failed to fetch matches'
            } finally {
                this.isLoading = false
            }
        },

        resetMugs() {
            this.currentMugIndex = 0
        }
    }
})