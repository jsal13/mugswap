<template>
  <div class="auth-container">
    <form @submit.prevent="handleRegister" class="auth-form">
      <h2 class="form-title">Join Mugswap</h2>
      
      <div v-if="authStore.error" class="error-message">
        {{ authStore.error }}
      </div>
      
      <div class="form-group">
        <label for="name" class="form-label">Full Name</label>
        <input
          id="name"
          v-model="name"
          type="text"
          class="form-input"
          required
        />
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
        <label for="age" class="form-label">Age</label>
        <input
          id="age"
          v-model.number="age"
          type="number"
          class="form-input"
          min="18"
          max="120"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="bio" class="form-label">Bio (Optional)</label>
        <textarea
          id="bio"
          v-model="bio"
          class="form-textarea"
          placeholder="Tell us about your coffee preferences..."
        ></textarea>
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
        {{ authStore.isLoading ? 'Creating Account...' : 'Sign Up' }}
      </button>
      
      <div class="auth-link">
        <p>Already have an account? <router-link to="/login">Log in</router-link></p>
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Register',
  setup() {
    const name = ref('')
    const email = ref('')
    const age = ref(25)
    const bio = ref('')
    const password = ref('')
    const router = useRouter()
    const authStore = useAuthStore()
    
    const handleRegister = async () => {
      const userData = {
        name: name.value,
        email: email.value,
        age: age.value,
        bio: bio.value,
        password: password.value
      }
      
      const success = await authStore.register(userData)
      if (success) {
        router.push('/swipe')
      }
    }
    
    return {
      name,
      email,
      age,
      bio,
      password,
      authStore,
      handleRegister
    }
  }
}
</script>