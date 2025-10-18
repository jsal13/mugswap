<template>
  <div class="profile-container">
    <div class="profile-card">
      <div class="card">
        <div class="card-content">
          <div class="profile-header">
            <div class="profile-avatar">
              {{ initials }}
            </div>
            <h2 class="profile-name">{{ authStore.user?.name }}</h2>
            <p class="profile-email">{{ authStore.user?.email }}</p>
          </div>
          
          <div class="profile-details">
            <div class="detail-section">
              <h3 class="section-title">Profile Information</h3>
              
              <div class="detail-row">
                <span class="detail-label">Age:</span>
                <span class="detail-value">{{ authStore.user?.age }} years old</span>
              </div>
              
              <div class="detail-row">
                <span class="detail-label">Bio:</span>
                <span class="detail-value">
                  {{ authStore.user?.bio || 'No bio added yet' }}
                </span>
              </div>
              
              <div class="detail-row">
                <span class="detail-label">Member since:</span>
                <span class="detail-value">Recently joined</span>
              </div>
            </div>
            
            <div class="detail-section">
              <h3 class="section-title">Mug Preferences</h3>
              
              <div class="preference-tags">
                <span class="preference-tag">Ceramic</span>
                <span class="preference-tag">Large Size</span>
                <span class="preference-tag">Classic Design</span>
                <span class="preference-tag">Handle Required</span>
              </div>
            </div>
            
            <div class="detail-section">
              <h3 class="section-title">Statistics</h3>
              
              <div class="stats-grid">
                <div class="stat-item">
                  <div class="stat-number">{{ mugStore.matches.length }}</div>
                  <div class="stat-label">Matches</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ totalSwipes }}</div>
                  <div class="stat-label">Total Swipes</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ likePercentage }}%</div>
                  <div class="stat-label">Like Rate</div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="profile-actions">
            <button @click="editProfile" class="edit-btn">
              ✏️ Edit Profile
            </button>
            <button @click="logout" class="logout-btn">
              🚪 Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useMugStore } from '../stores/mugs'

export default {
  name: 'Profile',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const mugStore = useMugStore()
    
    const initials = computed(() => {
      if (!authStore.user?.name) return '??'
      return authStore.user.name
        .split(' ')
        .map(word => word[0])
        .join('')
        .toUpperCase()
        .slice(0, 2)
    })
    
    const totalSwipes = computed(() => {
      // For demo purposes, calculate based on current mug index
      return mugStore.currentMugIndex || 0
    })
    
    const likePercentage = computed(() => {
      if (totalSwipes.value === 0) return 0
      return Math.round((mugStore.matches.length / totalSwipes.value) * 100)
    })
    
    onMounted(() => {
      mugStore.fetchMatches()
    })
    
    const editProfile = () => {
      alert('Edit profile functionality would be implemented here!')
    }
    
    const logout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    return {
      authStore,
      mugStore,
      initials,
      totalSwipes,
      likePercentage,
      editProfile,
      logout
    }
  }
}
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  padding: 2rem;
}

.profile-card {
  max-width: 600px;
  width: 100%;
}

.profile-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid var(--color-jade);
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-jade) 0%, var(--color-jade-dark) 100%);
  color: var(--color-white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 auto 1rem;
  border: 3px solid var(--color-jade-light);
}

.profile-name {
  font-size: 1.8rem;
  color: var(--color-black);
  margin-bottom: 0.5rem;
}

.profile-email {
  color: var(--color-gray-dark);
  font-size: 1rem;
}

.profile-details {
  margin-bottom: 2rem;
}

.detail-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.2rem;
  color: var(--color-black);
  margin-bottom: 1rem;
  font-weight: bold;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--color-gray-light);
}

.detail-label {
  font-weight: bold;
  color: var(--color-black);
}

.detail-value {
  color: var(--color-gray-dark);
  text-align: right;
  flex: 1;
  margin-left: 1rem;
}

.preference-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.preference-tag {
  background: linear-gradient(135deg, var(--color-jade) 0%, var(--color-jade-dark) 100%);
  color: var(--color-white);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  border: 1px solid var(--color-jade-light);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background: var(--color-off-white);
  border: 2px solid var(--color-jade);
  border-radius: 12px;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--color-jade);
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--color-gray-dark);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.profile-actions {
  display: flex;
  gap: 1rem;
}

.edit-btn, .logout-btn {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.3s;
}

.edit-btn {
  background: linear-gradient(135deg, var(--color-jade) 0%, var(--color-jade-dark) 100%);
  color: var(--color-white);
  border: 2px solid var(--color-jade);
}

.edit-btn:hover {
  background: linear-gradient(135deg, var(--color-jade-light) 0%, var(--color-jade) 100%);
  transform: translateY(-2px);
}

.logout-btn {
  background: var(--color-black);
  color: var(--color-white);
  border: 2px solid var(--color-gray);
}

.logout-btn:hover {
  background: var(--color-gray-dark);
  border-color: var(--color-white);
}

.edit-btn:hover, .logout-btn:hover {
  opacity: 0.9;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .profile-actions {
    flex-direction: column;
  }
  
  .detail-row {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .detail-value {
    margin-left: 0;
    margin-top: 0.25rem;
    text-align: left;
  }
}
</style>