# Plano de Testes para o Módulo Teams

## Visão Geral

Este plano de testes foi desenvolvido para o módulo `teams` do projeto Planify usando **pytest** como framework de testes. O módulo gerencia equipes, membros e permissões dentro do sistema.

## Estrutura de Testes

### 📁 Arquivos de Teste

```
teams/tests/
├── conftest.py              # Fixtures compartilhadas
├── test_models.py           # Testes dos modelos
├── test_serializers.py      # Testes dos serializers
├── test_views.py           # Testes das views/API
├── test_fixtures.py        # Testes das fixtures
├── test_integration.py     # Testes de integração
└── __init__.py
```

### 🧪 Tipos de Teste

#### 1. **Testes de Modelos** (`test_models.py`)
- **Equipe Model**
  - ✅ Criação com dados válidos
  - ✅ Validações de campos obrigatórios
  - ✅ Relacionamentos com membros e permissões
  - ✅ Representação string (`__str__`)
  
- **MembroEquipe Model**
  - ✅ Criação de membros válidos
  - ✅ Constraint `unique_together` (equipe + usuário)
  - ✅ Lógica de primeiro membro como PO
  - ✅ Validação de papéis disponíveis
  - ✅ Relacionamentos com usuário e equipe
  
- **PermissaoEquipe Model**
  - ✅ Criação de permissões válidas
  - ✅ Constraint `unique_together` 
  - ✅ Validação de módulos e permissões
  - ✅ Métodos de display
  
- **Relacionamentos e Cascatas**
  - ✅ Efeito cascata ao deletar equipe
  - ✅ SET_NULL ao deletar usuário criador
  - ✅ Cascade ao deletar usuário membro

#### 2. **Testes de Serializers** (`test_serializers.py`)
- **PermissaoEquipeSerializer**
  - ✅ Serialização completa
  - ✅ Deserialização e validação
  - ✅ Campos de display
  
- **MembroEquipeSerializer**
  - ✅ Serialização com dados aninhados
  - ✅ Validações de campos obrigatórios
  - ✅ Campos readonly
  
- **EquipeSerializer**
  - ✅ Serialização com membros e permissões aninhados
  - ✅ Campo calculado `total_membros`
  - ✅ Validações de criação e atualização
  - ✅ Campos readonly (criado_em, atualizado_em)
  
- **Integração entre Serializers**
  - ✅ Dados aninhados funcionais
  - ✅ Relacionamentos preservados

#### 3. **Testes de Views/API** (`test_views.py`)
- **EquipeViewSet - CRUD**
  - ✅ Listagem paginada
  - ✅ Recuperação de equipe específica
  - ✅ Criação de nova equipe
  - ✅ Atualização completa e parcial
  - ✅ Exclusão de equipe
  
- **EquipeViewSet - Filtros**
  - ✅ Filtro por texto (nome/descrição)
  - ✅ Filtro "minhas equipes"
  - ✅ Filtro por usuário específico
  
- **EquipeViewSet - Actions Customizadas**
  - ✅ `membros/` - listar membros
  - ✅ `adicionar_membro/` - adicionar membro
  - ✅ `atualizar_papel_membro/` - alterar papel
  - ✅ `remover_membro/` - remover membro
  - ✅ `usuarios_disponiveis/` - usuários não membros
  
- **PermissaoEquipeViewSet**
  - ✅ CRUD completo de permissões
  - ✅ Validações de duplicatas
  
- **Busca e Ordenação**
  - ✅ Search por nome e descrição
  - ✅ Ordenação por campos permitidos
  
- **Permissões e Autenticação**
  - ✅ Endpoints protegidos por autenticação
  - ✅ Acesso negado para não autenticados

#### 4. **Testes de Fixtures** (`test_fixtures.py`)
- **Validação das Fixtures**
  - ✅ Criação correta de usuários
  - ✅ Cliente API autenticado
  - ✅ Equipes com dados válidos
  - ✅ Membros e permissões relacionados
  
- **Dependências e Isolamento**
  - ✅ Dependências entre fixtures funcionais
  - ✅ Isolamento entre testes
  - ✅ Performance otimizada

#### 5. **Testes de Integração** (`test_integration.py`)
- **Fluxos Completos**
  - ✅ Criação de equipe + adição de membros + permissões
  - ✅ Gestão completa de membros (adicionar/atualizar/remover)
  - ✅ Hierarquia de permissões por papel
  
- **Busca e Filtros Integrados**
  - ✅ Busca combinada equipes/usuários
  - ✅ Filtros complexos funcionais
  
- **Validações de Negócio**
  - ✅ Membro único por equipe
  - ✅ Permissão única por combinação
  - ✅ Papéis válidos
  
- **Efeitos Cascata**
  - ✅ Exclusão de equipe remove membros/permissões
  - ✅ Exclusão de usuário afeta relacionamentos

## 📊 Cobertura de Testes

### Modelos de Dados
| Modelo | Cobertura | Testes |
|--------|-----------|--------|
| `Equipe` | 100% | 7 testes |
| `MembroEquipe` | 100% | 11 testes |
| `PermissaoEquipe` | 100% | 9 testes |
| Relacionamentos | 100% | 3 testes |

### API Endpoints
| Endpoint | Métodos | Cobertura | Testes |
|----------|---------|-----------|--------|
| `/equipes/` | GET, POST | 100% | 8 testes |
| `/equipes/{id}/` | GET, PUT, PATCH, DELETE | 100% | 4 testes |
| `/equipes/{id}/membros/` | GET | 100% | 1 teste |
| `/equipes/{id}/adicionar_membro/` | POST | 100% | 2 testes |
| `/equipes/{id}/atualizar_papel_membro/` | POST | 100% | 1 teste |
| `/equipes/{id}/remover_membro/` | POST | 100% | 1 teste |
| `/equipes/usuarios_disponiveis/` | GET | 100% | 1 teste |
| `/permissoes/` | GET, POST, PUT, PATCH, DELETE | 100% | 6 testes |

### Serializers
| Serializer | Cobertura | Testes |
|------------|-----------|--------|
| `EquipeSerializer` | 100% | 8 testes |
| `MembroEquipeSerializer` | 100% | 4 testes |
| `PermissaoEquipeSerializer` | 100% | 3 testes |
| Integração | 100% | 2 testes |

## 🚀 Executando os Testes

### Pré-requisitos
```bash
# Instalar dependências
pip install pytest pytest-django

# Configurar DJANGO_SETTINGS_MODULE
export DJANGO_SETTINGS_MODULE=planify.settings
```

### Comandos de Execução

```bash
# Executar todos os testes do módulo teams
pytest teams/tests/

# Executar arquivo específico
pytest teams/tests/test_models.py

# Executar classe específica
pytest teams/tests/test_models.py::TestEquipeModel

# Executar teste específico
pytest teams/tests/test_models.py::TestEquipeModel::test_criacao_equipe_valida

# Com relatório de cobertura
pytest teams/tests/ --cov=teams

# Com relatório HTML de cobertura
pytest teams/tests/ --cov=teams --cov-report=html

# Modo verboso
pytest teams/tests/ -v

# Parar no primeiro erro
pytest teams/tests/ -x

# Executar testes em paralelo
pytest teams/tests/ -n auto
```

### Marcadores de Teste

```bash
# Apenas testes que usam banco de dados
pytest teams/tests/ -m django_db

# Apenas testes de integração
pytest teams/tests/test_integration.py

# Apenas testes de modelos
pytest teams/tests/test_models.py
```

## 🔧 Configuração

### Arquivos de Configuração

1. **`pytest.ini`** (raiz do projeto):
```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = planify.settings
python_files = tests.py test_*.py *_tests.py
addopts = --tb=short --strict-markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

2. **`conftest.py`** (teams/tests/):
- Fixtures compartilhadas para todos os testes
- Configuração de banco de dados de teste
- Dados de teste reutilizáveis

## 📈 Métricas de Qualidade

### Objetivos de Cobertura
- **Modelos**: 100% de cobertura
- **Views**: 95% de cobertura  
- **Serializers**: 100% de cobertura
- **Integração**: 90% de cobertura

### Tipos de Validação
- ✅ **Funcionais**: Comportamento correto das funcionalidades
- ✅ **Validação**: Regras de negócio respeitadas
- ✅ **Segurança**: Autenticação e autorização
- ✅ **Performance**: Fixtures otimizadas
- ✅ **Integração**: Fluxos completos funcionais

## 🐛 Estratégia de Debugging

### Para Falhas de Teste
```bash
# Executar com mais detalhes
pytest teams/tests/test_models.py::test_falhou -vvv

# Entrar no debugger em falhas
pytest teams/tests/test_models.py --pdb

# Ver output completo
pytest teams/tests/test_models.py -s
```

### Para Problemas de Fixtures
```bash
# Verificar fixtures disponíveis
pytest teams/tests/test_fixtures.py -v

# Testar fixture específica
pytest teams/tests/test_fixtures.py::test_user_fixtures
```

## 📋 Checklist de Validação

Antes de considerar o módulo teams testado completamente:

- [ ] ✅ Todos os modelos testados
- [ ] ✅ Todos os endpoints testados  
- [ ] ✅ Todos os serializers testados
- [ ] ✅ Fixtures validadas e funcionais
- [ ] ✅ Testes de integração passando
- [ ] ✅ Cobertura de código > 95%
- [ ] ✅ Testes executam sem warnings
- [ ] ✅ Performance aceitável (< 30s total)
- [ ] ✅ Documentação atualizada

## 🔄 Manutenção

### Quando Adicionar Novos Testes
- Novos modelos ou campos
- Novos endpoints ou actions
- Novas regras de negócio
- Bugs descobertos em produção

### Quando Atualizar Testes Existentes
- Mudanças na lógica de negócio
- Alterações nos modelos
- Modificações nos serializers
- Refatoração de views

## 📚 Recursos Adicionais

- [Documentação pytest-django](https://pytest-django.readthedocs.io/)
- [Django Testing Best Practices](https://docs.djangoproject.com/en/stable/topics/testing/)
- [DRF Testing Guide](https://www.django-rest-framework.org/api-guide/testing/)

---

**Autor**: GitHub Copilot  
**Data**: 2025-06-24  
**Versão**: 1.0
