import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Endereço da API backend
  headers: {
    'Content-Type': 'application/json',
  }
})

// Adiciona o cabeçalho X-User-Email se o usuário estiver logado
api.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.user && authStore.user.email) {
    config.headers['X-User-Email'] = authStore.user.email
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

export default api
