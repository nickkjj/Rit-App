<script setup>
import { computed } from 'vue'

const props = defineProps({
  relation: {
    type: String,
    required: true
  }
})

const displayRelation = computed(() => {
  return props.relation.toLowerCase() === 'direto' ? 'Direto' : 'Indireto'
})
</script>

<template>
  <span class="rel-chip">
    {{ displayRelation }}
  </span>
</template>
