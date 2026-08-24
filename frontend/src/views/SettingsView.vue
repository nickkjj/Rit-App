<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const isAuthorized = computed(() => {
  const allowedPositions = ['CEO', 'CTO', 'CFO']
  return allowedPositions.includes(authStore.user?.position_name)
})

const loading = ref(true)
const submitting = ref(false)
const error = ref('')
const successMessage = ref('')

const questions = ref([])

onMounted(async () => {
  if (isAuthorized.value) {
    await fetchCurrentQuestions()
  } else {
    loading.value = false
  }
})

async function fetchCurrentQuestions() {
  loading.value = true
  error.value = ''
  try {
    const res = await api.get('/questions/versions/current/')
    // Clonamos as questões para permitir edição no draft
    questions.value = (res.data.questions || []).map(q => ({
      title: q.title,
      weight: q.weight,
      id: q.id || Math.random().toString(36).substr(2, 9)
    }))
    
    // Se vier vazio, adicione uma default
    if (questions.value.length === 0) {
      addQuestion()
    }
  } catch (err) {
    if (err.response && err.response.status === 404) {
      // Nenhuma versão ativa
      addQuestion()
    } else {
      console.error(err)
      error.value = 'Erro ao buscar questões atuais.'
    }
  } finally {
    loading.value = false
  }
}

const totalWeight = computed(() => {
  return questions.value.reduce((acc, q) => acc + (Number(q.weight) || 0), 0)
})

const isTotalValid = computed(() => totalWeight.value === 100)
const hasEmptyTitles = computed(() => questions.value.some(q => !q.title.trim()))

function addQuestion() {
  questions.value.push({
    title: '',
    weight: 0,
    id: Math.random().toString(36).substr(2, 9)
  })
}

function removeQuestion(index) {
  questions.value.splice(index, 1)
}

async function saveSettings() {
  if (!isTotalValid.value) {
    error.value = 'A soma dos pesos deve ser exatamente 100.'
    return
  }
  if (hasEmptyTitles.value) {
    error.value = 'Todas as questões devem ter um título.'
    return
  }
  
  submitting.value = true
  error.value = ''
  successMessage.value = ''
  
  const payload = {
    questions: questions.value.map(q => ({
      title: q.title.trim(),
      weight: Number(q.weight)
    }))
  }
  
  try {
    await api.post('/questions/versions/', payload)
    successMessage.value = 'Nova versão de questões salva com sucesso! O formulário de avaliações foi atualizado.'
    await fetchCurrentQuestions()
  } catch (err) {
    console.error(err)
    error.value = 'Erro ao salvar as configurações. Verifique os dados e tente novamente.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="max-w-[800px] mx-auto w-full">
    
    <div v-if="!isAuthorized" class="card overflow-hidden text-center py-12 px-6">
      <div class="w-16 h-16 bg-alert-bg rounded-full flex items-center justify-center mx-auto mb-4 text-alert-fg">
        <font-awesome-icon icon="lock" class="w-8 h-8" />
      </div>
      <h2 class="text-[18px] font-bold text-textMain mb-2">Acesso Restrito</h2>
      <p class="text-[14px] text-text2 max-w-md mx-auto">Apenas pessoas com cargo de diretoria (CEO, CTO ou CFO) podem visualizar esta página e alterar as métricas globais.</p>
    </div>

    <div v-else class="card overflow-hidden">
      <div class="p-[24px] border-b border-border">
        <div class="flex items-center gap-3 mb-1">
          <h2 class="text-[16px] font-bold m-0 text-textMain">Configurações de Avaliação</h2>
          <span class="bg-brand-50 text-brand-700 text-[11px] font-semibold px-2 py-0.5 rounded-full border border-brand-200">Apenas para CEO, CTO e CFO</span>
        </div>
        <p class="text-[13px] text-text2 mt-1">Gerencie as questões utilizadas nos relatórios de desempenho e seus respectivos pesos na nota final.</p>
      </div>
      
      <div class="p-[24px]">
        <div v-if="loading" class="text-center text-text2 py-8">Carregando configurações...</div>
        
        <div v-else>
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-bold text-[14px] text-textMain">Questões Ativas</h3>
            <div class="text-[13px] font-semibold" :class="isTotalValid ? 'text-done-fg' : 'text-alert-fg'">
              Soma dos Pesos: {{ totalWeight }}%
              <span v-if="!isTotalValid" class="block text-[11px] font-normal mt-[2px]">A soma precisa ser exata de 100%</span>
            </div>
          </div>
          
          <div class="space-y-3 mb-6">
            <div v-for="(q, index) in questions" :key="q.id" class="flex items-start gap-3">
              <div class="w-8 h-10 flex items-center justify-center font-bold text-text3 shrink-0">{{ index + 1 }}.</div>
              <div class="flex-1">
                <input 
                  type="text" 
                  v-model="q.title" 
                  placeholder="Descreva a pergunta (ex: Qual o nível de proatividade?)"
                  class="w-full border border-border rounded-custom px-3 py-2 text-[14px] text-textMain focus:outline-none focus:border-brand-700"
                />
              </div>
              <div class="w-[100px] shrink-0 relative">
                <input 
                  type="number" 
                  v-model="q.weight" 
                  min="0" max="100"
                  class="w-full border border-border rounded-custom pl-3 pr-8 py-2 text-[14px] text-textMain focus:outline-none focus:border-brand-700"
                />
                <div class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-text2 text-[14px]">%</div>
              </div>
              <button 
                @click="removeQuestion(index)" 
                class="w-10 h-10 flex items-center justify-center text-text3 hover:text-alert-fg border border-transparent hover:border-alert-bg hover:bg-alert-bg rounded-lg transition-colors shrink-0 disabled:opacity-50"
                :disabled="questions.length <= 1"
              >
                <font-awesome-icon icon="trash" class="w-4 h-4" />
              </button>
            </div>
          </div>
          
          <button type="button" @click="addQuestion" class="flex items-center gap-1 text-[13.5px] font-medium text-brand-700 hover:text-brand-800">
            <font-awesome-icon icon="plus" class="w-4 h-4" />
            Adicionar nova questão
          </button>
          
          <div v-if="error" class="mb-4 text-alert-fg bg-alert-bg p-3 rounded-lg text-sm">
            {{ error }}
          </div>
          <div v-if="successMessage" class="mb-4 text-done-fg bg-done-bg p-3 rounded-lg text-sm">
            {{ successMessage }}
          </div>
          
          <div class="border-t border-border pt-4 flex justify-end">
            <button 
              @click="saveSettings" 
              class="btn btn-primary px-8"
              :disabled="submitting || !isTotalValid || hasEmptyTitles"
            >
              <span v-if="submitting">Salvando...</span>
              <span v-else>Salvar e Publicar Versão</span>
            </button>
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>
