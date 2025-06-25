# Refatoração do Módulo Communications - Documentação

## Resumo das Melhorias Implementadas

Este documento descreve as melhorias implementadas no módulo `communications` seguindo as melhores práticas do Django e Django REST Framework.

## 📋 Mudanças Realizadas

### 1. **Padronização da Filtragem com django-filters**

#### ✅ O que foi feito:
- Criado arquivo `communications/filters.py` centralizando toda lógica de filtragem
- Implementadas classes FilterSet para todos os modelos:
  - `ChatMensagemFilter`
  - `ComunicacaoFilter`  
  - `NotificacaoFilter`

#### 🎯 Benefícios:
- **Código mais limpo**: Views não precisam mais de lógica de filtragem manual
- **Consistência**: Todas as views usam o mesmo padrão de filtragem
- **Manutenibilidade**: Filtros centralizados e reutilizáveis
- **Documentação automática**: Swagger gera automaticamente a documentação dos filtros

#### 📝 Como usar:
```python
# Antes (lógica manual na view)
def get_queryset(self):
    queryset = ChatMensagem.objects.all()
    projeto_id = self.request.GET.get('projeto')
    if projeto_id:
        queryset = queryset.filter(projeto_id=projeto_id)
    # ... mais filtros manuais

# Depois (FilterSet declarativo)
class ChatMensagemViewSet(viewsets.ModelViewSet):
    filterset_class = ChatMensagemFilter
    # A filtragem é feita automaticamente!
```

### 2. **Desacoplamento com GenericForeignKey**

#### ✅ O que foi feito:
- Refatorado modelo `Notificacao` para usar `GenericForeignKey`
- Adicionados campos `content_type`, `object_id` e `content_object`
- Mantidos campos legados (`projeto`, `tarefa`) para compatibilidade durante migração
- Criados métodos utilitários `get_related_object_info()` e `set_related_object()`

#### 🎯 Benefícios:
- **Extensibilidade**: Notificações podem ser relacionadas a qualquer modelo
- **Flexibilidade**: Não precisa migração de BD para adicionar novos tipos
- **Escalabilidade**: Sistema preparado para crescimento

#### 📝 Como usar:
```python
# Antes (acoplado a modelos específicos)
notificacao = Notificacao.objects.create(
    usuario=usuario,
    projeto=projeto,  # Limitado apenas a projetos
    titulo="..."
)

# Depois (genérico para qualquer objeto)
NotificationService.create_notification(
    usuario=usuario,
    obj=qualquer_objeto,  # Projeto, Tarefa, Risco, etc.
    titulo="..."
)
```

### 3. **Camada de Serviços**

#### ✅ O que foi feito:
- Criado arquivo `communications/services.py` com:
  - `NotificationService`: Centraliza criação de notificações
  - `ChatService`: Gerencia mensagens de chat com notificações automáticas
  - `CommunicationService`: Gerencia comunicações formais

#### 🎯 Benefícios:
- **Reutilização**: Lógica pode ser usada em views, signals, tasks, etc.
- **Testabilidade**: Serviços são mais fáceis de testar isoladamente
- **Manutenibilidade**: Lógica de negócio centralizada
- **Consistência**: Comportamento padronizado em todo o sistema

#### 📝 Como usar:
```python
# Notificação simples
NotificationService.create_notification(
    usuario=usuario,
    tipo='SISTEMA',
    titulo='Bem-vindo!',
    mensagem='Você foi cadastrado.'
)

# Notificação em lote
NotificationService.bulk_notify_users(
    usuarios=[user1, user2, user3],
    tipo='PROJETO',
    titulo='Projeto atualizado',
    mensagem='O status do projeto foi alterado.'
)

# Mensagem de chat com notificações automáticas
ChatService.send_message(
    projeto=projeto,
    autor=usuario,
    texto='Olá pessoal!',
    notify_members=True  # Notifica automaticamente outros membros
)
```

### 4. **Serializers Simplificados**

#### ✅ O que foi feito:
- Simplificado `ConfiguracaoNotificacaoSerializer` removendo lógica desnecessária
- Adicionado suporte ao `GenericForeignKey` no `NotificacaoSerializer`
- Adicionados campos calculados para melhor experiência da API

#### 🎯 Benefícios:
- **Responsabilidade única**: Serializers focam apenas em serialização
- **Menos código**: Lógica movida para views e serviços apropriados
- **Melhor API**: Campos calculados fornecem mais informações úteis

### 5. **Views Otimizadas**

#### ✅ O que foi feito:
- Removida lógica manual de filtragem das views
- Adicionados `search_fields` e `ordering` padrão
- Integração com serviços para criação de objetos
- Otimização de queries com `select_related` e `prefetch_related`

#### 🎯 Benefícios:
- **Performance**: Queries otimizadas reduzem N+1 problems
- **Funcionalidade**: Busca e ordenação automáticas
- **Consistência**: Comportamento padronizado entre views

## 🔄 Migração e Compatibilidade

### Migração de Dados
1. **Automática**: Criadas migrações para adicionar novos campos
2. **Migração de dados**: Script automático move dados existentes para `GenericForeignKey`
3. **Reversível**: Possível reverter se necessário

### Compatibilidade
- **API**: Todas as APIs existentes continuam funcionando
- **Campos legados**: Mantidos durante período de transição
- **Filtros**: Novos filtros são adicionais, não quebram os existentes

## 📊 Comparação Antes vs Depois

| Aspecto | Antes | Depois |
|---------|-------|---------|
| **Filtragem** | Manual nas views | Declarativa com FilterSets |
| **Notificações** | Acopladas a Projeto/Tarefa | Genéricas para qualquer modelo |
| **Lógica de negócio** | Espalhada nas views | Centralizada em serviços |
| **Testabilidade** | Difícil (views complexas) | Fácil (serviços isolados) |
| **Reutilização** | Baixa | Alta |
| **Manutenibilidade** | Média | Alta |
| **Extensibilidade** | Requer migração BD | Plug-and-play |

## 🚀 Próximos Passos Recomendados

### Curto Prazo (1-2 sprints)
1. **Aplicar migrações** em ambiente de desenvolvimento
2. **Testar integração** com outras partes do sistema
3. **Atualizar testes** existentes para usar novos serviços

### Médio Prazo (3-6 sprints)
1. **Remover campos legados** (`projeto`, `tarefa`) após confirmação
2. **Migrar outras partes** do sistema para usar os serviços
3. **Adicionar novos tipos** de notificação (Riscos, Documentos, etc.)

### Longo Prazo (6+ sprints)
1. **Email/SMS integration** nos serviços de notificação
2. **Notificações em tempo real** (WebSockets)
3. **Analytics** sobre comunicações e engajamento

## 📁 Estrutura de Arquivos

```
communications/
├── models.py           # ✅ Modelo Notificacao com GenericForeignKey
├── serializers.py      # ✅ Serializers simplificados e otimizados
├── views.py           # ✅ Views limpas usando FilterSets e serviços
├── filters.py         # 🆕 Filtros centralizados
├── services.py        # 🆕 Camada de serviços
├── examples.py        # 🆕 Exemplos de uso
└── migrations/
    ├── 0004_add_generic_foreign_key.py     # 🆕 Adiciona campos GenericFK
    └── 0005_migrate_data_to_generic_fk.py  # 🆕 Migra dados existentes
```

## 🧪 Exemplos de Uso

Ver arquivo `communications/examples.py` para exemplos completos de:
- Criação de notificações simples e complexas
- Uso do ChatService
- Comunicações formais
- Verificação de configurações de usuário

## ✅ Testes Recomendados

```python
# Teste do serviço de notificação
def test_notification_service():
    user = User.objects.create_user('test')
    projeto = Projeto.objects.create(titulo='Test')
    
    notification = NotificationService.create_notification(
        usuario=user,
        tipo='PROJETO',
        titulo='Test',
        mensagem='Test message',
        obj=projeto
    )
    
    assert notification.content_object == projeto
    assert notification.get_related_object_info()['type'] == 'projeto'

# Teste do serviço de chat
def test_chat_service():
    projeto = Projeto.objects.create(titulo='Test')
    user = User.objects.create_user('test')
    
    message = ChatService.send_message(
        projeto=projeto,
        autor=user,
        texto='Hello world!'
    )
    
    assert message.texto == 'Hello world!'
    assert message.autor == user
```

---

## 📞 Suporte

Para dúvidas sobre a implementação ou uso dos novos recursos, consulte:
1. Este documento
2. Arquivo `examples.py` com casos de uso
3. Docstrings nos métodos dos serviços
4. Testes unitários (quando implementados)
