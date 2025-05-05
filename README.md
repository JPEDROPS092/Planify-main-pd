# Planify - Sistema de Gerenciamento de Projetos de P&D

Planify é um sistema web completo para gerenciamento de projetos de Pesquisa e Desenvolvimento (P&D), desenvolvido com Django REST Framework no backend e Nuxt.js com Material UI no frontend.

## Visão Geral

O Planify tem como missão impulsionar o setor de tecnologia da informação, promovendo colaboração e eficiência. Ao adotar uma abordagem moderna e integrada, o software busca ampliar a interação entre as empresas associadas e fornecer suporte às tomadas de decisão entre as lideranças.

### Principais Módulos

O sistema está estruturado nos seguintes módulos principais:

1. **Usuários (users)** - Autenticação, perfis e permissões
2. **Projetos (projects)** - Gerenciamento de projetos e sprints
3. **Tarefas (tasks)** - Gerenciamento de tarefas e atribuições
4. **Equipes (teams)** - Gerenciamento de equipes e membros
5. **Riscos (risks)** - Identificação e mitigação de riscos
6. **Custos (costs)** - Controle de orçamentos e gastos
7. **Documentos (documents)** - Gerenciamento de documentação
8. **Comunicações (communications)** - Chat integrado e notificações

## Tecnologias Utilizadas

### Backend
- Django 4.2+
- Django REST Framework
- SQLite (desenvolvimento) / PostgreSQL (produção)
- Python 3.9+

### Frontend
- Nuxt.js 3
- Vue.js 3
- Material UI
- Tailwind CSS

## Configuração do Ambiente de Desenvolvimento

### Requisitos
- Python 3.9+
- Node.js 16+
- npm ou yarn

### Backend

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/Planify.git
cd Planify/backend

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor de desenvolvimento
python manage.py runserver
```

### Frontend

```bash
# Navegar para o diretório do frontend
cd ../frontend

# Instalar dependências
npm install

# Executar servidor de desenvolvimento
npm run dev
```

## Estrutura do Projeto

```
Planify/
├── backend/
│   ├── communications/  # Módulo de comunicações e notificações
│   ├── costs/           # Módulo de gestão de custos
│   ├── documents/       # Módulo de documentação
│   ├── planify/         # Configurações do projeto Django
│   ├── projects/        # Módulo de projetos
│   ├── risks/           # Módulo de gestão de riscos
│   ├── tasks/           # Módulo de tarefas
│   ├── teams/           # Módulo de equipes
│   ├── users/           # Módulo de usuários
│   └── manage.py        # Script de gerenciamento Django
│
└── frontend/
    ├── components/      # Componentes Vue reutilizáveis
    ├── layouts/         # Layouts da aplicação
    ├── pages/           # Páginas da aplicação
    ├── plugins/         # Plugins Nuxt.js
    └── nuxt.config.ts   # Configuração do Nuxt.js
```

## Funcionalidades Principais

- Autenticação e controle de acesso baseado em papéis
- Gerenciamento completo de projetos de P&D
- Acompanhamento de tarefas com diferentes status
- Gestão de equipes e atribuição de papéis
- Identificação e mitigação de riscos
- Controle de custos e orçamentos
- Repositório de documentos
- Sistema de comunicação integrado (chat e notificações)
- Calendário de projetos e eventos

## Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.
