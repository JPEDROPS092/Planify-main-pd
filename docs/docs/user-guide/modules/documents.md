---
sidebar_position: 6
---

# Módulo de Documentos

O Módulo de Documentos do Planify permite gerenciar, organizar e compartilhar todos os arquivos e documentos relacionados aos seus projetos de P&D. Esta seção explica como utilizar as ferramentas de gerenciamento documental para manter a informação organizada e acessível.

## Visão Geral de Documentos

A página principal de Documentos apresenta uma visão organizada de todos os arquivos aos quais você tem acesso:

<!-- ![Visão Geral de Documentos](/img/docs/documents-overview.png) -->

### Elementos da Página de Documentos

- **Barra de Pesquisa**: Busque documentos por nome, conteúdo, tags ou metadados
- **Filtros**: Filtre por projeto, tipo, autor, data ou tags
- **Estrutura de Pastas**: Navegue pela hierarquia de diretórios
- **Visualização de Arquivos**: Lista ou grade de documentos
- **Botões de Ação**: Upload, criação de pasta, compartilhamento

## Gerenciando Documentos

### Fazendo Upload de Documentos

1. Na página de Documentos, clique no botão "Upload" ou arraste arquivos para a área designada
2. Selecione um ou mais arquivos do seu computador
3. Escolha a pasta de destino
4. Adicione metadados (opcional):
   - Título personalizado
   - Descrição
   - Tags
   - Projeto associado
5. Clique em "Fazer Upload"

<!-- ![Upload de Documentos](/img/docs/document-upload.png) -->

### Criando Pastas

Para organizar seus documentos:

1. Navegue até o local desejado
2. Clique em "Nova Pasta"
3. Digite o nome da pasta
4. Adicione uma descrição (opcional)
5. Defina permissões de acesso (opcional)
6. Clique em "Criar"

### Visualizando Documentos

O Planify oferece visualização integrada para diversos tipos de arquivo:

1. Clique no documento para abrir a visualização
2. Dependendo do tipo de arquivo, você terá diferentes opções:
   - **Documentos de Texto**: Visualizador com opções de zoom, busca
   - **Planilhas**: Visualização tabular com filtros
   - **PDFs**: Leitor completo com anotações
   - **Imagens**: Visualizador com zoom e rotação
   - **Vídeos**: Player integrado
   - **Código**: Visualizador com syntax highlighting

<!-- ![Visualizador de Documentos](/img/docs/document-viewer.png) -->

### Editando Documentos

Para documentos que suportam edição online:

1. Abra o documento na visualização
2. Clique no botão "Editar"
3. Faça as alterações necessárias
4. Clique em "Salvar"

Para edição offline:

1. Faça o download do arquivo
2. Edite em seu aplicativo local
3. Faça upload da nova versão

### Gerenciando Versões

O Planify mantém o histórico de versões dos documentos:

1. Na página de detalhes do documento, clique na aba "Versões"
2. Visualize todas as versões anteriores com data, autor e comentários
3. Compare versões lado a lado
4. Restaure uma versão anterior se necessário
5. Faça download de versões específicas

<!-- ![Histórico de Versões](/img/docs/document-versions.png) -->

### Excluindo Documentos

Para remover um documento:

1. Selecione o documento na lista
2. Clique no ícone de lixeira ou selecione "Excluir" no menu de ações
3. Confirme a exclusão

:::note Nota
Documentos excluídos são movidos para a "Lixeira" e podem ser recuperados por um período determinado (geralmente 30 dias).
:::

## Organizando Documentos

### Estrutura de Pastas

O Planify permite criar uma hierarquia de pastas para organizar documentos:

#### Estrutura Recomendada para Projetos

```
/Projetos/
  /[Nome do Projeto]/
    /01-Planejamento/
    /02-Documentação Técnica/
    /03-Relatórios/
    /04-Contratos/
    /05-Apresentações/
    /06-Recursos/
```

### Usando Tags

As tags permitem categorização flexível:

1. Selecione um documento
2. Clique em "Editar Tags"
3. Adicione tags existentes ou crie novas
4. Clique em "Salvar"

Você pode filtrar documentos por tags e criar conjuntos de tags para categorias específicas.

### Metadados Personalizados

Configure campos adicionais para seus documentos:

1. Acesse "Configurações" > "Metadados de Documentos"
2. Crie campos personalizados:
   - Texto
   - Número
   - Data
   - Lista de opções
   - Usuário
3. Defina quais tipos de documento usam cada campo
4. Preencha esses campos ao fazer upload ou editar documentos

## Compartilhamento e Colaboração

### Compartilhando Documentos

Para compartilhar um documento ou pasta:

1. Selecione o item
2. Clique em "Compartilhar"
3. Escolha o método de compartilhamento:
   - **Usuários/Equipes**: Selecione usuários ou equipes específicas
   - **Link**: Gere um link de acesso (com ou sem senha)
   - **Público**: Torne acessível para todos no sistema
4. Defina o nível de permissão:
   - **Visualizar**: Apenas leitura
   - **Comentar**: Visualizar e adicionar comentários
   - **Editar**: Visualizar, comentar e modificar
   - **Gerenciar**: Controle total, incluindo compartilhamento
5. Defina uma data de expiração (opcional)
6. Clique em "Compartilhar"

<!-- ![Opções de Compartilhamento](/img/docs/document-sharing.png) -->

### Colaboração em Tempo Real

Para documentos que suportam edição colaborativa:

1. Abra o documento no editor online
2. Compartilhe com outros usuários com permissão de edição
3. Veja indicadores de presença mostrando quem está visualizando/editando
4. Observe as alterações em tempo real
5. Use o chat integrado para discutir mudanças

### Comentários e Anotações

Para adicionar comentários:

1. Abra o documento no visualizador
2. Clique no ícone de comentário ou selecione o texto/área
3. Digite seu comentário
4. Mencione usuários com @nome para notificá-los
5. Clique em "Adicionar Comentário"

Para documentos como PDFs, você pode adicionar anotações diretamente no conteúdo.

## Recursos Avançados

### Controle de Versão

Configure políticas de versionamento:

1. Acesse "Configurações" > "Controle de Versão"
2. Defina regras:
   - Criação automática de versões
   - Número máximo de versões a manter
   - Aprovação necessária para novas versões
   - Bloqueio de documentos em revisão

### Fluxos de Aprovação

Para documentos que requerem aprovação formal:

1. Selecione o documento
2. Clique em "Iniciar Aprovação"
3. Configure o fluxo:
   - Selecione aprovadores
   - Defina prazos
   - Adicione instruções
4. Inicie o processo
5. Acompanhe o status na aba "Aprovações"
6. Os aprovadores recebem notificações e podem:
   - Aprovar
   - Rejeitar (com comentários)
   - Solicitar alterações

<!-- ![Fluxo de Aprovação](/img/docs/document-approval.png) -->

### Modelos de Documentos

Crie e utilize modelos para padronização:

1. Acesse "Modelos" no menu de Documentos
2. Clique em "Novo Modelo"
3. Faça upload ou crie um documento base
4. Defina campos variáveis que serão preenchidos
5. Salve o modelo

Para usar um modelo:
1. Clique em "Novo Documento"
2. Selecione "Usar Modelo"
3. Escolha o modelo desejado
4. Preencha os campos variáveis
5. Clique em "Criar"

### OCR e Pesquisa de Conteúdo

O Planify oferece reconhecimento óptico de caracteres (OCR) para documentos digitalizados:

1. Ao fazer upload, marque a opção "Aplicar OCR"
2. O sistema processará o documento para tornar o texto pesquisável
3. Use a pesquisa global para encontrar conteúdo dentro dos documentos

### Assinaturas Digitais

Para documentos que requerem assinatura:

1. Selecione o documento
2. Clique em "Solicitar Assinatura"
3. Configure o processo:
   - Adicione signatários (internos ou externos)
   - Defina a ordem de assinatura
   - Posicione os campos de assinatura
4. Inicie o processo
5. Acompanhe o status na aba "Assinaturas"

## Integrações

O módulo de Documentos se integra com:

### Integração com Serviços de Armazenamento

Conecte-se a serviços externos:
- Google Drive
- Microsoft OneDrive
- Dropbox
- Amazon S3

Para configurar:
1. Acesse "Configurações" > "Integrações"
2. Selecione o serviço
3. Siga as instruções de autenticação
4. Configure as opções de sincronização

### Integração com Outros Módulos

- **Projetos**: Documentos são organizados por projeto
- **Tarefas**: Anexe documentos diretamente às tarefas
- **Riscos**: Vincule documentação aos registros de riscos
- **Custos**: Associe comprovantes às despesas

## Segurança e Conformidade

### Controle de Acesso

O Planify implementa controles granulares:

- Permissões por pasta/documento
- Herança de permissões na hierarquia
- Restrições baseadas em papéis
- Registro de acesso e auditoria

### Políticas de Retenção

Configure regras para retenção de documentos:

1. Acesse "Configurações" > "Políticas de Retenção"
2. Crie políticas baseadas em:
   - Tipo de documento
   - Classificação
   - Idade do documento
3. Defina ações automáticas:
   - Arquivamento
   - Notificação para revisão
   - Exclusão

### Classificação de Segurança

Categorize documentos por nível de confidencialidade:

- **Público**: Acessível a todos
- **Interno**: Apenas usuários autenticados
- **Confidencial**: Acesso restrito
- **Restrito**: Acesso altamente controlado

A classificação determina controles adicionais como marca d'água, restrições de download, etc.

## Relatórios e Análises

### Relatórios Disponíveis

- **Inventário de Documentos**: Lista completa com metadados
- **Atividade de Documentos**: Acessos, edições, downloads
- **Armazenamento Utilizado**: Uso de espaço por projeto/usuário
- **Documentos Pendentes**: Itens aguardando aprovação/revisão
- **Análise de Colaboração**: Padrões de uso e contribuição

### Gerando Relatórios

1. Na página de Documentos, clique em "Relatórios"
2. Selecione o tipo de relatório
3. Configure os filtros e parâmetros
4. Clique em "Gerar"
5. Visualize, exporte ou agende envios periódicos

## Melhores Práticas

### Organização Eficiente

- Estabeleça uma estrutura de pastas consistente
- Use nomenclatura padronizada para arquivos
- Aplique tags para categorização flexível
- Preencha metadados para facilitar a busca
- Arquive documentos obsoletos regularmente

### Colaboração Produtiva

- Defina claramente as permissões de acesso
- Utilize comentários para discussões contextualizadas
- Mantenha o controle de versões ativo
- Documente as alterações significativas
- Use modelos para padronização

### Segurança Documental

- Classifique documentos por nível de confidencialidade
- Revise periodicamente as permissões de acesso
- Utilize assinaturas digitais para documentos oficiais
- Implemente políticas de retenção adequadas
- Monitore e audite o acesso a documentos sensíveis

## Próximos Passos

Agora que você conhece o Módulo de Documentos, explore o [Módulo de Comunicações](/docs/user-guide/modules/communications) para aprender como gerenciar a comunicação entre os membros da equipe.
