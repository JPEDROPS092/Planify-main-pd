<template>
  <div class="w-full h-full">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import Chart from "chart.js/auto";

interface CategoryData {
  categoria_nome: string;
  total_gasto: number;
  total_custos: number;
  percentual: number;
}

const props = defineProps<{
  data: CategoryData[];
}>();

const chartCanvas = ref<HTMLCanvasElement>();
let chartInstance: Chart | null = null;

// Cores para o gráfico de pizza
const colors = [
  "#3B82F6", // blue-500
  "#10B981", // emerald-500
  "#F59E0B", // amber-500
  "#EF4444", // red-500
  "#8B5CF6", // violet-500
  "#06B6D4", // cyan-500
  "#84CC16", // lime-500
  "#F97316", // orange-500
  "#EC4899", // pink-500
  "#6B7280", // gray-500
];

const createChart = () => {
  if (!chartCanvas.value || !props.data) return;

  // Destruir gráfico anterior se existir
  if (chartInstance) {
    chartInstance.destroy();
  }

  const ctx = chartCanvas.value.getContext("2d");
  if (!ctx) return;

  const labels = props.data.map(item => item.categoria_nome || 'Sem categoria');
  const values = props.data.map(item => item.total_gasto);
  const backgroundColors = props.data.map((_, index) => colors[index % colors.length]);

  chartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels,
      datasets: [
        {
          data: values,
          backgroundColor: backgroundColors,
          borderWidth: 2,
          borderColor: "#ffffff",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            padding: 20,
            usePointStyle: true,
          },
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const value = context.parsed;
              const total = values.reduce((sum, val) => sum + val, 0);
              const percentage = ((value / total) * 100).toFixed(1);
              return `${context.label}: ${new Intl.NumberFormat("pt-BR", {
                style: "currency",
                currency: "BRL",
              }).format(value)} (${percentage}%)`;
            },
          },
        },
      },
    },
  });
};

onMounted(() => {
  createChart();
});

watch(() => props.data, () => {
  createChart();
}, { deep: true });
</script>
