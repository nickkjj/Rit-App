<script setup>
import { onMounted, ref, computed } from 'vue'
import { useTeamStore } from '@/stores/team'
import EmployeeRow from '@/components/EmployeeRow.vue'
import EvaluationModal from '@/components/EvaluationModal.vue'

const teamStore = useTeamStore()
const searchQuery = ref('')
const filterStatus = ref('Todos')

onMounted(() => {
  if (teamStore.members.length === 0) {
    teamStore.fetchTeam()
  }
})

const filteredEmployees = computed(() => {
  let list = teamStore.members
  
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(e => e.name.toLowerCase().includes(q) || e.position_name.toLowerCase().includes(q))
  }
  
  if (filterStatus.value === 'Pendentes') {
    list = list.filter(e => e.evaluation_status === 'Pendente')
  } else if (filterStatus.value === 'Realizadas') {
    list = list.filter(e => e.evaluation_status !== 'Pendente')
  }
  
  return list
})

const showEvaluationModal = ref(false)
const selectedEmployeeId = ref(null)
const selectedEmployeeName = ref('')

function handleAction(id) {
  selectedEmployeeId.value = id
  const emp = teamStore.members.find(m => m.id === id)
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
  <div class="max-w-[1200px] mx-auto w-full">
    
    <div class="card overflow-hidden">
      <div class="p-4 md:p-[24px] border-b border-border flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 class="text-[16px] font-bold m-0 text-textMain">Lista de Funcionários</h2>
          <p class="text-[13px] text-text2 mt-1">Gerencie sua equipe e realize avaliações pendentes.</p>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-3">
          <div class="relative">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Buscar por nome..." 
              class="w-full sm:w-[200px] pl-9 pr-3 py-[9px] text-[13.5px] rounded-custom border border-border bg-surface focus:outline-none focus:border-brand-700 text-textMain"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-text3">
              <font-awesome-icon icon="magnifying-glass" class="w-4 h-4" />
            </div>
          </div>
          
          <select 
            v-model="filterStatus"
            class="sm:w-[150px] border border-border rounded-custom py-[9px] px-3 pr-8 appearance-none bg-surface text-[13.5px] text-textMain focus:outline-none focus:border-brand-700 cursor-pointer"
          >
            <option>Todos</option>
            <option>Pendentes</option>
            <option>Realizadas</option>
          </select>
        </div>
      </div>
      
      <div class="flex flex-col">
        <div v-if="teamStore.loading" class="p-10 text-center text-text2 text-sm">Carregando lista...</div>
        <div v-else-if="filteredEmployees.length === 0" class="p-10 text-center text-text2 text-sm">Nenhum funcionário encontrado com os filtros aplicados.</div>
        
        <div v-else class="flex flex-col w-full">
          <!-- Desktop Header -->
          <div class="hidden md:flex items-center gap-[11px] px-[18px] py-[10px] bg-bg/50 border-b border-border text-[12px] font-bold text-text3 uppercase tracking-wider">
            <div class="w-[28px] shrink-0"></div>
            <div class="flex-1 min-w-0">Funcionário</div>
            <div class="w-[80px]">Relação</div>
            <div class="w-[120px]">Status</div>
            <div class="w-[85px] text-right">Ação</div>
          </div>
          
          <EmployeeRow 
            v-for="employee in filteredEmployees" 
            :key="employee.id" 
            :employee="employee"
            @action="handleAction"
          />
        </div>
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
