# Backlog do Backend - Planify

## 📋 Visão Geral do Sistema

O Planify é um sistema de gerenciamento de projetos desenvolvido em Django com Django REST Framework. O sistema permite o gerenciamento completo de projetos, tarefas, equipes, riscos, custos, documentos e comunicações, com um sistema robusto de autenticação e controle de permissões.

## 🏗️ Estrutura Atual do Projeto

### Módulos Implementados

#### 🔐 Usuários e Autenticação
- Sistema completo de autenticação baseado em JWT
- Modelo de usuário personalizado com papéis (ADMIN, PROJECT_MANAGER, TEAM_LEADER, etc.)
- Sistema de perfis de acesso e permissões
- Gerenciamento de senhas com histórico e políticas de segurança
- Bloqueio de conta após tentativas de login malsucedidas
- Configurações de preferências de usuário (tema, notificações)

#### 📊 Projetos
- Gerenciamento de projetos com status, prioridade e cronograma
- Sistema de sprints para metodologias ágeis
- Controle de membros do projeto com papéis específicos
- Histórico de alterações de status do projeto

#### ✅ Tarefas
- Gerenciamento de tarefas com prioridade e status
- Sistema de atribuição de tarefas a usuários
- Comentários em tarefas
- Histórico de alterações de status
- Vinculação de tarefas a sprints

#### 👥 Equipes
- Gerenciamento de membros do projeto
- Atribuição de papéis específicos para cada membro

#### ⚠️ Riscos
- Registro de riscos com probabilidade e impacto
- Matriz de risco automatizada
- Controle de status de riscos
- Planos de mitigação e contingência
- Histórico de alterações

#### 💰 Custos
- Registro de custos do projeto e tarefas
- Categorização de custos
- Sistema de orçamento para projetos e tarefas
- Alertas de orçamento
- Registro de comprovantes

#### 📄 Documentos
- Upload e gerenciamento de documentos
- Versionamento de documentos
- Histórico de alterações
- Comentários em documentos

#### 💬 Comunicações
- Sistema de chat para projetos
- Notificações do sistema
- Configurações de notificações por usuário
- Registro de leitura de mensagens

#### 🔧 Core
- Utilitários e decoradores comuns
- Tratamento de exceções personalizado
- URLs centralizadas

### Componentes Técnicos
- Autenticação JWT personalizada
- Documentação OpenAPI via DRF Spectacular
- Configuração CORS
- Sistema de logging colorido
- Testes automatizados
- Middleware de permissões

## ✅ Funcionalidades já Implementadas

- [x] Sistema de autenticação JWT
- [x] Gerenciamento de usuários e permissões
- [x] CRUD de projetos
- [x] CRUD de tarefas
- [x] CRUD de equipes
- [x] CRUD de riscos
- [x] CRUD de custos
- [x] CRUD de documentos
- [x] CRUD de comunicações
- [x] Documentação da API com DRF Spectacular
- [x] Sistema de notificações
- [x] Histórico de alterações
- [x] Middleware de permissões
- [x] Sistema de orçamento e alertas
- [x] Sistema de chat de projeto

## 📝 Backlog de Funcionalidades a Implementar

### Alta Prioridade

- [ ] **Implementação de Websockets para Chat em Tempo Real**
  - [ ] Configurar Django Channels
  - [ ] Implementar consumidores para chat
  - [ ] Implementar notificações em tempo real

- [ ] **Relatórios e Dashboards**
  - [ ] Relatórios de progresso do projeto
  - [ ] Gráficos de Burndown para Sprints
  - [ ] Relatórios de distribuição de tarefas
  - [ ] Relatórios de riscos por projeto
  - [ ] Relatórios de custos e orçamento

- [ ] **Integração com Calendário**
  - [ ] API para visualização de calendário
  - [ ] Integração com Google Calendar/Outlook
  - [ ] Envio de convites para reuniões

- [ ] **Sistema de Aprovações**
  - [ ] Aprovação de documentos
  - [ ] Aprovação de mudanças em tarefas
  - [ ] Aprovação de orçamentos
  - [ ] Fluxo de aprovação configurável

### Média Prioridade

- [ ] **Melhorias no Sistema de Tarefas**
  - [ ] Implementar subtarefas
  - [ ] Sistema de dependências entre tarefas
  - [ ] Templates de tarefas
  - [ ] Estimativa de tempo e registro de horas trabalhadas

- [ ] **Integrações Externas**
  - [ ] Integração com GitHub/GitLab
  - [ ] Integração com Slack/Discord
  - [ ] Webhooks para automações

- [ ] **Melhorias no Sistema de Documentos**
  - [ ] Visualização de documentos inline
  - [ ] Edição colaborativa de documentos
  - [ ] Sistema de templates de documentos

- [ ] **Sistema de Feedback e Avaliações**
  - [ ] Avaliação de desempenho em tarefas
  - [ ] Feedback de stakeholders
  - [ ] Pesquisas de satisfação

### Baixa Prioridade

- [ ] **Internacionalização Completa**
  - [ ] Suporte a múltiplos idiomas
  - [ ] Tradução de emails e notificações

- [ ] **Melhorias de Segurança**
  - [ ] Autenticação de dois fatores (2FA)
  - [ ] Auditoria avançada de acessos
  - [ ] Políticas de segurança configuráveis

- [ ] **Melhorias de Performance**
  - [ ] Implementar cache Redis
  - [ ] Otimização de consultas ao banco de dados
  - [ ] Paginação e carregamento lazy de relacionamentos

- [ ] **Importação/Exportação de Dados**
  - [ ] Exportação de projetos para Excel/CSV
  - [ ] Importação de projetos de outros sistemas
  - [ ] Exportação de relatórios em PDF

## 🛠️ Melhorias Técnicas

- [ ] **Migração para PostgreSQL**
  - [ ] Configurar PostgreSQL
  - [ ] Migrar dados do SQLite
  - [ ] Adaptar consultas para aproveitar recursos do PostgreSQL

- [ ] **Implementação de Testes Automatizados Completos**
  - [ ] Aumentar cobertura de testes unitários
  - [ ] Implementar testes de integração
  - [ ] Implementar testes de performance

- [ ] **CI/CD**
  - [ ] Configurar pipeline de integração contínua
  - [ ] Implementar deploy automatizado
  - [ ] Análise estática de código

- [ ] **Containerização**
  - [ ] Dockerizar a aplicação
  - [ ] Configurar docker-compose para ambiente de desenvolvimento
  - [ ] Preparar para deployment em Kubernetes

## 📊 Status do Projeto

O backend do Planify está em um estágio avançado de desenvolvimento, com todos os módulos principais já implementados e funcionais. O sistema já oferece uma API completa para gerenciamento de projetos, mas existem diversas oportunidades de melhorias e novas funcionalidades que podem ser implementadas para tornar o sistema ainda mais robusto e completo.

## 📈 Próximos Passos Recomendados

1. Implementar relatórios e dashboards para melhorar a visibilidade dos projetos
2. Adicionar websockets para comunicação em tempo real
3. Desenvolver sistema de aprovações para fluxos de trabalho mais controlados
4. Migrar o banco de dados para PostgreSQL para melhor performance e recursos
5. Implementar subtarefas e dependências entre tarefas
6. Melhorar a cobertura de testes automatizados
7. Dockerizar a aplicação para facilitar o deployment