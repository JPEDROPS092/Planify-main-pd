#!/bin/bash

# Script para resolver problemas de componentes duplicados no Planify
echo "Iniciando correção de componentes duplicados..."

# 1. Corrigir o problema do TaskForm
echo "Corrigindo TaskForm..."
cat > /home/jpcode092/projects/Planify-main-pd/frontend/components/TaskForm.vue << 'EOL'
<template>
  <!-- Este componente é um wrapper para o componente em /components/task/TaskForm.vue -->
  <task-form
    v-bind="$attrs"
    :task="task"
    :project-id="projectId"
    :loading="loading"
    @submit="$emit('submit', $event)"
    @cancel="$emit('cancel')"
  />
</template>

<script setup lang="ts">
// Este componente é um wrapper para o componente TaskForm em /components/task/TaskForm.vue
// Mantido para compatibilidade com código existente
import TaskForm from './task/TaskForm.vue'
import type { Tarefa } from '~/services/api/types'

const props = defineProps({
  task: {
    type: Object as () => Tarefa | null,
    default: null
  },
  projectId: {
    type: Number,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['submit', 'cancel'])
</script>
EOL

# 2. Corrigir o problema do UiButton
echo "Corrigindo UiButton..."
mkdir -p /home/jpcode092/projects/Planify-main-pd/frontend/components/ui/button-backup
mv /home/jpcode092/projects/Planify-main-pd/frontend/components/ui/Button.vue /home/jpcode092/projects/Planify-main-pd/frontend/components/ui/button-backup/

# 3. Corrigir o problema do UiCard
echo "Corrigindo UiCard..."
mkdir -p /home/jpcode092/projects/Planify-main-pd/frontend/components/ui/card-backup
mv /home/jpcode092/projects/Planify-main-pd/frontend/components/ui/Card.vue /home/jpcode092/projects/Planify-main-pd/frontend/components/ui/card-backup/

# 4. Corrigir o problema do UiAvatar
echo "Corrigindo UiAvatar..."
# Não é necessário mover, pois o problema é entre index.ts e Avatar.vue na mesma pasta

# 5. Corrigir o problema do UiBadge
echo "Corrigindo UiBadge..."
# Não é necessário mover, pois o problema é entre index.ts e Badge.vue na mesma pasta

# 6. Corrigir problemas de importação
echo "Corrigindo importações incorretas..."
find /home/jpcode092/projects/Planify-main-pd/frontend -type f -name "*.vue" -exec sed -i 's/import { useUserService } from '\''~\/services\/api\/auth'\''/import { useUserService } from '\''~\/services\/api\/userService'\''/g' {} \;

# 7. Limpar diretórios de API duplicados
echo "Limpando diretórios de API duplicados..."
rm -rf /home/jpcode092/projects/Planify-main-pd/frontend/services/api\ copy

echo "Correções concluídas!"
