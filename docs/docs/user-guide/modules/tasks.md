---
sidebar_position: 2
---

# Módulo de Tarefas

O Módulo de Tarefas do Planify permite gerenciar todas as atividades necessárias para a execução bem-sucedida dos seus projetos. Esta seção explica como criar, organizar e acompanhar tarefas de forma eficiente.

## Visão Geral de Tarefas

A página principal de Tarefas apresenta uma visão consolidada de todas as suas tarefas, independentemente do projeto:

<!-- ![Lista de Tarefas](/img/docs/tasks-list.png) -->

### Elementos da Página de Tarefas

- **Barra de Pesquisa**: Busque tarefas por título, descrição ou ID
- **Filtros Avançados**: Filtre por projeto, status, prioridade, responsável e datas
- **Botão de Nova Tarefa**: Inicie a criação de uma nova tarefa
- **Lista de Tarefas**: Exibe as tarefas com informações resumidas
- **Opções de Visualização**: Alterne entre lista, quadro Kanban ou calendário

## Criando uma Nova Tarefa

### Passo a Passo para Criação

1. Na página de Tarefas ou dentro de um projeto específico, clique no botão "+ Nova Tarefa"
2. Preencha o formulário de criação:

<!-- ![Formulário de Nova Tarefa](/img/docs/new-task-form.png) -->

3. **Informações Básicas**:
   - **Título**: Nome descritivo da tarefa
   - **Descrição**: Detalhamento do que deve ser feito
   - **Projeto**: Selecione o projeto ao qual a tarefa pertence
   - **Sprint**: Associe a tarefa a um sprint (opcional)
   - **Responsável**: Quem executará a tarefa
   - **Observadores**: Pessoas que receberão atualizações sobre a tarefa

4. **Detalhes da Tarefa**:
   - **Status**: Estado atual (Pendente, Em Andamento, Concluída, etc.)
   - **Prioridade**: Baixa, Média, Alta, Crítica
   - **Tipo**: Bug, Feature, Documentação, etc.
   - **Estimativa**: Tempo estimado para conclusão
   - **Data de Início**: Quando a tarefa deve começar
   - **Data de Término**: Prazo para conclusão

5. **Opções Avançadas**:
   - **Tarefas Relacionadas**: Vincule a outras tarefas
   - **Dependências**: Defina tarefas que devem ser concluídas antes
   - **Tags**: Adicione etiquetas para categorização
   - **Anexos**: Adicione arquivos relevantes

6. Clique em "Criar Tarefa"

:::tip Dica
Use a função de criação rápida pressionando "Q" em qualquer tela ou clicando no botão "+" flutuante para adicionar tarefas com informações mínimas e complementá-las depois.
:::

## Detalhes da Tarefa

Ao clicar em uma tarefa na lista, você acessa a página de detalhes:

<!-- ![Detalhes da Tarefa](/img/docs/task-details.png) -->

### Seções da Página de Detalhes

#### Informações Principais

Exibe os dados essenciais da tarefa:
- Título e descrição
- Status e prioridade
- Responsável e observadores
- Datas e prazos
- Progresso (percentual concluído)

#### Subtarefas

Permite dividir a tarefa em partes menores:
- Lista de subtarefas com status
- Opção para adicionar novas subtarefas
- Marcação de conclusão diretamente na lista

#### Comentários

Facilita a comunicação sobre a tarefa:
- Histórico de comentários em ordem cronológica
- Editor de texto rico para formatação
- Suporte a menções (@usuário)
- Anexo de arquivos nos comentários

#### Histórico

Registra todas as alterações na tarefa:
- Mudanças de status, prioridade, responsável
- Atualizações de datas e estimativas
- Adição/remoção de observadores
- Data, hora e autor de cada alteração

#### Anexos

Gerencia os arquivos relacionados à tarefa:
- Lista de arquivos anexados
- Visualização integrada de documentos
- Download de arquivos
- Controle de versões

#### Tempo Registrado

Acompanha o tempo dedicado à tarefa:
- Registro manual de horas trabalhadas
- Cronômetro integrado para registro em tempo real
- Histórico de registros por usuário
- Comparação entre tempo estimado e realizado

## Gerenciando Tarefas

### Editando uma Tarefa

Para modificar uma tarefa existente:

1. Na página de detalhes, clique no botão "Editar"
2. Atualize as informações necessárias
3. Clique em "Salvar Alterações"

Todas as modificações são registradas no histórico da tarefa.

### Atualizando o Status

Para alterar o status de uma tarefa:

1. Na lista de tarefas, clique no status atual para abrir o menu suspenso
2. Selecione o novo status
3. Opcionalmente, adicione um comentário sobre a mudança
4. Clique em "Atualizar"

Alternativamente, na visualização Kanban, arraste a tarefa para a coluna correspondente ao novo status.

### Atribuindo Responsáveis

Para designar ou alterar o responsável:

1. Na página de detalhes, clique no campo "Responsável"
2. Pesquise e selecione o usuário na lista
3. Clique em "Atribuir"

O novo responsável receberá uma notificação sobre a atribuição.

### Definindo Prioridade

Para ajustar a prioridade de uma tarefa:

1. Na página de detalhes, clique no campo "Prioridade"
2. Selecione o nível apropriado:
   - **Baixa**: Pode aguardar, sem impacto significativo
   - **Média**: Importante, mas não urgente
   - **Alta**: Urgente, com impacto considerável
   - **Crítica**: Requer atenção imediata, bloqueia o progresso

### Gerenciando Dependências

Para estabelecer relações entre tarefas:

1. Na página de detalhes, vá para a seção "Dependências"
2. Clique em "Adicionar Dependência"
3. Pesquise e selecione a tarefa relacionada
4. Defina o tipo de dependência:
   - **Bloqueia**: Esta tarefa bloqueia o início da selecionada
   - **Bloqueada por**: Esta tarefa só pode iniciar após a selecionada
   - **Relacionada**: Conexão informativa, sem bloqueio
5. Clique em "Salvar"

### Adicionando Subtarefas

Para dividir uma tarefa em partes menores:

1. Na página de detalhes, vá para a seção "Subtarefas"
2. Clique em "Adicionar Subtarefa"
3. Digite o título da subtarefa
4. Opcionalmente, adicione detalhes como responsável e data
5. Clique em "Adicionar"

As subtarefas concluídas contribuem para o percentual de progresso da tarefa principal.

## Visualizações de Tarefas

O Planify oferece diferentes formas de visualizar suas tarefas:

### Lista

A visualização padrão, ideal para ver muitas tarefas com detalhes:
- Colunas personalizáveis
- Ordenação por qualquer campo
- Agrupamento por projeto, status, responsável, etc.
- Exportação para Excel ou CSV

### Quadro Kanban

Visualização baseada em colunas, perfeita para acompanhar o fluxo de trabalho:
- Colunas representando os status
- Arraste e solte para atualizar
- Filtros por projeto, responsável, etc.
- Limite de tarefas por coluna (opcional)

<!-- ![Visualização Kanban](/img/docs/tasks-kanban.png) -->

### Calendário

Visualização temporal das tarefas:
- Tarefas organizadas por data
- Visualização diária, semanal ou mensal
- Identificação visual de conflitos
- Arraste e solte para reagendar

<!-- ![Visualização Calendário](/img/docs/tasks-calendar.png) -->

### Gráfico de Gantt

Visualização de cronograma e dependências:
- Linha do tempo visual
- Dependências representadas por linhas
- Caminho crítico destacado
- Ajuste de datas arrastando as barras

<!-- ![Visualização Gantt](/img/docs/tasks-gantt.png) -->

## Recursos Avançados

### Filtros Salvos

Crie e salve filtros personalizados para acessar rapidamente conjuntos específicos de tarefas:

1. Configure os filtros desejados
2. Clique em "Salvar Filtro"
3. Dê um nome ao filtro
4. Escolha se deseja compartilhá-lo com a equipe
5. Acesse seus filtros salvos no menu lateral

### Automações

Configure regras para automatizar ações em tarefas:

#### Exemplos de Automações

- **Notificações**: Enviar alerta quando uma tarefa estiver próxima do prazo
- **Atribuições**: Atribuir automaticamente certos tipos de tarefas a usuários específicos
- **Status**: Mudar o status quando todas as subtarefas forem concluídas
- **Prioridade**: Aumentar a prioridade quando o prazo estiver próximo

#### Criando uma Automação

1. Acesse "Configurações" > "Automações"
2. Clique em "Nova Automação"
3. Defina o gatilho (quando a automação será executada)
4. Configure as condições (critérios para execução)
5. Especifique as ações a serem realizadas
6. Ative a automação

### Importação em Massa

Para adicionar múltiplas tarefas de uma vez:

1. Na página de Tarefas, clique em "Importar"
2. Baixe o modelo de planilha
3. Preencha os dados das tarefas
4. Faça upload da planilha preenchida
5. Revise as tarefas a serem importadas
6. Clique em "Importar Tarefas"

### Exportação de Tarefas

Para exportar suas tarefas:

1. Configure os filtros para selecionar as tarefas desejadas
2. Clique em "Exportar"
3. Escolha o formato (Excel, CSV, PDF)
4. Selecione os campos a incluir
5. Clique em "Exportar"

## Integrações

O módulo de Tarefas se integra com outros componentes do Planify:

- **Projetos**: Tarefas são organizadas por projeto
- **Equipes**: Atribuição baseada em membros da equipe
- **Calendário**: Tarefas aparecem no calendário geral
- **Documentos**: Anexos são gerenciados pelo módulo de Documentos
- **Comunicações**: Notificações sobre atualizações de tarefas

## Melhores Práticas

### Organização Eficiente

- Use títulos claros e descritivos
- Mantenha descrições objetivas com passos específicos
- Divida tarefas grandes em subtarefas gerenciáveis
- Estabeleça dependências apenas quando realmente necessárias
- Use tags para categorizar e facilitar a busca

### Gerenciamento de Tempo

- Defina estimativas realistas
- Registre o tempo trabalhado regularmente
- Atualize o status assim que houver mudanças
- Configure lembretes para tarefas importantes
- Revise periodicamente tarefas atrasadas

### Colaboração

- Adicione comentários contextualizados
- Mencione (@usuário) pessoas específicas quando necessário
- Anexe documentos relevantes diretamente na tarefa
- Mantenha os observadores atualizados sobre mudanças importantes
- Use subtarefas para dividir o trabalho entre a equipe

## Próximos Passos

Agora que você conhece o Módulo de Tarefas, explore o [Módulo de Equipes](/docs/user-guide/modules/teams) para aprender como gerenciar os membros e papéis dentro dos seus projetos.
