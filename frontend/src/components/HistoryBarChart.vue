<script setup>
import { ref, onMounted, watch } from 'vue'
import { Chart, BarController, BarElement, CategoryScale, LinearScale, Tooltip } from 'chart.js'
import { useTeamStore } from '@/stores/team'

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip)

const teamStore = useTeamStore()
const chartCanvas = ref(null)
let chartInstance = null

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy()
  }
  
  if (!chartCanvas.value) return
  
  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels: teamStore.historyLabels,
      datasets: [{
        label: 'Média de Desempenho',
        data: teamStore.historyData,
        backgroundColor: '#7A32F2',
        borderRadius: 4,
        barThickness: 16
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#383838',
          padding: 8,
          titleFont: { size: 12 },
          bodyFont: { size: 12 },
          callbacks: {
            label: function(context) {
              return context.parsed.y + ' pontos'
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false, drawBorder: false },
          ticks: { font: { size: 11 }, color: '#888' }
        },
        y: {
          grid: { color: '#E5E7EB', drawBorder: false, borderDash: [4, 4] },
          ticks: { font: { size: 11 }, color: '#888', stepSize: 20 },
          min: 0,
          max: 100
        }
      }
    }
  })
}

onMounted(() => {
  renderChart()
})

watch(() => [teamStore.historyData, teamStore.historyLabels], () => {
  renderChart()
}, { deep: true })
</script>

<template>
  <div class="w-full h-[180px] mt-4">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>
