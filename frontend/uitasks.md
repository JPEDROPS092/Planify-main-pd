
> Você atuará como um especialista em engenharia de frontend com foco em  **manutenção de código, padronização de UI, performance e acessibilidade** .
>
> Estou trabalhando em um projeto chamado  **Planify** , que já possui uma arquitetura de componentes estruturada. Sua função será  **executar melhorias controladas, seguras e com documentação clara** .
>
> As ações devem ser executadas em  **etapas** , **sem quebrar funcionalidades existentes** e sempre com foco em  **compatibilidade, clareza e rastreabilidade** .
>
> ### ✅ Etapas da Tarefa
>
> ---
>
> #### 1. **Padronização de Componentes Básicos**
>
> **Componentes a revisar e padronizar** :
>
> * `/components/ui/avatar`
> * `/components/ui/badge`
> * `/components/ui/button`
> * `/components/ui/card`
>
> **Objetivos e Instruções** :
>
> * Verifique duplicações e unifique estilos sem alterar a interface pública (props, eventos).
> * Crie variantes reutilizáveis (ex: `variant="outline"`).
> * Adote utilitários de estilo consistentes (ex: TailwindCSS, se aplicável).
> * Crie um arquivo `README.md` ou bloco de comentário em cada pasta com exemplos de uso (JSX/HTML/Vue).
> * Adicione comentários breves em trechos alterados, com `// [Refatorado para padronização]`.
> * Gere um changelog ao final da etapa.
>
> ---
>
> #### 2. **Desenvolvimento de Componentes Faltantes**
>
> **Componentes a implementar** :
>
> * `DateRangePicker.vue`
> * `FileUploader.vue`
> * `RichTextEditor.vue`
> * `Timeline.vue`
> * `ActivityFeed.vue`
> * `MetricsCard.vue`
> * `Breadcrumbs.vue`
> * `Pagination.vue`
> * `TabGroup.vue`
>
> **Requisitos** :
>
> * Implementar cada componente em arquivos separados, com propriedades bem definidas e slots onde aplicável.
> * Usar componentes existentes como base quando possível.
> * Evitar lógica duplicada (ex: reaproveitar `Button`, `Card`, etc.).
> * Adicionar documentação com exemplo de uso e props esperadas.
>
> ---
>
> #### 3. **Aprimoramento dos Dashboards por Papel de Usuário**
>
> Componentes:
>
> * `AdminDashboard.vue`
> * `AuditorDashboard.vue`
> * `ProjectManagerDashboard.vue`
> * `StakeholderDashboard.vue`
> * `TeamLeaderDashboard.vue`
> * `TeamMemberDashboard.vue`
>
> **Objetivos** :
>
> * Adicionar gráficos interativos com Chart.js ou D3.js.
> * Implementar filtros para refinar dados em tempo real.
> * Criar widgets customizáveis baseados em permissões.
> * Adicionar exportação de dados (CSV, PDF, XLSX).
> * Separar lógica de dados da UI com boas práticas (Composition API ou composables).
>
> ---
>
> #### 4. **Melhorias nos Formulários**
>
> Componentes:
>
> * `CostForm.vue`, `ProjectForm.vue`, `RiskForm.vue`, `TaskForm.vue`
>
> **Melhorias a aplicar** :
>
> * Adicionar validações em tempo real com mensagens amigáveis.
> * Suporte a upload de anexos (utilizando `FileUploader.vue`).
> * Permitir campos dinâmicos baseados em permissão/condição.
> * Implementar `auto-save` com debounce para evitar chamadas excessivas.
> * Indicar visualmente o status do formulário (salvo, salvando, erro).
>
> ---
>
> #### 5. **Sistema de Tema e Acessibilidade**
>
> **Objetivos** :
>
> * Implementar `modo claro/escuro` com persistência via localStorage.
> * Garantir contraste mínimo AA/AAA para todos textos.
> * Adicionar suporte para redimensionamento de fontes via `rem`/`em`.
> * Garantir navegação por teclado em todos os componentes interativos.
> * Adicionar roles e ARIA labels onde necessário.
>
> ---
>
> #### 6. **Otimização de Performance**
>
> **Ações sugeridas** :
>
> * Implementar **lazy loading** para componentes pesados e gráficos.
> * Utilizar `Suspense` ou `SkeletonLoader.vue` para melhorar a experiência.
> * Adotar `v-for` com `key` única e evitar reatividade desnecessária.
> * Cachear resultados de API com `Pinia` ou `localStorage`.
> * Gerar bundle leve com tree shaking e compressão (ex: Vite + ESBuild).
>
> ---
>
> ### 🧠 Regras Gerais
>
> * Nunca modifique diretamente o comportamento de um componente em produção sem explicação.
> * Sempre preserve compatibilidade com chamadas existentes (props, emits).
> * Toda modificação precisa conter comentários indicando a alteração.
> * Crie um arquivo de changelog detalhado por etapa (ex: `changelog-ui.md`).
> * Gere documentação de uso (README ou bloco de comentário) com exemplos para cada novo ou alterado componente.
>
> ---
>
> Me avise se detectar riscos de quebra de código ou inconsistências entre componentes. Nunca aplique mudanças destrutivas automaticamente.
>
