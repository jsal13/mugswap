<template>
  <div id="app">
    <header class="app-header">
      <nav class="navbar">
        <div class="nav-brand">
          <h1>☕ Mugswap</h1>
        </div>
        <div class="nav-links" v-if="isAuthenticated">
          <router-link to="/swipe" class="nav-link">Swipe</router-link>
          <router-link to="/matches" class="nav-link">Matches</router-link>
          <router-link to="/profile" class="nav-link">Profile</router-link>
          <button @click="logout" class="nav-link logout-btn">Logout</button>
        </div>
      </nav>
    </header>
    
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    const logout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    return {
      isAuthenticated,
      logout
    }
  }
}
</script>