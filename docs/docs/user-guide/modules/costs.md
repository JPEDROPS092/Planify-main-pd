---
sidebar_position: 5
---

# Módulo de Custos

O Módulo de Custos do Planify permite planejar, monitorar e controlar os aspectos financeiros dos seus projetos de P&D. Esta seção explica como gerenciar orçamentos, registrar despesas e gerar relatórios financeiros detalhados.

## Visão Geral de Custos

A página principal de Custos apresenta uma visão consolidada dos aspectos financeiros de todos os projetos aos quais você tem acesso:

<!-- ![Visão Geral de Custos](/img/docs/costs-overview.png) -->

### Elementos da Página de Custos

- **Painel de Resumo**: Exibe totais de orçamento, gastos realizados e saldo disponível
- **Filtros**: Filtre por projeto, período, categoria ou responsável
- **Gráficos**: Visualizações de distribuição de custos e tendências
- **Lista de Transações**: Registro de despesas e receitas
- **Alertas**: Notificações sobre limites orçamentários ou anomalias

## Gerenciando Orçamentos

### Criando um Orçamento

1. Na página de Custos ou dentro de um projeto específico, clique em "Gerenciar Orçamentos"
2. Clique no botão "Novo Orçamento"
3. Preencha o formulário:

<!-- ![Formulário de Orçamento](/img/docs/budget-form.png) -->

4. **Informações Básicas**:
   - **Projeto**: Selecione o projeto associado
   - **Nome do Orçamento**: Título descritivo (ex: "Orçamento 2025" ou "Fase 1")
   - **Período**: Datas de início e término da vigência
   - **Valor Total**: Montante total disponível
   - **Responsável**: Pessoa encarregada de gerenciar o orçamento

5. **Distribuição por Categorias**:
   - Aloque valores para diferentes categorias:
     - Pessoal (salários, benefícios)
     - Equipamentos
     - Software
     - Serviços de Terceiros
     - Viagens
     - Materiais
     - Outros

6. **Configurações Avançadas**:
   - **Limites de Alerta**: Percentual para notificações (ex: 80% do orçamento)
   - **Restrições**: Regras específicas de utilização
   - **Notas**: Informações adicionais ou premissas

7. Clique em "Criar Orçamento"

### Visualizando Orçamentos

Na página de orçamentos, você pode:

- Ver todos os orçamentos ativos e encerrados
- Filtrar por projeto, período ou status
- Comparar orçado vs. realizado
- Visualizar gráficos de distribuição e utilização
- Exportar relatórios detalhados

<!-- ![Lista de Orçamentos](/img/docs/budgets-list.png) -->

### Editando um Orçamento

Para modificar um orçamento existente:

1. Na lista de orçamentos, localize o orçamento desejado
2. Clique no ícone de edição (✏️)
3. Atualize as informações necessárias
4. Adicione uma justificativa para a alteração
5. Clique em "Salvar Alterações"

:::note Nota
Todas as alterações em orçamentos são registradas no histórico para auditoria.
:::

### Revisões de Orçamento

Para casos que exigem uma revisão formal:

1. Na página do orçamento, clique em "Solicitar Revisão"
2. Especifique as alterações propostas
3. Forneça justificativa detalhada
4. Selecione aprovadores necessários
5. Submeta para aprovação

O sistema notificará os aprovadores e registrará todo o processo de revisão.

## Registrando Despesas

### Adicionando uma Nova Despesa

1. Na página de Custos, clique no botão "+ Nova Despesa"
2. Preencha o formulário:

<!-- ![Formulário de Despesa](/img/docs/expense-form.png) -->

3. **Informações Básicas**:
   - **Descrição**: Título descritivo da despesa
   - **Projeto**: Projeto associado
   - **Orçamento**: Selecione o orçamento a ser debitado
   - **Categoria**: Tipo de despesa
   - **Valor**: Montante gasto
   - **Data**: Quando a despesa ocorreu
   - **Fornecedor/Beneficiário**: Quem recebeu o pagamento

4. **Detalhes Adicionais**:
   - **Método de Pagamento**: Como foi pago (cartão, transferência, etc.)
   - **Número da Nota Fiscal**: Referência do documento fiscal
   - **Status de Pagamento**: Pendente, Pago, Reembolsado
   - **Alocação**: Distribuição entre centros de custo (se aplicável)

5. **Comprovantes**:
   - Faça upload de notas fiscais, recibos ou outros documentos
   - Adicione comentários ou observações

6. Clique em "Registrar Despesa"

### Aprovação de Despesas

Se configurado, as despesas podem passar por um fluxo de aprovação:

1. Após o registro, a despesa fica com status "Aguardando Aprovação"
2. Os aprovadores designados recebem notificação
3. Cada aprovador pode:
   - Aprovar: A despesa é processada normalmente
   - Rejeitar: A despesa é marcada como rejeitada
   - Solicitar Informações: Pede esclarecimentos ao solicitante
4. Após aprovação final, a despesa é contabilizada no orçamento

<!-- ![Fluxo de Aprovação](/img/docs/expense-approval.png) -->

### Gerenciando Reembolsos

Para despesas que exigem reembolso:

1. Ao registrar a despesa, marque a opção "Requer Reembolso"
2. Especifique quem deve ser reembolsado
3. Adicione dados bancários (se necessário)
4. Após aprovação, o sistema gera uma solicitação de reembolso
5. O status é atualizado conforme o processamento:
   - Solicitado
   - Em Processamento
   - Pago
   - Cancelado

## Visualizações Financeiras

O Planify oferece diversas visualizações para análise financeira:

### Dashboard Financeiro

Visão consolidada com indicadores-chave:
- Orçamento total vs. utilizado
- Gastos por categoria
- Tendências de despesas
- Previsões de fluxo de caixa
- Alertas e notificações

<!-- ![Dashboard Financeiro](/img/docs/financial-dashboard.png) -->

### Relatório de Despesas

Lista detalhada de todas as transações:
- Filtros por data, categoria, projeto, etc.
- Agrupamento personalizado
- Exportação para Excel ou PDF
- Visualização de comprovantes
- Trilha de auditoria

### Análise por Categoria

Distribuição de gastos por tipo:
- Gráficos de pizza/barras
- Comparação entre períodos
- Detalhamento por subcategorias
- Análise de tendências

<!-- ![Análise por Categoria](/img/docs/category-analysis.png) -->

### Fluxo de Caixa

Visualização temporal de receitas e despesas:
- Gráfico de linha/barras por período
- Saldo acumulado
- Projeções futuras
- Pontos de atenção (picos de despesa)

## Recursos Avançados

### Previsão de Custos

Ferramenta para estimar gastos futuros:

1. Acesse "Previsões" no menu de Custos
2. Clique em "Nova Previsão"
3. Selecione o projeto e período
4. Defina premissas e parâmetros
5. O sistema calcula estimativas baseadas em:
   - Dados históricos
   - Cronograma do projeto
   - Compromissos futuros
   - Tendências identificadas

<!-- ![Previsão de Custos](/img/docs/cost-forecast.png) -->

### Cenários Financeiros

Compare diferentes cenários para tomada de decisão:

1. Na página de orçamento, clique em "Criar Cenário"
2. Defina as variáveis a serem alteradas
3. Configure múltiplos cenários (otimista, pessimista, etc.)
4. Visualize o impacto de cada cenário
5. Compare resultados lado a lado

### Importação em Massa

Para adicionar múltiplas transações de uma vez:

1. Na página de Custos, clique em "Importar"
2. Baixe o modelo de planilha
3. Preencha os dados das despesas
4. Faça upload da planilha preenchida
5. Revise as transações a serem importadas
6. Clique em "Importar Despesas"

### Integração Contábil

O Planify pode se integrar com sistemas contábeis:

- Exportação de dados em formatos compatíveis
- Mapeamento de categorias para plano de contas
- Conciliação de transações
- Importação de dados bancários

## Relatórios Financeiros

### Tipos de Relatórios

O módulo de Custos oferece diversos relatórios pré-configurados:

- **Resumo Orçamentário**: Visão geral de orçado vs. realizado
- **Detalhamento de Despesas**: Lista completa de transações
- **Análise por Categoria**: Distribuição de gastos por tipo
- **Análise por Projeto**: Comparação entre projetos
- **Fluxo de Caixa**: Movimentação financeira ao longo do tempo
- **Relatório de Variação**: Análise de desvios orçamentários

### Gerando Relatórios

1. Na página de Custos, clique em "Relatórios"
2. Selecione o tipo de relatório
3. Configure os filtros e parâmetros:
   - Período
   - Projetos
   - Categorias
   - Nível de detalhe
4. Clique em "Gerar Relatório"
5. Visualize, exporte ou compartilhe o relatório

<!-- ![Geração de Relatórios](/img/docs/financial-reports.png) -->

### Relatórios Personalizados

Para necessidades específicas:

1. Clique em "Novo Relatório Personalizado"
2. Selecione os campos a serem incluídos
3. Configure filtros e critérios
4. Defina agrupamentos e totalizadores
5. Escolha o formato de visualização
6. Salve o modelo para uso futuro

## Controles e Segurança

### Permissões Financeiras

O Planify implementa controles de acesso específicos para dados financeiros:

| Papel | Permissões |
|-------|------------|
| **Administrador Financeiro** | Acesso completo a todos os dados financeiros |
| **Gerente de Orçamento** | Criar/editar orçamentos, aprovar despesas |
| **Analista Financeiro** | Visualizar dados, gerar relatórios |
| **Solicitante** | Registrar despesas, visualizar próprias solicitações |

### Trilha de Auditoria

Todas as ações financeiras são registradas para auditoria:

- Quem realizou a ação
- O que foi alterado
- Quando ocorreu
- Justificativa fornecida

Para acessar:
1. Na página de Custos, clique em "Auditoria"
2. Configure os filtros desejados
3. Visualize o histórico completo de alterações

### Alertas e Notificações

Configure alertas para monitoramento proativo:

- Orçamento atingindo limite (ex: 80% utilizado)
- Despesas acima de determinado valor
- Aprovações pendentes há mais de X dias
- Anomalias ou padrões incomuns de gastos

## Integrações

O módulo de Custos se integra com outros componentes do Planify:

- **Projetos**: Orçamentos são vinculados a projetos específicos
- **Tarefas**: Custos podem ser associados a tarefas individuais
- **Equipes**: Despesas relacionadas a membros da equipe
- **Documentos**: Armazenamento de comprovantes e contratos
- **Riscos**: Impacto financeiro de riscos identificados

## Melhores Práticas

### Planejamento Orçamentário

- Envolva as partes interessadas na elaboração do orçamento
- Baseie-se em dados históricos de projetos similares
- Inclua reservas para contingências
- Documente premissas utilizadas
- Revise periodicamente e ajuste conforme necessário

### Controle de Despesas

- Registre despesas assim que ocorrerem
- Categorize corretamente para análise precisa
- Anexe sempre os comprovantes
- Verifique conformidade com políticas internas
- Monitore variações em relação ao orçado

### Análise Financeira

- Compare regularmente orçado vs. realizado
- Identifique tendências e padrões
- Investigue variações significativas
- Use dados financeiros para decisões futuras
- Compartilhe insights relevantes com stakeholders

## Próximos Passos

Agora que você conhece o Módulo de Custos, explore o [Módulo de Documentos](/docs/user-guide/modules/documents) para aprender como gerenciar arquivos e documentação dos seus projetos.
