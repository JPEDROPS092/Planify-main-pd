---
sidebar_position: 1
---

# Módulo de Projetos

O Módulo de Projetos é o coração do Planify, permitindo criar, gerenciar e monitorar projetos de P&D de forma eficiente. Esta seção explica todas as funcionalidades disponíveis para o gerenciamento de projetos.

## Visão Geral de Projetos

A página de Projetos apresenta uma visão consolidada de todos os projetos aos quais você tem acesso:

<!-- ![Lista de Projetos](/img/docs/projects-list.png) -->

### Elementos da Página de Projetos

- **Barra de Pesquisa**: Busque projetos por nome, código ou descrição
- **Filtros**: Filtre projetos por status, equipe, data ou outros critérios
- **Botão de Novo Projeto**: Inicie a criação de um novo projeto
- **Lista de Projetos**: Exibe os projetos com informações resumidas
- **Opções de Visualização**: Alterne entre visualização em lista, cartões ou Gantt

## Criando um Novo Projeto

### Passo a Passo para Criação

1. Na página de Projetos, clique no botão "+ Novo Projeto"
2. Preencha o formulário de criação:

<!-- ![Formulário de Novo Projeto](/img/docs/new-project-form.png) -->

3. **Informações Básicas**:
   - **Nome do Projeto**: Um título descritivo e único
   - **Código do Projeto**: Identificador único (gerado automaticamente, mas pode ser personalizado)
   - **Descrição**: Detalhes sobre o objetivo e escopo do projeto
   - **Data de Início**: Quando o projeto começa
   - **Data de Término Prevista**: Prazo estimado para conclusão
   - **Status Inicial**: Geralmente "Em Planejamento" ou "Não Iniciado"

4. **Configurações Avançadas**:
   - **Metodologia**: Ágil, Cascata, Híbrida, etc.
   - **Prioridade**: Baixa, Média, Alta, Crítica
   - **Orçamento Previsto**: Valor estimado para o projeto
   - **Cliente/Patrocinador**: Entidade que solicitou ou financia o projeto

5. **Equipe do Projeto**:
   - **Gerente do Projeto**: Responsável principal
   - **Membros da Equipe**: Selecione usuários para a equipe inicial
   - **Equipes Associadas**: Vincule equipes existentes ao projeto

6. Clique em "Criar Projeto"

:::tip Dica
Você pode criar um projeto a partir de um template pré-definido selecionando a opção "Usar Template" no topo do formulário.
:::

## Detalhes do Projeto

Ao clicar em um projeto na lista, você acessa a página de detalhes do projeto:

<!-- ![Detalhes do Projeto](/img/docs/project-details.png) -->

### Abas de Navegação

A página de detalhes do projeto é organizada em abas:

#### Visão Geral

Apresenta um resumo do projeto, incluindo:
- Informações básicas (nome, código, datas)
- Progresso geral (percentual concluído)
- Gráficos e indicadores de desempenho
- Próximos marcos (milestones)
- Atividades recentes

#### Tarefas

Lista todas as tarefas do projeto com opções para:
- Adicionar novas tarefas
- Filtrar por responsável, status, prioridade
- Agrupar por diferentes critérios
- Exportar a lista de tarefas

#### Kanban

Visualização em quadro Kanban das tarefas do projeto:
- Colunas representando os diferentes status
- Arraste e solte para atualizar o status
- Filtros e agrupamentos personalizáveis
- Adição rápida de tarefas em cada coluna

#### Equipe

Gerenciamento da equipe do projeto:
- Lista de membros com papéis
- Adição/remoção de membros
- Atribuição de responsabilidades
- Visualização de carga de trabalho

#### Cronograma

Visualização do cronograma do projeto:
- Gráfico de Gantt interativo
- Marcos (milestones) importantes
- Dependências entre tarefas
- Caminho crítico

#### Riscos

Gerenciamento de riscos do projeto:
- Registro de riscos identificados
- Matriz de probabilidade e impacto
- Planos de mitigação
- Histórico de tratamento

#### Custos

Controle financeiro do projeto:
- Orçamento planejado vs. realizado
- Categorias de despesas
- Gráficos de distribuição de custos
- Previsões e alertas

#### Documentos

Gerenciamento de documentação:
- Upload de arquivos
- Organização em pastas
- Controle de versões
- Visualização integrada

#### Comunicações

Comunicação da equipe:
- Chat do projeto
- Histórico de mensagens
- Menções e notificações
- Compartilhamento de arquivos

## Gerenciando Projetos

### Editando um Projeto

Para editar as informações de um projeto:

1. Na página de detalhes do projeto, clique no botão "Editar Projeto"
2. Modifique as informações necessárias
3. Clique em "Salvar Alterações"

Todas as alterações são registradas no histórico do projeto.

### Alterando o Status do Projeto

Para atualizar o status de um projeto:

1. Na página de detalhes, localize o campo de status
2. Clique no status atual para abrir o menu suspenso
3. Selecione o novo status:
   - **Em Planejamento**: Fase inicial de definição
   - **Em Andamento**: Execução ativa
   - **Em Pausa**: Temporariamente interrompido
   - **Concluído**: Finalizado com sucesso
   - **Cancelado**: Encerrado antes da conclusão
4. Adicione um comentário explicando a mudança (opcional)
5. Clique em "Atualizar Status"

### Arquivando um Projeto

Projetos concluídos ou cancelados podem ser arquivados:

1. Na página de detalhes, clique no menu de opções (⋮)
2. Selecione "Arquivar Projeto"
3. Confirme a ação

Projetos arquivados não aparecem na lista principal, mas podem ser acessados através do filtro "Arquivados".

### Excluindo um Projeto

:::caution Atenção
A exclusão de projetos é uma ação irreversível e requer permissões especiais.
:::

Para excluir um projeto:

1. Na página de detalhes, clique no menu de opções (⋮)
2. Selecione "Excluir Projeto"
3. Digite o nome do projeto para confirmar
4. Clique em "Excluir Permanentemente"

## Recursos Avançados

### Templates de Projeto

O Planify permite criar e utilizar templates para padronizar projetos:

#### Criando um Template

1. Crie um projeto com a estrutura desejada (tarefas, equipe, etc.)
2. Na página de detalhes, clique no menu de opções (⋮)
3. Selecione "Salvar como Template"
4. Dê um nome e descrição ao template
5. Selecione quais elementos incluir (tarefas, riscos, documentos, etc.)
6. Clique em "Salvar Template"

#### Usando um Template

1. Ao criar um novo projeto, clique em "Usar Template"
2. Selecione o template desejado na lista
3. Personalize as informações específicas do projeto
4. Clique em "Criar Projeto"

### Duplicando Projetos

Para criar um novo projeto baseado em um existente:

1. Na página de detalhes, clique no menu de opções (⋮)
2. Selecione "Duplicar Projeto"
3. Ajuste as informações do novo projeto
4. Selecione quais elementos duplicar
5. Clique em "Criar Cópia"

### Relatórios de Projeto

O Planify oferece relatórios detalhados para análise de projetos:

#### Gerando Relatórios

1. Na página de detalhes, clique na aba "Relatórios"
2. Selecione o tipo de relatório:
   - **Resumo Executivo**: Visão geral para stakeholders
   - **Progresso Detalhado**: Análise completa do andamento
   - **Desempenho da Equipe**: Métricas por membro
   - **Análise de Riscos**: Situação dos riscos identificados
   - **Relatório Financeiro**: Análise de custos e orçamento
3. Configure os parâmetros do relatório
4. Clique em "Gerar Relatório"

#### Exportando Relatórios

Os relatórios podem ser exportados em diferentes formatos:
- PDF (para apresentação formal)
- Excel (para análise adicional)
- PowerPoint (para apresentações)
- HTML (para compartilhamento web)

### Integrações

O módulo de Projetos se integra com outras ferramentas:

- **Calendário**: Eventos e prazos são sincronizados
- **Email**: Notificações automáticas de atualizações
- **Ferramentas Externas**: Integração com MS Project, Jira, etc. (se configurado)

## Melhores Práticas

### Organização de Projetos

- Use uma nomenclatura padronizada para facilitar a busca
- Mantenha a descrição clara e objetiva
- Defina marcos (milestones) para acompanhar o progresso
- Estabeleça KPIs mensuráveis para avaliar o sucesso

### Gerenciamento Eficiente

- Atualize regularmente o status das tarefas
- Realize reuniões periódicas de acompanhamento
- Documente decisões importantes
- Mantenha o registro de riscos atualizado
- Comunique mudanças de escopo a todos os envolvidos

## Próximos Passos

Agora que você conhece o Módulo de Projetos, explore o [Módulo de Tarefas](/docs/user-guide/modules/tasks) para aprender como gerenciar as atividades dentro dos seus projetos.
