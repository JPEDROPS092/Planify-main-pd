# Componentes UI do Planify

Este diretório contém todos os componentes de UI padronizados do Planify, organizados para facilitar a reutilização e manutenção.

## Componentes Básicos (Padronizados)

### Avatar

Componente para exibição de avatares de usuários, com suporte para imagens e fallback.

- Variantes de tamanho: `sm`, `base`, `lg`
- Variantes de forma: `circle`, `square`
- [Documentação detalhada](/components/ui/avatar/README.md)

### Badge

Componente para exibição de etiquetas e indicadores de status.

- Variantes: `default`, `secondary`, `outline`, `destructive`, `success`
- [Documentação detalhada](/components/ui/badge/README.md)

### Button

Componente para ações e interações do usuário.

- Variantes de estilo: `default`, `secondary`, `outline`, `ghost`, `link`, `destructive`, `success`
- Variantes de tamanho: `default`, `sm`, `lg`, `icon`
- [Documentação detalhada](/components/ui/button/README.md)

### Card

Componente para agrupamento de conteúdo relacionado.

- Subcomponentes: `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter`
- [Documentação detalhada](/components/ui/card/README.md)

## Componentes Avançados

### ActivityFeed

Componente para exibição de atividades e atualizações recentes.

```vue
<script setup>
import { ActivityFeed } from '@/components/ui/activity-feed';

const activities = [
  {
    id: 1,
    user: { id: 1, name: 'João Silva', initials: 'JS' },
    action: 'criou a tarefa',
    target: { type: 'task', id: 1, name: 'Implementar dashboard' },
    timestamp: new Date(),
  },
  // Mais atividades...
];
</script>

<template>
  <ActivityFeed :activities="activities" />
</template>
```

### Breadcrumbs

Componente para navegação hierárquica de páginas.

```vue
<script setup>
import { Breadcrumbs } from '@/components/ui/breadcrumbs';
import { Home, FileText } from 'lucide-vue-next';

const items = [
  { label: 'Projetos', href: '/projetos', icon: Home },
  { label: 'Projeto XYZ', href: '/projetos/xyz', icon: FileText },
  { label: 'Tarefas', active: true },
];
</script>

<template>
  <Breadcrumbs :items="items" />
</template>
```

### DateRangePicker

Componente para seleção de intervalo de datas.

```vue
<script setup>
import { ref } from 'vue';
import { DateRangePicker } from '@/components/ui/date-range-picker';

const startDate = ref(new Date());
const endDate = ref(null);
</script>

<template>
  <DateRangePicker
    v-model:startDate="startDate"
    v-model:endDate="endDate"
    placeholder="Selecione o período"
  />
</template>
```

### FileUploader

Componente para upload de arquivos com suporte a drag-and-drop.

```vue
<script setup>
import { FileUploader } from '@/components/ui/file-uploader';

const handleFilesSelected = (files) => {
  console.log('Arquivos selecionados:', files);
};
</script>

<template>
  <FileUploader
    accept=".pdf,.docx,image/*"
    :multiple="true"
    @files-selected="handleFilesSelected"
  />
</template>
```

### MetricsCard

Componente para exibição de métricas e estatísticas em dashboards.

```vue
<script setup>
import { MetricsCard } from '@/components/ui/metrics-card';
import { Users } from 'lucide-vue-next';

const userMetric = {
  title: 'Usuários Ativos',
  value: 1250,
  description: 'Total de usuários ativos no último mês',
  icon: Users,
  trend: {
    value: '12%',
    direction: 'up',
    isPositive: true,
  },
};
</script>

<template>
  <MetricsCard v-bind="userMetric" />
</template>
```

### Pagination

Componente para navegação em listas e tabelas com muitos itens.

```vue
<script setup>
import { ref } from 'vue';
import { Pagination } from '@/components/ui/pagination';

const currentPage = ref(1);
const totalPages = 10;
const totalItems = 95;
const itemsPerPage = ref(10);
</script>

<template>
  <Pagination
    v-model:currentPage="currentPage"
    v-model:itemsPerPage="itemsPerPage"
    :totalPages="totalPages"
    :totalItems="totalItems"
    :showItemsPerPage="true"
  />
</template>
```

### RichTextEditor

Editor de texto rico para o Planify.

```vue
<script setup>
import { ref } from 'vue';
import { RichTextEditor } from '@/components/ui/rich-text-editor';

const content = ref('<p>Conteúdo inicial do editor</p>');
</script>

<template>
  <RichTextEditor v-model="content" placeholder="Comece a digitar..." />
</template>
```

### TabGroup

Componente para organização de conteúdo em abas.

```vue
<script setup>
import { ref } from 'vue';
import { TabGroup } from '@/components/ui/tab-group';
import { FileText, CheckSquare, Users } from 'lucide-vue-next';

const activeTab = ref('overview');
const tabs = [
  { id: 'overview', label: 'Visão Geral', icon: FileText },
  { id: 'tasks', label: 'Tarefas', icon: CheckSquare },
  { id: 'team', label: 'Equipe', icon: Users },
];
</script>

<template>
  <TabGroup v-model="activeTab" :tabs="tabs" variant="underline">
    <template #content-overview>
      <p>Conteúdo da aba Visão Geral</p>
    </template>
    <template #content-tasks>
      <p>Conteúdo da aba Tarefas</p>
    </template>
    <template #content-team>
      <p>Conteúdo da aba Equipe</p>
    </template>
  </TabGroup>
</template>
```

### Timeline

Componente para exibição de eventos em ordem cronológica.

```vue
<script setup>
import { Timeline } from '@/components/ui/timeline';

const events = [
  {
    id: 1,
    title: 'Projeto iniciado',
    description: 'O projeto foi criado e a equipe foi definida',
    date: new Date('2025-01-15'),
    status: 'completed',
  },
  {
    id: 2,
    title: 'Fase de planejamento',
    description: 'Definição de requisitos e cronograma',
    date: new Date('2025-02-01'),
    status: 'completed',
  },
  {
    id: 3,
    title: 'Desenvolvimento',
    description: 'Implementação das funcionalidades principais',
    date: new Date('2025-03-15'),
    status: 'pending',
  },
];
</script>

<template>
  <Timeline :items="events" />
</template>
```

## Acessibilidade

Todos os componentes foram desenvolvidos com foco em acessibilidade, seguindo as melhores práticas:

- Uso de atributos ARIA apropriados
- Suporte para navegação por teclado
- Contraste adequado de cores
- Textos alternativos para imagens
- Tamanhos mínimos para elementos interativos

## Utilização

Para utilizar estes componentes, importe-os diretamente dos arquivos index.ts de cada pasta:

```vue
<script setup>
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
</script>
```

## Utilitários

Os componentes utilizam os seguintes utilitários:

- `cn`: Função para composição de classes CSS (baseada em clsx/tailwind-merge)
- `cva`: Class Variance Authority para definição de variantes tipadas
