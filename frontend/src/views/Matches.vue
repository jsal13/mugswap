<template>
  <div class="matches-container">
    <h2 class="page-title">Your Mug Matches ❤️</h2>
    
    <div v-if="mugStore.isLoading" class="loading">
      Loading matches...
    </div>
    
    <div v-else-if="mugStore.error" class="error-message">
      {{ mugStore.error }}
    </div>
    
    <div v-else-if="mugStore.matches.length === 0" class="no-matches">
      <div class="empty-state">
        <h3>No matches yet!</h3>
        <p>Start swiping to find your perfect mug matches.</p>
        <router-link to="/swipe" class="submit-btn">Start Swiping</router-link>
      </div>
    </div>
    
    <div v-else class="matches-grid">
      <div v-for="mug in mugStore.matches" :key="mug.id" class="match-card">
        <div class="card">
          <img 
            :src="mug.image_url" 
            :alt="mug.name"
            class="mug-image"
            @error="handleImageError"
          />
          
          <div class="card-content">
            <h3 class="card-title">{{ mug.name }}</h3>
            <p class="card-description">{{ mug.description }}</p>
            
            <div class="match-actions">
              <button class="contact-btn">
                💬 Send Message
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useMugStore } from '../stores/mugs'

export default {
  name: 'Matches',
  setup() {
    const mugStore = useMugStore()
    
    onMounted(() => {
      mugStore.fetchMatches()
    })
    
    const handleImageError = (event) => {
      event.target.src = 'https://via.placeholder.com/300x200/cccccc/666666?text=Mug+Image'
    }
    
    return {
      mugStore,
      handleImageError
    }
  }
}
</script>

<style scoped>
.matches-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.page-title {
  text-align: center;
  color: var(--color-jade-light);
  font-size: 2rem;
  margin-bottom: 2rem;
}

.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.match-card {
  transition: transform 0.3s ease;
}

.match-card:hover {
  transform: translateY(-5px);
}

.match-card .card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.match-card .mug-image {
  height: 200px;
  object-fit: cover;
}

.match-card .card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.match-card .card-title {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.match-card .card-description {
  font-size: 0.9rem;
  margin-bottom: 1rem;
  flex: 1;
}



.match-actions {
  margin-top: auto;
}

.contact-btn {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, var(--color-jade) 0%, var(--color-jade-dark) 100%);
  color: var(--color-white);
  border: 2px solid var(--color-jade);
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.contact-btn:hover {
  background: linear-gradient(135deg, var(--color-jade-light) 0%, var(--color-jade) 100%);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 166, 118, 0.3);
}

.empty-state {
  text-align: center;
  color: var(--color-white);
  padding: 3rem;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.empty-state p {
  margin-bottom: 2rem;
  opacity: 0.8;
}

.empty-state .submit-btn {
  display: inline-block;
  text-decoration: none;
}

@media (max-width: 768px) {
  .matches-container {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
  
  .matches-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>