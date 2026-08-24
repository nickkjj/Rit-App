import { defineStore } from 'pinia'
import api from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.user,
    initials: (state) => {
      if (!state.user || !state.user.name) return ''
      const parts = state.user.name.split(' ')
      if (parts.length === 1) return parts[0][0].toUpperCase()
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
    }
  },
  
  actions: {
    async login(email) {
      try {
        const response = await api.post('/session/', { email })
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
        return true
      } catch (error) {
        console.error('Erro ao fazer login:', error)
        return false
      }
    },
    
    logout() {
      this.user = null
      localStorage.removeItem('user')
    }
  }
})
