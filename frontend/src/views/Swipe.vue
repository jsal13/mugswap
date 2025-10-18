<template>
  <div class="swipe-container">
    <div v-if="mugStore.isLoading" class="loading">
      Loading mugs...
    </div>
    
    <div v-else-if="mugStore.error" class="error-message">
      {{ mugStore.error }}
    </div>
    
    <div v-else-if="!mugStore.currentMug" class="no-mugs">
      <div class="card">
        <div class="card-content">
          <h2 class="card-title">No More Mugs!</h2>
          <p class="card-description">
            You've seen all available mugs. Check back later for more!
          </p>
          <button @click="resetAndRefresh" class="submit-btn">
            Refresh Mugs
          </button>
        </div>
      </div>
    </div>
    
    <div v-else class="mug-card">
      <div class="card">
        <img 
          :src="mugStore.currentMug.image_url" 
          :alt="mugStore.currentMug.name"
          class="mug-image"
          @error="handleImageError"
        />
        
        <div class="card-content">
          <h2 class="card-title">{{ mugStore.currentMug.name }}</h2>
          <p class="card-description">{{ mugStore.currentMug.description }}</p>
        </div>
        
        <div class="action-buttons">
          <button @click="handleSwipe(false)" class="action-btn pass-btn" title="Pass">
            ❌
          </button>
          <button @click="handleSwipe(true)" class="action-btn like-btn" title="Like">
            ❤️
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useMugStore } from '../stores/mugs'

export default {
  name: 'Swipe',
  setup() {
    const mugStore = useMugStore()
    
    onMounted(() => {
      if (mugStore.mugs.length === 0) {
        mugStore.fetchMugs()
      }
    })
    
    const handleSwipe = async (isLike) => {
      if (!mugStore.currentMug) return
      
      await mugStore.swipe(mugStore.currentMug.id, isLike)
      
      if (isLike) {
        // Show a brief animation or feedback for likes
        console.log('Liked!', mugStore.currentMug.name)
      }
    }
    
    const handleImageError = (event) => {
      // Fallback image when original fails to load
      event.target.src = 'https://via.placeholder.com/400x300/cccccc/666666?text=Mug+Image'
    }
    
    const resetAndRefresh = () => {
      mugStore.resetMugs()
      mugStore.fetchMugs()
    }
    
    return {
      mugStore,
      handleSwipe,
      handleImageError,
      resetAndRefresh
    }
  }
}
</script>

<style scoped>
.swipe-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.mug-card {
  perspective: 1000px;
}

.card {
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.no-mugs {
  max-width: 400px;
  width: 100%;
}

.action-buttons {
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>