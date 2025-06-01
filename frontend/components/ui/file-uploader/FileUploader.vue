<!--
  FileUploader.vue
  
  Componente para upload de arquivos com suporte a drag-and-drop,
  visualização de progresso e validação de tipos de arquivo.
  
  Props:
  - accept: Tipos de arquivo aceitos (ex: 'image/*,.pdf')
  - multiple: Permite selecionar múltiplos arquivos
  - maxSize: Tamanho máximo do arquivo em bytes
  - maxFiles: Número máximo de arquivos permitidos
  - disabled: Se o componente está desabilitado
  - class: Classes CSS adicionais
  
  Eventos:
  - files-selected: Emitido quando arquivos são selecionados
  - file-error: Emitido quando ocorre um erro (tamanho excedido, tipo inválido, etc.)
  - upload-progress: Emitido durante o progresso do upload
  - upload-complete: Emitido quando o upload é concluído
-->

<script setup lang="ts">
import { ref, computed } from 'vue';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Upload, X, File, AlertCircle } from 'lucide-vue-next';

const props = withDefaults(
  defineProps<{
    accept?: string;
    multiple?: boolean;
    maxSize?: number;
    maxFiles?: number;
    disabled?: boolean;
    class?: string;
  }>(),
  {
    accept: '',
    multiple: false,
    maxSize: 5 * 1024 * 1024, // 5MB
    maxFiles: 5,
    disabled: false,
  }
);

const emit = defineEmits<{
  'files-selected': [files: File[]];
  'file-error': [error: string];
  'upload-progress': [progress: number];
  'upload-complete': [fileUrls: string[]];
}>();

const fileInputRef = ref<HTMLInputElement | null>(null);
const isDragging = ref(false);
const selectedFiles = ref<File[]>([]);
const uploadProgress = ref<number>(0);
const errors = ref<string[]>([]);
const isUploading = ref(false);

const hasFiles = computed(() => selectedFiles.value.length > 0);

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const openFileDialog = () => {
  if (!props.disabled && fileInputRef.value) {
    fileInputRef.value.click();
  }
};

const handleDragOver = (e: DragEvent) => {
  e.preventDefault();
  e.stopPropagation();
  if (!props.disabled) {
    isDragging.value = true;
  }
};

const handleDragLeave = (e: DragEvent) => {
  e.preventDefault();
  e.stopPropagation();
  isDragging.value = false;
};

const validateFiles = (files: File[]): boolean => {
  errors.value = [];

  // Verificar número máximo de arquivos
  if (props.multiple && files.length > props.maxFiles) {
    errors.value.push(
      `Número máximo de arquivos excedido (máximo: ${props.maxFiles})`
    );
    return false;
  }

  // Verificar tipos de arquivo
  if (props.accept) {
    const acceptedTypes = props.accept.split(',').map((type) => type.trim());

    for (const file of files) {
      const fileType = file.type;
      const fileExtension = '.' + file.name.split('.').pop();

      const isAccepted = acceptedTypes.some((type) => {
        if (type.startsWith('.')) {
          // Verificar extensão
          return fileExtension.toLowerCase() === type.toLowerCase();
        } else if (type.endsWith('/*')) {
          // Verificar tipo MIME genérico (ex: image/*)
          const genericType = type.replace('/*', '');
          return fileType.startsWith(genericType);
        } else {
          // Verificar tipo MIME específico
          return fileType === type;
        }
      });

      if (!isAccepted) {
        errors.value.push(`Tipo de arquivo não permitido: ${file.name}`);
        return false;
      }
    }
  }

  // Verificar tamanho máximo
  for (const file of files) {
    if (file.size > props.maxSize) {
      errors.value.push(
        `Arquivo muito grande: ${file.name} (${formatFileSize(file.size)}). Tamanho máximo: ${formatFileSize(props.maxSize)}`
      );
      return false;
    }
  }

  return true;
};

const handleFilesSelected = (e: Event) => {
  const input = e.target as HTMLInputElement;
  if (input.files && input.files.length > 0) {
    const fileList = Array.from(input.files);

    if (validateFiles(fileList)) {
      if (props.multiple) {
        selectedFiles.value = [...selectedFiles.value, ...fileList];
      } else {
        selectedFiles.value = [fileList[0]];
      }

      emit('files-selected', selectedFiles.value);
    } else {
      emit('file-error', errors.value.join(', '));
    }
  }
};

const handleDrop = (e: DragEvent) => {
  e.preventDefault();
  e.stopPropagation();
  isDragging.value = false;

  if (props.disabled) return;

  if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
    const fileList = Array.from(e.dataTransfer.files);

    if (validateFiles(fileList)) {
      if (props.multiple) {
        selectedFiles.value = [...selectedFiles.value, ...fileList];
      } else {
        selectedFiles.value = [fileList[0]];
      }

      emit('files-selected', selectedFiles.value);
    } else {
      emit('file-error', errors.value.join(', '));
    }
  }
};

const removeFile = (index: number) => {
  selectedFiles.value.splice(index, 1);
  emit('files-selected', selectedFiles.value);
};

const simulateUpload = () => {
  if (selectedFiles.value.length === 0) return;

  isUploading.value = true;
  uploadProgress.value = 0;

  // Simulação de upload com progresso
  const interval = setInterval(() => {
    uploadProgress.value += 10;
    emit('upload-progress', uploadProgress.value);

    if (uploadProgress.value >= 100) {
      clearInterval(interval);
      isUploading.value = false;

      // Simular URLs de arquivos enviados
      const fileUrls = selectedFiles.value.map(
        (file) => `https://example.com/uploads/${file.name}`
      );
      emit('upload-complete', fileUrls);
    }
  }, 300);
};

const clearFiles = () => {
  selectedFiles.value = [];
  uploadProgress.value = 0;
  errors.value = [];
  if (fileInputRef.value) {
    fileInputRef.value.value = '';
  }
};
</script>

<template>
  <div :class="props.class">
    <!-- Área de upload -->
    <div
      class="relative border-2 border-dashed rounded-lg p-6 transition-colors"
      :class="[
        isDragging
          ? 'border-primary bg-primary/5'
          : 'border-input bg-background',
        disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
      ]"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
      @drop="handleDrop"
      @click="openFileDialog"
    >
      <input
        ref="fileInputRef"
        type="file"
        :accept="accept"
        :multiple="multiple"
        class="hidden"
        :disabled="disabled"
        @change="handleFilesSelected"
      />

      <div
        class="flex flex-col items-center justify-center space-y-2 text-center"
      >
        <Upload class="h-10 w-10 text-muted-foreground" />
        <div class="flex flex-col space-y-1">
          <p class="text-sm font-medium">
            <span class="text-primary font-semibold"
              >Clique para fazer upload</span
            >
            ou arraste e solte
          </p>
          <p class="text-xs text-muted-foreground">
            {{ multiple ? 'Arquivos' : 'Arquivo' }}
            {{ accept ? `(${accept})` : '' }}
          </p>
          <p v-if="maxSize" class="text-xs text-muted-foreground">
            Tamanho máximo: {{ formatFileSize(maxSize) }}
          </p>
        </div>
      </div>
    </div>

    <!-- Lista de erros -->
    <div v-if="errors.length > 0" class="mt-2">
      <div
        v-for="(error, index) in errors"
        :key="index"
        class="flex items-center text-destructive text-sm mt-1"
      >
        <AlertCircle class="h-4 w-4 mr-1" />
        <span>{{ error }}</span>
      </div>
    </div>

    <!-- Progresso de upload -->
    <div v-if="isUploading" class="mt-4">
      <div class="text-sm font-medium mb-1">Enviando arquivos...</div>
      <div class="w-full h-2 bg-secondary rounded-full overflow-hidden">
        <div
          class="h-full bg-primary transition-all duration-300 ease-in-out"
          :style="{ width: `${uploadProgress}%` }"
        ></div>
      </div>
    </div>

    <!-- Lista de arquivos selecionados -->
    <div v-if="hasFiles" class="mt-4 space-y-2">
      <div class="text-sm font-medium">Arquivos selecionados</div>
      <ul class="space-y-2">
        <li
          v-for="(file, index) in selectedFiles"
          :key="index"
          class="flex items-center justify-between p-2 bg-accent/30 rounded-md"
        >
          <div class="flex items-center space-x-2">
            <File class="h-5 w-5 text-muted-foreground" />
            <div>
              <p class="text-sm font-medium truncate max-w-[200px]">
                {{ file.name }}
              </p>
              <p class="text-xs text-muted-foreground">
                {{ formatFileSize(file.size) }}
              </p>
            </div>
          </div>
          <button
            @click.stop="removeFile(index)"
            class="text-muted-foreground hover:text-destructive focus:outline-none"
          >
            <X class="h-4 w-4" />
          </button>
        </li>
      </ul>

      <div class="flex space-x-2 mt-4">
        <Button variant="outline" size="sm" @click.stop="clearFiles">
          Limpar
        </Button>
        <Button size="sm" @click.stop="simulateUpload" :disabled="isUploading">
          Enviar arquivos
        </Button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Estilos específicos para o componente, se necessário */
</style>
