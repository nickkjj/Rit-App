<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/api'

const props = defineProps({
  employeeId: {
    type: Number,
    required: true
  },
  employeeName: {
    type: String,
    default: 'Funcionário'
  }
})

const emit = defineEmits(['close', 'success'])

const loading = ref(true)
const submitting = ref(false)
const error = ref('')
const questions = ref([])
const answers = ref({}) // { questionId: value (1-4) }

const isRecent = ref(false)
const recentData = ref(null)

onMounted(async () => {
  try {
    // Primeiro tenta buscar se já existe avaliação recente
    const recentRes = await api.get(`/evaluations/recent/?employee_id=${props.employeeId}`)
    
    if (recentRes.data.recent) {
      isRecent.value = true
      recentData.value = recentRes.data
    } else {
      // Se não, busca o formulário atual para avaliar
      const res = await api.get('/questions/versions/current/')
      questions.value = res.data.questions || []
      
      questions.value.forEach(q => {
        answers.value[q.id] = null
      })
    }
  } catch (err) {
    console.error(err)
    error.value = 'Erro ao carregar os dados.'
  } finally {
    loading.value = false
  }
})

const allAnswered = computed(() => {
  return questions.value.length > 0 && questions.value.every(q => answers.value[q.id] !== null)
})

async function submitEvaluation() {
  if (!allAnswered.value || isRecent.value) return
  
  submitting.value = true
  error.value = ''
  
  const payload = {
    employee_id: props.employeeId,
    answers: Object.entries(answers.value).map(([question_id, answer]) => ({
      question_id: parseInt(question_id),
      answer: parseInt(answer)
    }))
  }
  
  try {
    await api.post('/evaluations/', payload)
    emit('success')
  } catch (err) {
    console.error(err)
    if (err.response && err.response.data && err.response.data.non_field_errors) {
      error.value = err.response.data.non_field_errors[0]
    } else {
      error.value = 'Erro ao enviar avaliação.'
    }
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="fixed inset-0 z-[100] flex items-center justify-center bg-[#140A1C]/50 p-4">
    <div class="bg-surface rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden">
      
      <!-- Header -->
      <div class="p-5 border-b border-border flex justify-between items-center bg-bg/50">
        <h2 class="text-[16px] font-bold text-textMain m-0">Avaliação de Desempenho</h2>
        <button @click="emit('close')" class="text-text3 hover:text-textMain transition-colors">
          <font-awesome-icon icon="times" class="w-5 h-5" />
        </button>
      </div>
      
      <!-- Body -->
      <div class="p-6 overflow-y-auto flex-1">
        <div v-if="loading" class="text-center text-text2 py-8">Carregando formulário...</div>
        
        <div v-else-if="error && !questions.length" class="text-center text-alert-fg py-8 bg-alert-bg rounded-lg">
          {{ error }}
        </div>
        
        <!-- Estado: Avaliação Recente (Read-Only) -->
        <div v-else-if="isRecent" class="space-y-6">
          <div class="bg-brand-050 border border-brand-200 rounded-lg p-4 flex gap-3 items-start">
            <div class="text-brand-600 mt-0.5">
              <font-awesome-icon icon="clock" class="w-5 h-5" />
            </div>
            <div>
              <h4 class="text-brand-800 font-bold text-[14px]">Avaliação já realizada recentemente</h4>
              <p class="text-brand-700 text-[13px] mt-1">
                Você já avaliou {{ employeeName }} há pouco tempo. O ciclo é de uma semana.
                <br>
                <strong>Próxima avaliação disponível em: {{ recentData?.days_left }} dias e {{ recentData?.hours_left }} horas.</strong>
              </p>
            </div>
          </div>
          
          <div>
            <h3 class="font-bold text-textMain text-[15px] mb-3 border-b border-border pb-2">Histórico da última avaliação</h3>
            <div class="space-y-3">
              <div v-for="(ans, idx) in recentData?.answers" :key="idx" class="border border-border bg-surface p-3 rounded-lg flex justify-between items-center">
                <div>
                  <div class="text-[13px] font-semibold text-textMain">{{ ans.question_title }}</div>
                  <div class="text-[11px] text-text2">Peso: {{ ans.weight }}%</div>
                </div>
                <div class="w-8 h-8 rounded-full bg-brand-100 text-brand-700 font-bold flex items-center justify-center shrink-0">
                  {{ ans.answer }}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Estado: Pendente (Formulário) -->
        <div v-else class="space-y-6">
          <p class="text-[13.5px] text-text2 mb-4">
            Responda as questões abaixo com notas de 1 a 4, onde 1 é o menor nível de proficiência e 4 é o maior nível de proficiência.
          </p>
          
          <div v-for="(question, index) in questions" :key="question.id" class="border border-border rounded-lg p-5 bg-surface">
            <div class="flex gap-3 mb-4">
              <div class="w-6 h-6 rounded-full bg-brand-050 text-brand-700 flex items-center justify-center font-bold text-xs shrink-0">
                {{ index + 1 }}
              </div>
              <div>
                <h4 class="text-[14px] font-bold text-textMain leading-tight mb-1">{{ question.title }}</h4>
                <span class="text-[11.5px] font-semibold text-brand-300">Peso na nota: {{ question.weight }}%</span>
              </div>
            </div>
            
            <div class="grid grid-cols-4 gap-2">
              <label 
                v-for="score in 4" :key="score"
                class="relative flex flex-col items-center p-3 cursor-pointer border rounded-lg transition-all"
                :class="answers[question.id] === score ? 'border-brand-600 bg-brand-050 ring-1 ring-brand-600' : 'border-border hover:border-text3'"
              >
                <input 
                  type="radio" 
                  :name="'question_' + question.id" 
                  :value="score" 
                  v-model="answers[question.id]"
                  class="sr-only"
                >
                <span class="text-lg font-bold" :class="answers[question.id] === score ? 'text-brand-700' : 'text-textMain'">
                  {{ score }}
                </span>
                <span class="text-[10px] uppercase font-bold tracking-wider mt-1" :class="answers[question.id] === score ? 'text-brand-600' : 'text-text3'">
                  {{ score === 1 ? 'Ruim' : score === 2 ? 'Regular' : score === 3 ? 'Bom' : 'Ótimo' }}
                </span>
              </label>
            </div>
          </div>
          
          <div v-if="error && questions.length" class="text-alert-fg bg-alert-bg p-3 rounded-lg text-sm mt-4">
            {{ error }}
          </div>
        </div>
      </div>
      
      <!-- Footer -->
      <div class="p-5 border-t border-border bg-bg/50 flex justify-end gap-3">
        <button @click="emit('close')" class="btn btn-ghost" :disabled="submitting">
          {{ isRecent ? 'Fechar' : 'Cancelar' }}
        </button>
        <button 
          v-if="!isRecent"
          @click="submitEvaluation" 
          class="btn btn-primary"
          :disabled="loading || submitting || !allAnswered"
        >
          <span v-if="submitting">Enviando...</span>
          <span v-else>Confirmar Avaliação</span>
        </button>
      </div>
      
    </div>
  </div>
</template>
