<template>
  <div v-if="fileUrl">
    <a :href="fileUrl" target="_blank" rel="noopener noreferrer">
      <!-- 1. Usar ref para referenciar o canvas -->
      <canvas ref="canvasEl" class="border-2 hover:border-red-800"/>
    </a>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import * as pdfjsLib from 'pdfjs-dist';

// 2. Importe o worker com o sufixo "?url" do Vite
// Isso instrui o Vite a copiar o arquivo do worker para a pasta de build
// e nos dá a URL pública correta para ele.
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.mjs?url';

// 3. Defina a fonte do worker UMA VEZ.
pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;

// Define as props do componente com TypeScript
const props = defineProps<{
  fileUrl: string;
  width?: number;
}>();

// Cria uma referência para o elemento canvas no template
const canvasEl = ref<HTMLCanvasElement | null>(null);

const renderThumbnail = async () => {
  // Garante que a URL e o elemento canvas existam
  if (!props.fileUrl || !canvasEl.value) {
    return;
  }

  try {
    // 4. Não precisa criar o `new PDFWorker()` aqui
    const pdf = await pdfjsLib.getDocument(props.fileUrl).promise;
    const page = await pdf.getPage(1); // Pega a primeira página

    const desiredWidth = props.width || 200;
    let viewport = page.getViewport({ scale: 1.0 });
    const scale = desiredWidth / viewport.width;
    viewport = page.getViewport({ scale });

    const canvas = canvasEl.value;
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    const context = canvas.getContext('2d');
    if (context) {
      await page.render({ canvasContext: context, viewport: viewport }).promise;
    }
  } catch (error) {
    console.error('Erro ao renderizar o thumbnail do PDF:', error);
  }
};

// 5. Renderiza quando o componente é montado
onMounted(() => {
  renderThumbnail();
});

// 6. (Bônus) Observa mudanças na prop fileUrl e renderiza novamente
// Isso torna o componente reutilizável se a URL do PDF mudar dinamicamente.
watch(() => props.fileUrl, () => {
  renderThumbnail();
});
</script>