
# 🌟 **Planify** - Sistema de Gerenciamento de Projetos de P&D

![Planify Banner](https://via.placeholder.com/1200x400?text=Planify+-+Gerenciamento+de+Projetos+de+P%26D)

**Planify** é uma solução completa para gerenciamento de projetos de Pesquisa e Desenvolvimento (P&D), projetada para promover colaboração, eficiência e organização. Com uma interface moderna e recursos avançados, o Planify é a ferramenta ideal para equipes que buscam excelência em seus projetos.

---

## 🚀 **Visão Geral**

O Planify foi desenvolvido para atender às necessidades de equipes de P&D, oferecendo uma abordagem integrada para gerenciar projetos, tarefas, equipes, riscos, custos e muito mais.

### 🎯 **Missão**

Impulsionar o setor de tecnologia da informação, promovendo colaboração e eficiência, enquanto fornece suporte às tomadas de decisão entre lideranças.

---

## 🛠️ **Principais Funcionalidades**

- 🔒 **Autenticação e Controle de Acesso**: Gerenciamento de usuários com permissões baseadas em papéis.
- 📋 **Gerenciamento de Projetos**: Criação, acompanhamento e análise de projetos.
- ✅ **Tarefas e Kanban**: Gerenciamento de tarefas com visualização em quadro Kanban.
- 👥 **Gestão de Equipes**: Organização de equipes e atribuição de papéis.
- ⚠️ **Gestão de Riscos**: Identificação, análise e mitigação de riscos.
- 💰 **Controle de Custos**: Orçamento, despesas e relatórios financeiros.
- 📂 **Repositório de Documentos**: Upload, versionamento e controle de acesso.
- 💬 **Comunicação Integrada**: Chat e notificações em tempo real.
- 📅 **Calendário de Projetos**: Visualização de eventos e prazos.

---

## 🏗️ **Estrutura do Projeto**

```plaintext
Planify/
├── backend/             # Backend em Django REST Framework
│   ├── communications/  # Módulo de comunicações e notificações
│   ├── costs/           # Módulo de gestão de custos
│   ├── documents/       # Módulo de documentação
│   ├── projects/        # Módulo de projetos
│   ├── risks/           # Módulo de gestão de riscos
│   ├── tasks/           # Módulo de tarefas
│   ├── teams/           # Módulo de equipes
│   ├── users/           # Módulo de usuários
│   └── manage.py        # Script de gerenciamento Django
│
└── frontend/            # Frontend em Nuxt.js
    ├── components/      # Componentes Vue reutilizáveis
    ├── layouts/         # Layouts da aplicação
    ├── pages/           # Páginas da aplicação
    ├── plugins/         # Plugins Nuxt.js
    └── nuxt.config.ts   # Configuração do Nuxt.js
```

---

## 🧰 **Tecnologias Utilizadas**

### **Backend**

- 🐍 **Python 3.9+**
- 🌐 **Django 4.2+**
- 🔗 **Django REST Framework**
- 🗄️ **PostgreSQL** (produção) / **SQLite** (desenvolvimento)

### **Frontend**

- 🖼️ **Nuxt.js 3**
- 🖌️ **Vue.js 3**
- 🎨 **Material UI**
- 🌀 **Tailwind CSS**

---

## ⚙️ **Configuração do Ambiente de Desenvolvimento**

### **Requisitos**

- Python 3.9+
- Node.js 16+
- npm, yarn ou bun

### **Backend**

```bash
# Clonar o repositório
git clone https://github.com/jpedrops092/Planify-main-pd.git
cd Planify-main-pd/backend

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

### **Frontend**

```bash
# Navegar para o diretório do frontend
cd ../frontend

# Instalar dependências
npm install

# Executar servidor de desenvolvimento
npm run dev
```

---

## 🌟 **Como Contribuir**

Contribuições são bem-vindas! Siga os passos abaixo para colaborar:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. Faça commit das suas alterações:
   ```bash
   git commit -m "Adiciona nova funcionalidade"
   ```
4. Faça push para a branch:
   ```bash
   git push origin feature/nova-funcionalidade
   ```
5. Abra um Pull Request.

---

## 📜 **Licença**

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.

---

## 📞 **Contato**

- **GitHub**: [Planify](https://github.com/seu-usuario/Planify)
- **Discord**: [Comunidade Planify](https://discord.gg/planify)
- **Documentação**: [Planify Docs](https://planify-docs.com)

---


>
