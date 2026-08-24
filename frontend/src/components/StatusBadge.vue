<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true
  }
})

const isPending = computed(() => props.status === 'Pendente')
</script>

<template>
  <span 
    class="badge" 
    :class="isPending ? 'badge-pending' : 'badge-done'"
  >
    {{ status }}
  </span>
</template>
