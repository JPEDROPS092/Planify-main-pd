<!--
  DateRangePicker.vue
  
  Componente para seleção de intervalo de datas.
  Permite ao usuário selecionar uma data de início e uma data de fim.
  
  Props:
  - startDate: Data inicial selecionada
  - endDate: Data final selecionada
  - minDate: Data mínima permitida
  - maxDate: Data máxima permitida
  - format: Formato de exibição da data (padrão: DD/MM/YYYY)
  - placeholder: Texto de placeholder
  - disabled: Se o componente está desabilitado
  - class: Classes CSS adicionais
  
  Eventos:
  - update:startDate: Emitido quando a data inicial é alterada
  - update:endDate: Emitido quando a data final é alterada
  - change: Emitido quando qualquer data é alterada
-->

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { format, isAfter, isBefore, parse } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Calendar } from 'lucide-vue-next';

const props = withDefaults(
  defineProps<{
    startDate?: Date | null;
    endDate?: Date | null;
    minDate?: Date;
    maxDate?: Date;
    format?: string;
    placeholder?: string;
    disabled?: boolean;
    class?: string;
  }>(),
  {
    format: 'dd/MM/yyyy',
    placeholder: 'Selecione um período',
    disabled: false,
  }
);

const emit = defineEmits<{
  'update:startDate': [date: Date | null];
  'update:endDate': [date: Date | null];
  change: [startDate: Date | null, endDate: Date | null];
}>();

const isOpen = ref(false);
const localStartDate = ref<Date | null>(props.startDate || null);
const localEndDate = ref<Date | null>(props.endDate || null);
const inputValue = ref('');
const inputEl = ref<HTMLInputElement | null>(null);

const displayValue = computed(() => {
  if (!localStartDate.value && !localEndDate.value) return '';

  if (localStartDate.value && !localEndDate.value) {
    return format(localStartDate.value, props.format, { locale: ptBR });
  }

  if (localStartDate.value && localEndDate.value) {
    return `${format(localStartDate.value, props.format, { locale: ptBR })} - ${format(localEndDate.value, props.format, { locale: ptBR })}`;
  }

  return '';
});

watch(displayValue, (newValue) => {
  inputValue.value = newValue;
});

watch(
  () => props.startDate,
  (newValue) => {
    localStartDate.value = newValue;
  }
);

watch(
  () => props.endDate,
  (newValue) => {
    localEndDate.value = newValue;
  }
);

const toggleCalendar = () => {
  if (!props.disabled) {
    isOpen.value = !isOpen.value;
  }
};

const closeCalendar = () => {
  isOpen.value = false;
};

const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (inputEl.value && !inputEl.value.contains(target) && isOpen.value) {
    closeCalendar();
  }
};

const selectDate = (date: Date) => {
  if (!localStartDate.value || (localStartDate.value && localEndDate.value)) {
    // Começar um novo intervalo
    localStartDate.value = date;
    localEndDate.value = null;
    emit('update:startDate', date);
    emit('update:endDate', null);
    emit('change', date, null);
  } else {
    // Completar o intervalo
    if (isBefore(date, localStartDate.value)) {
      // Se a data selecionada for anterior à data inicial, inverte
      localEndDate.value = localStartDate.value;
      localStartDate.value = date;
      emit('update:startDate', date);
      emit('update:endDate', localEndDate.value);
    } else {
      localEndDate.value = date;
      emit('update:startDate', localStartDate.value);
      emit('update:endDate', date);
    }
    emit('change', localStartDate.value, localEndDate.value);
    closeCalendar();
  }
};

const clearDates = () => {
  localStartDate.value = null;
  localEndDate.value = null;
  emit('update:startDate', null);
  emit('update:endDate', null);
  emit('change', null, null);
  closeCalendar();
};

// Adicionar event listener para detectar cliques fora do componente
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<template>
  <div class="relative" :class="props.class">
    <div
      ref="inputEl"
      class="flex items-center w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
      :class="{ 'cursor-pointer': !disabled, 'opacity-50': disabled }"
      @click="toggleCalendar"
    >
      <input
        type="text"
        :value="displayValue"
        :placeholder="placeholder"
        class="flex-1 bg-transparent outline-none"
        readonly
        :disabled="disabled"
      />
      <Calendar class="ml-2 h-4 w-4 opacity-50" />
    </div>

    <div
      v-if="isOpen"
      class="absolute z-50 mt-2 w-auto rounded-md border bg-popover p-4 shadow-md"
    >
      <div class="space-y-4">
        <div class="grid gap-2">
          <div class="flex items-center justify-between">
            <div class="text-sm font-medium">
              Selecione o intervalo de datas
            </div>
            <Button variant="ghost" size="sm" @click="clearDates">
              Limpar
            </Button>
          </div>

          <!-- Aqui você pode integrar um componente de calendário para seleção de datas -->
          <!-- Esta é uma implementação simplificada para demonstração -->
          <div class="grid grid-cols-7 gap-1">
            <!-- Cabeçalho dos dias da semana -->
            <div
              v-for="day in ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']"
              :key="day"
              class="text-center text-xs font-medium text-muted-foreground"
            >
              {{ day }}
            </div>

            <!-- Dias do mês (simplificado) -->
            <!-- Em uma implementação real, você usaria uma biblioteca como date-fns para gerar os dias do mês atual -->
            <button
              v-for="day in 31"
              :key="day"
              class="aspect-square p-2 text-center text-sm rounded-md hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground focus:outline-none"
              :class="{
                'bg-primary text-primary-foreground':
                  (localStartDate &&
                    day === new Date(localStartDate).getDate()) ||
                  (localEndDate && day === new Date(localEndDate).getDate()),
                'bg-accent/50':
                  localStartDate &&
                  localEndDate &&
                  day > new Date(localStartDate).getDate() &&
                  day < new Date(localEndDate).getDate(),
              }"
              @click="selectDate(new Date(2025, 4, day))"
            >
              {{ day }}
            </button>
          </div>
        </div>

        <div class="flex items-center justify-between pt-2">
          <div class="text-sm text-muted-foreground">
            <span v-if="localStartDate && localEndDate">
              {{ format(localStartDate, 'PPP', { locale: ptBR }) }} -
              {{ format(localEndDate, 'PPP', { locale: ptBR }) }}
            </span>
            <span v-else-if="localStartDate">
              Início: {{ format(localStartDate, 'PPP', { locale: ptBR }) }}
            </span>
            <span v-else> Nenhuma data selecionada </span>
          </div>
          <Button size="sm" @click="closeCalendar"> Aplicar </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Estilos específicos para o componente, se necessário */
</style>
