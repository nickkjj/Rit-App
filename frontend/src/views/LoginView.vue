<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const router = useRouter()
const authStore = useAuthStore()

const users = ref([])
const selectedEmail = ref('')
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  try {
    const response = await api.get('/login-users/')
    users.value = response.data
    if (users.value.length > 0) {
      selectedEmail.value = users.value[0].email
    }
  } catch (err) {
    console.error(err)
    error.value = 'Falha ao carregar os usuários.'
  }
})

async function handleLogin() {
  if (!selectedEmail.value) return
  
  loading.value = true
  error.value = ''
  
  const success = await authStore.login(selectedEmail.value)
  if (success) {
    router.push({ name: 'dashboard' })
  } else {
    error.value = 'Erro ao realizar login.'
  }
  loading.value = false
}
</script>

<template>
  <div class="min-h-screen bg-bg flex items-center justify-center p-4">
    <div class="card p-8 w-full max-w-md">
      
      <div class="flex flex-col items-center mb-8">
        <div class="w-16 h-16 rounded-xl bg-gradient-to-br from-brand-300 to-mauve flex items-center justify-center text-white font-bold text-2xl mb-4">
          RIT
        </div>
        <p class="text-[13.5px] text-text2 text-center">Plataforma de monitoramento de desempenho de funcionários</p>
      </div>

      <div class="mb-4">
        <label class="block text-[13.5px] font-semibold text-textMain mb-2">Entrar como</label>
        <div class="relative">
          <select 
            v-model="selectedEmail"
            class="w-full border border-border rounded-custom py-2 px-3 pr-8 appearance-none bg-surface text-[14px] text-textMain focus:outline-none focus:border-brand-700"
            :disabled="users.length === 0"
          >
            <option v-for="user in users" :key="user.id" :value="user.email">
              {{ user.name }} ({{ user.position_name }})
            </option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-text2">
            <font-awesome-icon icon="chevron-down" class="w-4 h-4" />
          </div>
        </div>
      </div>

      <div v-if="error" class="mb-4 text-alert-fg bg-alert-bg p-3 rounded-lg text-sm">
        {{ error }}
      </div>

      <button 
        @click="handleLogin" 
        :disabled="loading || !selectedEmail"
        class="btn btn-primary w-full justify-center mt-2"
      >
        <span v-if="loading">Entrando...</span>
        <span v-else>Acessar</span>
      </button>

    </div>
  </div>
</template>
