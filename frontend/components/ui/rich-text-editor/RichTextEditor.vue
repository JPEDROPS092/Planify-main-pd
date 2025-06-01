<!--
  RichTextEditor.vue
  
  Editor de texto rico para o Planify.
  Permite formatação de texto, listas, links e outros elementos.
  
  Props:
  - modelValue: Conteúdo do editor (v-model)
  - placeholder: Texto de placeholder
  - readonly: Se o editor está em modo somente leitura
  - minHeight: Altura mínima do editor
  - maxHeight: Altura máxima do editor
  - toolbar: Configuração da barra de ferramentas
  - class: Classes CSS adicionais
  
  Eventos:
  - update:modelValue: Emitido quando o conteúdo é alterado
  - focus: Emitido quando o editor recebe foco
  - blur: Emitido quando o editor perde foco
-->

<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue';
import { cn } from '@/lib/utils';
import {
  Bold,
  Italic,
  Underline,
  List,
  ListOrdered,
  Link,
  Image,
  AlignLeft,
  AlignCenter,
  AlignRight,
  Heading1,
  Heading2,
  Code,
  Undo,
  Redo,
} from 'lucide-vue-next';

const props = withDefaults(
  defineProps<{
    modelValue?: string;
    placeholder?: string;
    readonly?: boolean;
    minHeight?: string;
    maxHeight?: string;
    toolbar?: string[];
    class?: string;
  }>(),
  {
    modelValue: '',
    placeholder: 'Comece a digitar...',
    readonly: false,
    minHeight: '150px',
    maxHeight: '500px',
    toolbar: () => [
      'bold',
      'italic',
      'underline',
      'heading',
      'list',
      'link',
      'image',
      'align',
    ],
  }
);

const emit = defineEmits<{
  'update:modelValue': [value: string];
  focus: [event: FocusEvent];
  blur: [event: FocusEvent];
}>();

const editorRef = ref<HTMLDivElement | null>(null);
const content = ref(props.modelValue);
const isEditorFocused = ref(false);

// Observar mudanças no modelValue
watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue !== content.value) {
      content.value = newValue;
      if (editorRef.value) {
        editorRef.value.innerHTML = newValue;
      }
    }
  }
);

// Atualizar o modelo quando o conteúdo do editor muda
const updateContent = () => {
  if (editorRef.value) {
    content.value = editorRef.value.innerHTML;
    emit('update:modelValue', content.value);
  }
};

// Comandos de formatação
const formatDoc = (command: string, value: string | null = null) => {
  if (props.readonly) return;
  document.execCommand(command, false, value);
  updateContent();
  editorRef.value?.focus();
};

// Funções de formatação específicas
const formatBold = () => formatDoc('bold');
const formatItalic = () => formatDoc('italic');
const formatUnderline = () => formatDoc('underline');
const formatHeading = (level: number) =>
  formatDoc('formatBlock', `<h${level}>`);
const formatParagraph = () => formatDoc('formatBlock', '<p>');
const formatBulletList = () => formatDoc('insertUnorderedList');
const formatNumberedList = () => formatDoc('insertOrderedList');
const formatAlign = (align: string) => formatDoc('justify' + align);
const formatUndo = () => formatDoc('undo');
const formatRedo = () => formatDoc('redo');

// Inserir link
const insertLink = () => {
  const url = prompt('Insira a URL do link:', 'http://');
  if (url) {
    formatDoc('createLink', url);
  }
};

// Inserir imagem
const insertImage = () => {
  const url = prompt('Insira a URL da imagem:', 'http://');
  if (url) {
    formatDoc('insertImage', url);
  }
};

// Eventos de foco
const handleFocus = (event: FocusEvent) => {
  isEditorFocused.value = true;
  emit('focus', event);
};

const handleBlur = (event: FocusEvent) => {
  isEditorFocused.value = false;
  emit('blur', event);
};

// Inicializar o editor
onMounted(() => {
  if (editorRef.value) {
    editorRef.value.innerHTML = content.value;

    // Adicionar ouvintes de evento para capturar mudanças
    editorRef.value.addEventListener('input', updateContent);
    editorRef.value.addEventListener('focus', handleFocus);
    editorRef.value.addEventListener('blur', handleBlur);
  }
});

// Limpar ouvintes de evento ao desmontar
onUnmounted(() => {
  if (editorRef.value) {
    editorRef.value.removeEventListener('input', updateContent);
    editorRef.value.removeEventListener('focus', handleFocus);
    editorRef.value.removeEventListener('blur', handleBlur);
  }
});
</script>

<template>
  <div :class="cn('rich-text-editor', props.class)">
    <!-- Barra de ferramentas -->
    <div
      class="flex flex-wrap items-center gap-1 p-2 border-b bg-muted/30 rounded-t-md"
      :class="{ 'opacity-50 pointer-events-none': readonly }"
    >
      <!-- Formatação de texto -->
      <button
        v-if="toolbar.includes('bold')"
        @click="formatBold"
        class="p-1 rounded hover:bg-accent"
        title="Negrito"
      >
        <Bold class="h-4 w-4" />
      </button>

      <button
        v-if="toolbar.includes('italic')"
        @click="formatItalic"
        class="p-1 rounded hover:bg-accent"
        title="Itálico"
      >
        <Italic class="h-4 w-4" />
      </button>

      <button
        v-if="toolbar.includes('underline')"
        @click="formatUnderline"
        class="p-1 rounded hover:bg-accent"
        title="Sublinhado"
      >
        <Underline class="h-4 w-4" />
      </button>

      <!-- Divisor -->
      <div
        v-if="toolbar.includes('heading')"
        class="w-px h-6 bg-border mx-1"
      ></div>

      <!-- Cabeçalhos -->
      <div v-if="toolbar.includes('heading')" class="flex items-center">
        <button
          @click="formatHeading(1)"
          class="p-1 rounded hover:bg-accent"
          title="Título 1"
        >
          <Heading1 class="h-4 w-4" />
        </button>

        <button
          @click="formatHeading(2)"
          class="p-1 rounded hover:bg-accent"
          title="Título 2"
        >
          <Heading2 class="h-4 w-4" />
        </button>

        <button
          @click="formatParagraph"
          class="p-1 rounded hover:bg-accent"
          title="Parágrafo"
        >
          <span class="text-xs font-bold">P</span>
        </button>
      </div>

      <!-- Divisor -->
      <div
        v-if="toolbar.includes('list')"
        class="w-px h-6 bg-border mx-1"
      ></div>

      <!-- Listas -->
      <div v-if="toolbar.includes('list')" class="flex items-center">
        <button
          @click="formatBulletList"
          class="p-1 rounded hover:bg-accent"
          title="Lista com marcadores"
        >
          <List class="h-4 w-4" />
        </button>

        <button
          @click="formatNumberedList"
          class="p-1 rounded hover:bg-accent"
          title="Lista numerada"
        >
          <ListOrdered class="h-4 w-4" />
        </button>
      </div>

      <!-- Divisor -->
      <div
        v-if="toolbar.includes('align')"
        class="w-px h-6 bg-border mx-1"
      ></div>

      <!-- Alinhamento -->
      <div v-if="toolbar.includes('align')" class="flex items-center">
        <button
          @click="formatAlign('Left')"
          class="p-1 rounded hover:bg-accent"
          title="Alinhar à esquerda"
        >
          <AlignLeft class="h-4 w-4" />
        </button>

        <button
          @click="formatAlign('Center')"
          class="p-1 rounded hover:bg-accent"
          title="Centralizar"
        >
          <AlignCenter class="h-4 w-4" />
        </button>

        <button
          @click="formatAlign('Right')"
          class="p-1 rounded hover:bg-accent"
          title="Alinhar à direita"
        >
          <AlignRight class="h-4 w-4" />
        </button>
      </div>

      <!-- Divisor -->
      <div
        v-if="toolbar.includes('link') || toolbar.includes('image')"
        class="w-px h-6 bg-border mx-1"
      ></div>

      <!-- Links e imagens -->
      <div
        v-if="toolbar.includes('link') || toolbar.includes('image')"
        class="flex items-center"
      >
        <button
          v-if="toolbar.includes('link')"
          @click="insertLink"
          class="p-1 rounded hover:bg-accent"
          title="Inserir link"
        >
          <Link class="h-4 w-4" />
        </button>

        <button
          v-if="toolbar.includes('image')"
          @click="insertImage"
          class="p-1 rounded hover:bg-accent"
          title="Inserir imagem"
        >
          <Image class="h-4 w-4" />
        </button>
      </div>

      <!-- Divisor -->
      <div class="w-px h-6 bg-border mx-1"></div>

      <!-- Desfazer/Refazer -->
      <div class="flex items-center">
        <button
          @click="formatUndo"
          class="p-1 rounded hover:bg-accent"
          title="Desfazer"
        >
          <Undo class="h-4 w-4" />
        </button>

        <button
          @click="formatRedo"
          class="p-1 rounded hover:bg-accent"
          title="Refazer"
        >
          <Redo class="h-4 w-4" />
        </button>
      </div>
    </div>

    <!-- Área de edição -->
    <div
      ref="editorRef"
      class="p-3 outline-none overflow-auto"
      :class="[
        isEditorFocused ? 'ring-1 ring-ring' : 'border-b border-l border-r',
        readonly ? 'bg-muted/30 cursor-default' : 'bg-background',
      ]"
      :contenteditable="!readonly"
      :style="{
        minHeight: minHeight,
        maxHeight: maxHeight,
      }"
      :placeholder="placeholder"
    ></div>
  </div>
</template>

<style scoped>
[contenteditable]:empty:before {
  content: attr(placeholder);
  color: #9ca3af; /* text-muted-foreground */
  pointer-events: none;
  display: block;
}
</style>
