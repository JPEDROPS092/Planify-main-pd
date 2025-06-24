# Módulo Teams - Documentação Completa

## Visão Geral

O módulo Teams é responsável pelo gerenciamento de equipes no sistema Planify. Ele permite a criação, organização e administração de equipes de trabalho, incluindo membros, papéis e permissões específicas.

## Modelos de Dados

### Equipe

Representa uma equipe de trabalho no sistema.

**Campos:**
- `nome` (CharField): Nome da equipe (máximo 200 caracteres)
- `descricao` (TextField): Descrição detalhada da equipe (opcional)
- `criado_por` (ForeignKey): Usuário que criou a equipe
- `criado_em` (DateTimeField): Data e hora de criação
- `atualizado_em` (DateTimeField): Data e hora da última atualização

**Relacionamentos:**
- `membros`: Membros da equipe (através de MembroEquipe)
- `permissoes`: Permissões da equipe (através de PermissaoEquipe)

### MembroEquipe

Representa a participação de um usuário em uma equipe.

**Campos:**
- `equipe` (ForeignKey): Equipe à qual o membro pertence
- `usuario` (ForeignKey): Usuário que é membro da equipe
- `papel` (CharField): Papel do membro na equipe
- `adicionado_em` (DateTimeField): Data e hora em que foi adicionado
- `adicionado_por` (ForeignKey): Usuário que adicionou este membro

**Papéis Disponíveis:**
- `PO`: Product Owner
- `SM`: Scrum Master
- `DEV`: Desenvolvedor
- `QA`: Quality Assurance
- `DESIGN`: Designer
- `STAKEHOLDER`: Stakeholder

**Restrições:**
- Um usuário não pode ser adicionado duas vezes na mesma equipe (unique_together)

### PermissaoEquipe

Define permissões específicas para papéis dentro de uma equipe.

**Campos:**
- `papel` (CharField): Papel ao qual a permissão se aplica
- `equipe` (ForeignKey): Equipe à qual a permissão pertence
- `modulo` (CharField): Módulo do sistema
- `permissao` (CharField): Tipo de permissão

**Módulos Disponíveis:**
- `PROJECTS`: Projetos
- `TASKS`: Tarefas
- `RISKS`: Riscos
- `COSTS`: Custos
- `DOCUMENTS`: Documentos
- `COMMUNICATIONS`: Comunicações

**Tipos de Permissão:**
- `CREATE`: Criar
- `READ`: Visualizar
- `UPDATE`: Atualizar
- `DELETE`: Excluir

**Restrições:**
- Não pode haver permissões duplicadas (unique_together)

## API Endpoints

### Equipes

#### Listar Equipes
```
GET /equipes/
```

**Parâmetros de Query:**
- `texto`: Filtrar por nome ou descrição
- `minhas_equipes`: Filtrar apenas equipes do usuário logado
- `usuario`: Filtrar por membro específico
- `search`: Busca textual em nome e descrição
- `ordering`: Ordenação (-criado_em, nome, etc.)

**Resposta:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "nome": "Equipe de Desenvolvimento",
      "criado_por_nome": "João Silva",
      "criado_em": "2025-06-24T10:00:00Z",
      "total_membros": 5
    }
  ]
}
```

#### Obter Detalhes da Equipe
```
GET /equipes/{id}/
```

**Resposta:**
```json
{
  "id": 1,
  "nome": "Equipe de Desenvolvimento",
  "descricao": "Equipe responsável pelo desenvolvimento do sistema",
  "criado_por": 1,
  "criado_por_nome": "João Silva",
  "criado_em": "2025-06-24T10:00:00Z",
  "atualizado_em": "2025-06-24T10:00:00Z",
  "total_membros": 5,
  "membros": [
    {
      "id": 1,
      "usuario": 1,
      "usuario_nome": "João Silva",
      "usuario_email": "joao@example.com",
      "papel": "PO",
      "papel_display": "Product Owner",
      "adicionado_em": "2025-06-24T10:00:00Z",
      "adicionado_por": 1,
      "adicionado_por_nome": "João Silva"
    }
  ],
  "permissoes": [
    {
      "id": 1,
      "papel": "DEV",
      "papel_display": "Desenvolvedor",
      "modulo": "TASKS",
      "modulo_display": "Tarefas",
      "permissao": "CREATE",
      "permissao_display": "Criar"
    }
  ]
}
```

#### Criar Equipe
```
POST /equipes/
```

**Payload:**
```json
{
  "nome": "Nova Equipe",
  "descricao": "Descrição da nova equipe"
}
```

**Nota:** O usuário que cria a equipe é automaticamente adicionado como membro com papel de Product Owner (PO).

#### Atualizar Equipe
```
PUT /equipes/{id}/
PATCH /equipes/{id}/
```

#### Excluir Equipe
```
DELETE /equipes/{id}/
```

### Actions Customizadas de Equipes

#### Listar Membros
```
GET /equipes/{id}/membros/
```

#### Adicionar Membro
```
POST /equipes/{id}/adicionar_membro/
```

**Payload:**
```json
{
  "usuario": 2,
  "papel": "DEV"
}
```

#### Atualizar Papel do Membro
```
POST /equipes/{id}/atualizar_papel_membro/
```

**Payload:**
```json
{
  "usuario": 2,
  "papel": "SM"
}
```

#### Remover Membro
```
POST /equipes/{id}/remover_membro/
```

**Payload:**
```json
{
  "usuario": 2
}
```

#### Usuários Disponíveis
```
GET /equipes/usuarios_disponiveis/?equipe={equipe_id}
```

Retorna usuários que podem ser adicionados à equipe (que ainda não são membros).

### Permissões de Equipe

#### Listar Permissões
```
GET /permissoes/
```

#### Obter Permissão
```
GET /permissoes/{id}/
```

#### Criar Permissão
```
POST /permissoes/
```

**Payload:**
```json
{
  "papel": "DEV",
  "equipe": 1,
  "modulo": "TASKS",
  "permissao": "CREATE"
}
```

#### Atualizar Permissão
```
PUT /permissoes/{id}/
PATCH /permissoes/{id}/
```

#### Excluir Permissão
```
DELETE /permissoes/{id}/
```

## Serializers

### EquipeSerializer
Serializer completo para operações CRUD de equipes. Inclui:
- Dados básicos da equipe
- Lista de membros
- Lista de permissões
- Total de membros
- Criação automática do criador como membro PO

### EquipeListSerializer
Serializer simplificado para listagem de equipes. Inclui apenas:
- ID, nome, criador, data de criação e total de membros

### MembroEquipeSerializer
Serializer para membros de equipe. Inclui:
- Dados do usuário (nome, email)
- Papel e sua descrição
- Dados de quem adicionou
- Data de adição

### PermissaoEquipeSerializer
Serializer para permissões de equipe. Inclui:
- Papel, módulo e permissão com suas descrições
- Referência à equipe

### UserMinimalSerializer
Serializer mínimo para usuários, usado para seleção de membros.

## Permissões e Autenticação

- **Autenticação obrigatória:** Todos os endpoints requerem autenticação
- **Permissões:** `IsAuthenticated` para todas as operações
- **Restrições de negócio:**
  - Usuários não podem ser adicionados duas vezes na mesma equipe
  - Permissões não podem ser duplicadas
  - Apenas membros da equipe podem visualizar detalhes completos

## Funcionalidades Especiais

### Busca e Filtros
- **Busca textual:** Por nome e descrição das equipes
- **Filtro por membro:** Equipes que contêm um usuário específico
- **Minhas equipes:** Equipes onde o usuário logado é membro
- **Ordenação:** Por nome, data de criação, etc.

### Gestão Automática
- **Criador como PO:** Ao criar uma equipe, o criador é automaticamente adicionado como Product Owner
- **Usuários disponíveis:** API para listar usuários que podem ser adicionados à equipe
- **Validações:** Previne duplicação de membros e permissões

### Exclusão em Cascata
- **Deletar equipe:** Remove automaticamente todos os membros e permissões
- **Deletar usuário:** Remove automaticamente suas participações em equipes

## Casos de Uso Comuns

### 1. Criar uma Equipe Ágil Completa

```python
# 1. Criar equipe
POST /equipes/
{
  "nome": "Equipe Scrum Alpha",
  "descricao": "Equipe de desenvolvimento ágil"
}

# 2. Adicionar Scrum Master
POST /equipes/1/adicionar_membro/
{
  "usuario": 2,
  "papel": "SM"
}

# 3. Adicionar Desenvolvedores
POST /equipes/1/adicionar_membro/
{
  "usuario": 3,
  "papel": "DEV"
}

# 4. Configurar permissões para desenvolvedores
POST /permissoes/
{
  "papel": "DEV",
  "equipe": 1,
  "modulo": "TASKS",
  "permissao": "CREATE"
}
```

### 2. Reestruturar Equipe

```python
# 1. Promover desenvolvedor para Scrum Master
POST /equipes/1/atualizar_papel_membro/
{
  "usuario": 3,
  "papel": "SM"
}

# 2. Remover membro que saiu da empresa
POST /equipes/1/remover_membro/
{
  "usuario": 4
}

# 3. Adicionar novo membro
POST /equipes/1/adicionar_membro/
{
  "usuario": 5,
  "papel": "QA"
}
```

### 3. Consultar Informações da Equipe

```python
# 1. Listar minhas equipes
GET /equipes/?minhas_equipes=true

# 2. Buscar equipes por tecnologia
GET /equipes/?search=React

# 3. Ver detalhes completos da equipe
GET /equipes/1/

# 4. Listar apenas membros
GET /equipes/1/membros/
```

## Testes

O módulo inclui uma suíte completa de testes cobrindo:

### Testes de Modelos (`test_models.py`)
- Criação e validação de equipes, membros e permissões
- Relacionamentos entre modelos
- Restrições de integridade
- Exclusão em cascata

### Testes de Serializers (`test_serializers.py`)
- Serialização e deserialização de dados
- Validações de campos
- Contexto de request
- Campos read-only

### Testes de Views (`test_views.py`)
- Endpoints de CRUD
- Actions customizadas
- Filtros e busca
- Autenticação e permissões

### Testes de Integração (`test_integration.py`)
- Fluxos completos de trabalho
- Cenários de uso real
- Testes de performance
- Testes de cascata

### Executar Testes

```bash
# Todos os testes do módulo teams
python manage.py test teams

# Testes específicos
python manage.py test teams.tests.test_models
python manage.py test teams.tests.test_views.EquipeViewSetTest

# Com cobertura
coverage run --source='teams' manage.py test teams
coverage report
```

## Configuração

### URLs
Adicione ao `urls.py` principal:

```python
from django.urls import path, include

urlpatterns = [
    path('api/teams/', include('teams.urls')),
]
```

### Settings
Certifique-se de que o app está em `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'teams',
    # ...
]
```

### Migrações
```bash
python manage.py makemigrations teams
python manage.py migrate
```

## Dependências

- Django REST Framework
- django-filter
- drf-spectacular (para documentação OpenAPI)

## Estrutura de Arquivos

```
teams/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── views.py
├── urls.py
├── migrations/
│   └── ...
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_serializers.py
    ├── test_views.py
    └── test_integration.py
```

## Considerações de Segurança

- **Autenticação obrigatória:** Todos os endpoints requerem usuário autenticado
- **Validação de entrada:** Todos os dados são validados antes da persistência
- **Prevenção de duplicatas:** Restrições de unicidade para evitar dados inconsistentes
- **Permissões granulares:** Sistema de permissões por papel e módulo
- **Auditoria:** Rastreamento de quem adicionou cada membro

## Performance

- **Queries otimizadas:** Uso de `select_related` e `prefetch_related`
- **Paginação:** Listagens são paginadas automaticamente
- **Índices:** Campos chave possuem índices para busca rápida
- **Cache:** Considere implementar cache para listagens frequentes

## Monitoramento

Logs importantes são gerados para:
- Criação e exclusão de equipes
- Adição e remoção de membros
- Mudanças de papel
- Configuração de permissões

## Roadmap Futuro

Funcionalidades planejadas:
- **Notificações:** Alertas para mudanças na equipe
- **Histórico:** Rastreamento de mudanças
- **Templates:** Modelos predefinidos de equipes
- **Métricas:** Dashboard com estatísticas da equipe
- **Integração:** Sincronização com ferramentas externas
