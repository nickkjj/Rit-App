import { defineStore } from 'pinia'
import api from '@/api'

export const useTeamStore = defineStore('team', {
  state: () => ({
    members: [],
    loading: false,
    error: null,
    historyLabels: [],
    historyData: []
  }),
  
  getters: {
    pendingEvaluations: (state) => {
      return state.members.filter(m => m.evaluation_status === 'Pendente')
    },
    completedEvaluations: (state) => {
      return state.members.filter(m => m.evaluation_status !== 'Pendente')
    },
    directPendingCount: (state) => {
      return state.members.filter(m => m.evaluation_status === 'Pendente' && m.relation === 'direto').length
    },
    indirectPendingCount: (state) => {
      return state.members.filter(m => m.evaluation_status === 'Pendente' && m.relation === 'indireto').length
    }
  },
  
  actions: {
    async fetchTeam() {
      this.loading = true
      this.error = null
      try {
        const response = await api.get('/team/dashboard/')
        this.members = response.data
      } catch (err) {
        console.error('Erro ao buscar o time', err)
        this.error = 'Não foi possível carregar a lista de funcionários.'
      } finally {
        this.loading = false
      }
    },
    
    async fetchTeamHistory() {
      try {
        const response = await api.get('/team/history/')
        this.historyLabels = response.data.labels || []
        this.historyData = response.data.data || []
      } catch (err) {
        console.error('Erro ao buscar histórico do time', err)
      }
    }
  }
})
