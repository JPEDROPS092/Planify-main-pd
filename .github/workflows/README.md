# Configuração do GitHub Actions para o Planify

Este diretório contém os workflows do GitHub Actions configurados para o projeto Planify. Os workflows automatizam os processos de integração contínua (CI) e entrega contínua (CD), garantindo a qualidade do código e facilitando o deploy.

## Workflows Disponíveis

### 1. Backend CI (`backend-ci.yml`)

Este workflow é executado quando há alterações nos arquivos do backend.

**Funcionalidades:**
- Configura um ambiente PostgreSQL para testes
- Instala as dependências Python
- Executa os testes do Django
- Realiza verificação de linting com Flake8

**Quando é executado:**
- Em pushes para a branch `main` que afetam arquivos no diretório `backend/`
- Em pull requests para a branch `main` que afetam arquivos no diretório `backend/`

### 2. Frontend CI (`frontend-ci.yml`)

Este workflow é executado quando há alterações nos arquivos do frontend.

**Funcionalidades:**
- Configura o ambiente Node.js
- Instala as dependências do projeto
- Executa o linting com ESLint
- Realiza o build do projeto Nuxt.js

**Quando é executado:**
- Em pushes para a branch `main` que afetam arquivos no diretório `frontend/`
- Em pull requests para a branch `main` que afetam arquivos no diretório `frontend/`

### 3. Deploy (`deploy.yml`)

Este workflow realiza o deploy do projeto após verificar que os testes do backend e o build do frontend foram bem-sucedidos.

**Funcionalidades:**
- Executa os testes do backend
- Realiza o build do frontend
- Prepara o ambiente de deploy
- Realiza o deploy para o ambiente de produção

**Quando é executado:**
- Em pushes para a branch `main`
- Manualmente através da interface do GitHub (workflow_dispatch)

### 4. Security Scan (`security-scan.yml`)

Este workflow realiza verificações de segurança no código e nas dependências do projeto.

**Funcionalidades:**
- Executa o Bandit para verificar vulnerabilidades no código Python
- Utiliza o Safety para verificar vulnerabilidades nas dependências Python
- Executa o npm audit para verificar vulnerabilidades nas dependências JavaScript

**Quando é executado:**
- Em pushes para a branch `main`
- Em pull requests para a branch `main`
- Automaticamente a cada domingo à meia-noite

## Personalização

Para personalizar os workflows para seu ambiente específico:

1. Modifique o arquivo `deploy.yml` para incluir os comandos específicos do seu ambiente de deploy (Heroku, AWS, etc.)
2. Ajuste as variáveis de ambiente conforme necessário
3. Adicione etapas adicionais conforme os requisitos do seu projeto

## Execução Manual

Você pode executar manualmente o workflow de deploy através da interface do GitHub:

1. Acesse a aba "Actions" do seu repositório
2. Selecione o workflow "Deploy"
3. Clique em "Run workflow"
4. Selecione a branch desejada e clique em "Run workflow"
