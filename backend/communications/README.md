# Módulo de Comunicações - Planify

## Visão Geral

O módulo de Comunicações do Planify gerencia todas as interações e notificações entre usuários do sistema. Ele é responsável por:

1. **Chat em Projetos**: Permite que membros da equipe troquem mensagens dentro do contexto de um projeto específico.
2. **Sistema de Notificações**: Gerencia notificações para usuários sobre eventos do sistema (tarefas, projetos, riscos, etc.).
3. **Configurações de Notificações**: Permite que usuários personalizem como e quando desejam receber notificações.
4. **Comunicações Formais**: Facilita comunicações estruturadas entre membros da equipe.

## Modelos de Dados

### ChatMensagem
Representa mensagens trocadas entre usuários em um projeto.
- Campos principais: `projeto`, `autor`, `texto`, `anexo`, `enviado_em`, `editado`
- Relacionamentos: Pertence a um `Projeto` e um `User` (autor)

### ChatMensagemLeitura
Registra quando um usuário leu uma mensagem específica.
- Campos principais: `mensagem`, `usuario`, `lido_em`
- Relacionamentos: Pertence a uma `ChatMensagem` e um `User`

### Notificacao
Gerencia notificações do sistema para usuários.
- Campos principais: `usuario`, `tipo`, `titulo`, `mensagem`, `lida`, `prioridade`, `criada_em`, `lida_em`
- Tipos: TAREFA, PROJETO, EQUIPE, RISCO, DOCUMENTO, SISTEMA
- Relacionamentos: Pertence a um `User` e opcionalmente a um `Projeto` e/ou `Tarefa`

### ConfiguracaoNotificacao
Armazena preferências de notificação para cada usuário.
- Campos principais: Configurações para diferentes tipos de eventos (`tarefa_atribuida`, `projeto_status`, etc.)
- Canais: EMAIL, SISTEMA, AMBOS, NENHUM
- Relacionamentos: Pertence a um `User` (relação um-para-um)

### Comunicacao
Gerencia comunicações formais entre usuários em um projeto.
- Campos principais: `projeto`, `titulo`, `texto`, `remetente`, `destinatarios`, `criada_em`
- Relacionamentos: Pertence a um `Projeto` e um `User` (remetente), e relaciona-se com múltiplos `User` (destinatários)

## API Endpoints

### Chat

- `GET /api/chat-mensagens/` - Lista mensagens (filtráveis por projeto, autor, data, texto)
- `POST /api/chat-mensagens/` - Cria uma nova mensagem
- `GET /api/chat-mensagens/{id}/` - Obtém detalhes de uma mensagem específica
- `PUT/PATCH /api/chat-mensagens/{id}/` - Atualiza uma mensagem
- `DELETE /api/chat-mensagens/{id}/` - Remove uma mensagem
- `POST /api/chat-mensagens/{id}/marcar_como_lida/` - Marca uma mensagem como lida
- `GET /api/chat-mensagens/mensagens_nao_lidas/` - Lista mensagens não lidas pelo usuário

### Notificações

- `GET /api/notificacoes/` - Lista notificações do usuário
- `GET /api/notificacoes/{id}/` - Obtém detalhes de uma notificação
- `POST /api/notificacoes/{id}/marcar_como_lida/` - Marca uma notificação como lida
- `POST /api/notificacoes/marcar_todas_como_lidas/` - Marca todas as notificações como lidas
- `GET /api/notificacoes/nao_lidas/` - Lista notificações não lidas

### Configurações de Notificações

- `GET /api/configuracoes-notificacao/` - Lista configurações do usuário
- `POST /api/configuracoes-notificacao/` - Cria/atualiza configurações
- `GET /api/configuracoes-notificacao/minha_configuracao/` - Obtém ou cria configuração do usuário

## Uso Típico

### Enviar uma mensagem em um projeto

```python
# Cliente
response = requests.post(
    'http://api.planify.com/api/chat-mensagens/',
    json={
        'projeto': 1,
        'texto': 'Olá equipe, temos uma reunião amanhã às 10h.'
    },
    headers={'Authorization': f'Bearer {token}'}
)
```

### Listar notificações não lidas

```python
# Cliente
response = requests.get(
    'http://api.planify.com/api/notificacoes/nao_lidas/',
    headers={'Authorization': f'Bearer {token}'}
)
```

## Integração com outros Módulos

- **Projetos**: As mensagens e comunicações são contextualizadas dentro de projetos
- **Tarefas**: Notificações podem ser geradas por eventos relacionados a tarefas
- **Usuários**: Todas as comunicações envolvem usuários como remetentes e destinatários

## Considerações de Segurança

- Todas as APIs requerem autenticação
- Usuários só podem ver mensagens e notificações relacionadas a eles
- Configurações de notificação são privadas para cada usuário
