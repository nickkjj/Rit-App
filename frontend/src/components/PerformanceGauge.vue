<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  completed: { type: Number, required: true },
  total: { type: Number, required: true }
})

const chartData = computed(() => ({
  labels: ['Realizadas', 'Pendentes'],
  datasets: [
    {
      data: [props.completed, props.total - props.completed],
      backgroundColor: ['#55286F', '#E4E1EA'], // brand-700 and border
      borderWidth: 0,
      circumference: 180,
      rotation: 270,
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '75%',
  plugins: {
    legend: { display: false },
    tooltip: { enabled: true }
  }
}
</script>

<template>
  <div class="relative w-full h-[140px] flex items-end justify-center mb-2 mt-4">
    <Doughnut :data="chartData" :options="chartOptions" />
    <div class="absolute inset-0 flex flex-col items-center justify-end pb-2 pointer-events-none">
      <span class="text-3xl font-bold text-textMain leading-none">{{ completed }}</span>
      <span class="text-[12px] text-text2 font-medium">de {{ total }} relatórios</span>
    </div>
  </div>
</template>
