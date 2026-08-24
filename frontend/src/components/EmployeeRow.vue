<script setup>
import { computed } from 'vue'
import StatusBadge from './StatusBadge.vue'
import RelationBadge from './RelationBadge.vue'

const props = defineProps({
  employee: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['action'])

const initials = computed(() => {
  if (!props.employee.name) return ''
  const parts = props.employee.name.split(' ')
  if (parts.length === 1) return parts[0][0].toUpperCase()
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
})

const isPending = computed(() => props.employee.evaluation_status === 'Pendente')
</script>

<template>
  <div class="flex items-center gap-[11px] px-[18px] py-[11px] border-t border-border">
    <span class="avatar">{{ initials }}</span>
    <div class="flex-1 min-w-0">
      <b class="block text-[13.5px] font-semibold">{{ employee.name }}</b>
      <span class="text-[12px] text-text2">{{ employee.position_name }}</span>
    </div>
    <RelationBadge :relation="employee.relation" />
    <StatusBadge :status="employee.evaluation_status" />
    
    <button 
      class="btn btn-sm shrink-0" 
      :class="isPending ? 'btn-primary' : 'btn-ghost'"
      @click="emit('action', employee.id)"
    >
      {{ isPending ? 'Avaliar' : 'Ver' }}
    </button>
  </div>
</template>
