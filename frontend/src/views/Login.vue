<template>
  <div class="auth-container">
    <form @submit.prevent="handleLogin" class="auth-form">
      <h2 class="form-title">Welcome to Mugswap</h2>
      
      <div v-if="authStore.error" class="error-message">
        {{ authStore.error }}
      </div>
      
      <div class="form-group">
        <label for="email" class="form-label">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          class="form-input"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="password" class="form-label">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          class="form-input"
          required
        />
      </div>
      
      <button 
        type="submit" 
        class="submit-btn"
        :disabled="authStore.isLoading"
      >
        {{ authStore.isLoading ? 'Logging in...' : 'Login' }}
      </button>
      
      <div class="auth-link">
        <p>Don't have an account? <router-link to="/register">Sign up</router-link></p>
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Login',
  setup() {
    const email = ref('')
    const password = ref('')
    const router = useRouter()
    const authStore = useAuthStore()
    
    const handleLogin = async () => {
      const success = await authStore.login(email.value, password.value)
      if (success) {
        router.push('/swipe')
      }
    }
    
    return {
      email,
      password,
      authStore,
      handleLogin
    }
  }
}
</script>