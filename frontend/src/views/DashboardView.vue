<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTeamStore } from '@/stores/team'
import EmployeeRow from '@/components/EmployeeRow.vue'
import PerformanceGauge from '@/components/PerformanceGauge.vue'
import HistoryBarChart from '@/components/HistoryBarChart.vue'
import EvaluationModal from '@/components/EvaluationModal.vue'

const router = useRouter()
const teamStore = useTeamStore()

const showEvaluationModal = ref(false)
const selectedEmployeeId = ref(null)
const selectedEmployeeName = ref('')

onMounted(() => {
  teamStore.fetchTeam()
  teamStore.fetchTeamHistory()
})

function handleEvaluate(employeeId) {
  selectedEmployeeId.value = employeeId
  const emp = teamStore.members.find(m => m.id === employeeId)
  selectedEmployeeName.value = emp ? emp.name : 'Funcionário'
  showEvaluationModal.value = true
}

function closeEvaluationModal() {
  showEvaluationModal.value = false
  selectedEmployeeId.value = null
  selectedEmployeeName.value = ''
}
</script>

<template>
  <div class="max-w-[1200px] mx-auto w-full flex flex-col xl:flex-row gap-6 items-start">
    
    <!-- Left Column (Evaluations list) -->
    <div class="w-full xl:w-[60%] flex flex-col gap-4">
      
      <!-- Alert Banner -->
      <div v-if="teamStore.pendingEvaluations.length > 0" class="card bg-[#FDF1E3] border-[#F3D5B5] p-[18px] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div class="flex gap-4 items-start">
          <div class="w-10 h-10 rounded-full bg-[#F3D5B5] flex items-center justify-center shrink-0 text-[#92400E]">
            <font-awesome-icon icon="info-circle" class="w-5 h-5" />
          </div>
          <div>
            <h3 class="font-bold text-[15px] text-[#92400E] leading-tight mb-1">Avaliações Pendentes</h3>
            <p class="text-[13px] text-[#92400E]/80 m-0">Você tem {{ teamStore.pendingEvaluations.length }} avaliações aguardando resposta neste ciclo.</p>
          </div>
        </div>
        <button class="btn bg-[#92400E] text-white hover:bg-[#78350F] whitespace-nowrap" @click="router.push({name: 'employees'})">
          Ver todas
        </button>
      </div>

      <!-- Quick List -->
      <div class="card p-0 overflow-hidden">
        <div class="p-[18px] border-b border-border flex items-center justify-between">
          <h2 class="text-[15px] font-bold m-0 text-textMain">Sua Equipe Direta</h2>
          <button class="text-[12.5px] font-semibold text-brand-700 hover:text-brand-800" @click="router.push({name: 'employees'})">Ver árvore completa</button>
        </div>
        
        <div class="flex flex-col">
          <div v-if="teamStore.loading" class="p-6 text-center text-text2 text-sm">Carregando...</div>
          <div v-else-if="teamStore.members.length === 0" class="p-6 text-center text-text2 text-sm">Nenhum funcionário encontrado.</div>
          <EmployeeRow 
            v-else
            v-for="employee in teamStore.members.filter(m => m.relation === 'direto').slice(0, 5)" 
            :key="employee.id" 
            :employee="employee"
            @action="handleEvaluate"
          />
        </div>
      </div>
      
    </div>

    <!-- Right Column (Charts) -->
    <div class="w-full xl:w-[40%] flex flex-col gap-4">
      
      <div class="card p-[18px]">
        <h2 class="text-[15px] font-bold m-0 text-textMain mb-1">Status do Ciclo</h2>
        <p class="text-[12.5px] text-text2">Progresso das avaliações da semana atual</p>
        
        <PerformanceGauge 
          :completed="teamStore.completedEvaluations.length"
          :total="teamStore.members.length"
        />
        
        <div class="flex justify-center gap-6 mt-2 pt-4 border-t border-border">
          <div class="text-center">
            <span class="block text-2xl font-bold text-textMain leading-tight">{{ teamStore.completedEvaluations.length }}</span>
            <span class="text-[11px] font-semibold text-text2 uppercase tracking-wide">Realizadas</span>
          </div>
          <div class="text-center">
            <span class="block text-2xl font-bold text-textMain leading-tight">{{ teamStore.pendingEvaluations.length }}</span>
            <span class="text-[11px] font-semibold text-text2 uppercase tracking-wide">Pendentes</span>
          </div>
        </div>
      </div>
      
      <div class="card p-[18px]">
        <div class="flex items-center justify-between mb-1">
          <h2 class="text-[15px] font-bold m-0 text-textMain">Histórico de Performance</h2>
          <span class="badge bg-[#F0EEF3] text-textMain font-medium">Equipe Direta</span>
        </div>
        <p class="text-[12.5px] text-text2">Evolução média das notas nos últimos 6 meses</p>
        
        <HistoryBarChart />
      </div>

    </div>

    <EvaluationModal 
      v-if="showEvaluationModal" 
      :employee-id="selectedEmployeeId"
      :employee-name="selectedEmployeeName"
      @close="closeEvaluationModal"
      @success="() => { closeEvaluationModal(); teamStore.fetchTeam(); }"
    />
  </div>
</template>
