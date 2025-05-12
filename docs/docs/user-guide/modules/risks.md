---
sidebar_position: 4
---

# Módulo de Riscos

O Módulo de Riscos do Planify permite identificar, avaliar e gerenciar de forma proativa os riscos associados aos seus projetos de P&D. Esta seção explica como utilizar as ferramentas de gerenciamento de riscos para minimizar ameaças e maximizar oportunidades.

## Visão Geral de Riscos

A página principal de Riscos apresenta uma visão consolidada dos riscos identificados em todos os projetos aos quais você tem acesso:

<!-- ![Lista de Riscos](/img/docs/risks-list.png) -->

### Elementos da Página de Riscos

- **Barra de Pesquisa**: Busque riscos por descrição, categoria ou projeto
- **Filtros**: Filtre por projeto, categoria, probabilidade, impacto ou status
- **Botão de Novo Risco**: Inicie o registro de um novo risco
- **Lista de Riscos**: Exibe os riscos com informações resumidas
- **Matriz de Riscos**: Visualização gráfica baseada em probabilidade e impacto

## Registrando um Novo Risco

### Passo a Passo para Registro

1. Na página de Riscos ou dentro de um projeto específico, clique no botão "+ Novo Risco"
2. Preencha o formulário de registro:

<!-- ![Formulário de Novo Risco](/img/docs/new-risk-form.png) -->

3. **Informações Básicas**:
   - **Título**: Descrição concisa do risco
   - **Descrição Detalhada**: Explicação completa do risco e suas implicações
   - **Projeto**: Selecione o projeto associado
   - **Categoria**: Tipo de risco (Técnico, Financeiro, Operacional, etc.)
   - **Responsável**: Pessoa encarregada de monitorar e tratar o risco

4. **Avaliação do Risco**:
   - **Probabilidade**: Chance de ocorrência (Muito Baixa, Baixa, Média, Alta, Muito Alta)
   - **Impacto**: Severidade das consequências (Muito Baixo, Baixo, Médio, Alto, Muito Alto)
   - **Exposição**: Calculada automaticamente (Probabilidade × Impacto)
   - **Data de Identificação**: Quando o risco foi identificado
   - **Gatilhos**: Eventos ou condições que indicam a materialização do risco

5. **Tratamento do Risco**:
   - **Estratégia**: Abordagem para lidar com o risco:
     - **Evitar**: Eliminar a causa
     - **Mitigar**: Reduzir probabilidade ou impacto
     - **Transferir**: Passar para terceiros (seguro, outsourcing)
     - **Aceitar**: Reconhecer e monitorar sem ação específica
   - **Plano de Resposta**: Ações planejadas caso o risco se materialize
   - **Plano de Contingência**: Alternativas se a resposta principal falhar
   - **Custo Estimado**: Recursos necessários para o tratamento

6. Clique em "Registrar Risco"

## Detalhes do Risco

Ao clicar em um risco na lista, você acessa a página de detalhes:

<!-- ![Detalhes do Risco](/img/docs/risk-details.png) -->

### Seções da Página de Detalhes

#### Informações Principais

Exibe os dados essenciais do risco:
- Título e descrição
- Categoria e projeto associado
- Responsável pelo monitoramento
- Avaliação de probabilidade e impacto
- Status atual

#### Plano de Tratamento

Detalha as estratégias para gerenciar o risco:
- Estratégia selecionada
- Ações de mitigação planejadas
- Plano de contingência
- Custos associados ao tratamento
- Cronograma de implementação

#### Monitoramento

Acompanha a evolução do risco ao longo do tempo:
- Histórico de avaliações
- Indicadores de tendência
- Gatilhos identificados
- Próximas revisões programadas

#### Ações

Lista as atividades específicas para tratamento:
- Descrição da ação
- Responsável pela execução
- Prazo para conclusão
- Status de implementação
- Eficácia observada

#### Histórico

Registra todas as alterações no risco:
- Mudanças na avaliação
- Atualizações no plano de tratamento
- Ocorrências relacionadas
- Data, hora e autor de cada alteração

## Gerenciando Riscos

### Atualizando a Avaliação

Para atualizar a avaliação de um risco:

1. Na página de detalhes, clique no botão "Atualizar Avaliação"
2. Ajuste os valores de probabilidade e impacto
3. Adicione justificativa para a mudança
4. Clique em "Salvar Avaliação"

O histórico de avaliações é mantido para análise de tendências.

### Alterando o Status

Para modificar o status de um risco:

1. Na página de detalhes, clique no status atual
2. Selecione o novo status:
   - **Identificado**: Recém registrado, sem tratamento iniciado
   - **Em Análise**: Sendo avaliado em detalhes
   - **Em Tratamento**: Ações de mitigação em andamento
   - **Monitorando**: Sob observação após tratamento inicial
   - **Ocorrido**: Risco que se materializou
   - **Encerrado**: Risco que não é mais relevante
3. Adicione um comentário explicando a mudança
4. Clique em "Atualizar Status"

### Adicionando Ações de Tratamento

Para registrar ações específicas:

1. Na seção "Ações", clique em "Nova Ação"
2. Preencha o formulário:
   - Descrição da ação
   - Responsável pela execução
   - Data de início e término previsto
   - Recursos necessários
3. Clique em "Adicionar Ação"

### Registrando Ocorrências

Quando um risco se materializa:

1. Na página de detalhes, clique em "Registrar Ocorrência"
2. Descreva o que aconteceu
3. Indique a data e hora da ocorrência
4. Avalie o impacto real
5. Documente as ações tomadas
6. Clique em "Salvar Ocorrência"

## Visualizações de Riscos

O Planify oferece diferentes formas de visualizar os riscos:

### Lista

A visualização padrão, ideal para ver muitos riscos com detalhes:
- Colunas personalizáveis
- Ordenação por qualquer campo
- Agrupamento por projeto, categoria, responsável, etc.
- Exportação para Excel ou CSV

### Matriz de Riscos

Visualização gráfica baseada em probabilidade e impacto:
- Eixo X: Impacto (Muito Baixo a Muito Alto)
- Eixo Y: Probabilidade (Muito Baixa a Muito Alta)
- Cores indicando níveis de exposição (Verde, Amarelo, Laranja, Vermelho)
- Tamanho dos pontos proporcional ao número de riscos

<!-- ![Matriz de Riscos](/img/docs/risk-matrix.png) -->

### Gráficos

Visualizações analíticas dos dados de risco:
- **Distribuição por Categoria**: Gráfico de pizza/barras
- **Tendência de Exposição**: Gráfico de linha temporal
- **Top Riscos**: Ranking dos riscos mais críticos
- **Status de Tratamento**: Progresso das ações

<!-- ![Gráficos de Riscos](/img/docs/risk-charts.png) -->

### Mapa de Calor

Visualização da distribuição de riscos por projeto ou área:
- Representação visual da concentração de riscos
- Cores indicando níveis de exposição
- Drill-down para análise detalhada
- Comparação entre projetos

## Recursos Avançados

### Análise Quantitativa

Para riscos que requerem avaliação numérica detalhada:

1. Na página de detalhes, clique na aba "Análise Quantitativa"
2. Configure os parâmetros:
   - Impacto financeiro mínimo, mais provável e máximo
   - Distribuição de probabilidade
   - Correlações com outros riscos
3. Execute a simulação Monte Carlo
4. Analise os resultados:
   - Valor esperado
   - Pior cenário
   - Intervalo de confiança
   - Gráficos de distribuição

### Templates de Riscos

Crie e utilize templates para padronizar a identificação de riscos:

#### Criando um Template

1. Acesse "Configurações" > "Templates de Riscos"
2. Clique em "Novo Template"
3. Defina categorias e riscos comuns
4. Configure avaliações padrão
5. Salve o template

#### Usando um Template

1. Ao criar um novo projeto, selecione "Aplicar Template de Riscos"
2. Escolha o template desejado
3. Os riscos predefinidos serão adicionados ao projeto
4. Personalize conforme necessário

### Importação em Massa

Para adicionar múltiplos riscos de uma vez:

1. Na página de Riscos, clique em "Importar"
2. Baixe o modelo de planilha
3. Preencha os dados dos riscos
4. Faça upload da planilha preenchida
5. Revise os riscos a serem importados
6. Clique em "Importar Riscos"

### Relatórios de Riscos

Gere relatórios detalhados para análise e comunicação:

#### Tipos de Relatórios

- **Resumo Executivo**: Visão geral para stakeholders
- **Registro Detalhado**: Lista completa com todos os detalhes
- **Análise de Tendências**: Evolução dos riscos ao longo do tempo
- **Eficácia de Tratamento**: Avaliação das ações implementadas

#### Gerando Relatórios

1. Na página de Riscos, clique em "Relatórios"
2. Selecione o tipo de relatório
3. Configure os filtros e parâmetros
4. Clique em "Gerar"
5. Visualize ou exporte (PDF, Excel, PowerPoint)

## Integrações

O módulo de Riscos se integra com outros componentes do Planify:

- **Projetos**: Riscos são associados a projetos específicos
- **Tarefas**: Ações de tratamento podem ser convertidas em tarefas
- **Custos**: Impacto financeiro dos riscos é considerado no orçamento
- **Documentos**: Anexos e evidências relacionados aos riscos
- **Comunicações**: Notificações sobre riscos críticos ou ocorrências

## Melhores Práticas

### Identificação de Riscos

- Realize sessões de brainstorming com a equipe
- Considere diferentes categorias (técnico, financeiro, operacional, etc.)
- Consulte o histórico de projetos similares
- Envolva especialistas de diferentes áreas
- Revise periodicamente para identificar novos riscos

### Avaliação Eficaz

- Use critérios consistentes para probabilidade e impacto
- Considere múltiplas dimensões de impacto (custo, prazo, qualidade)
- Reavalie regularmente conforme o projeto evolui
- Documente as premissas utilizadas na avaliação
- Evite otimismo excessivo nas estimativas

### Tratamento e Monitoramento

- Priorize riscos com base na exposição (probabilidade × impacto)
- Defina claramente responsabilidades para cada risco
- Estabeleça indicadores mensuráveis para monitoramento
- Implemente ações preventivas o quanto antes
- Revise a eficácia das ações implementadas

### Comunicação de Riscos

- Mantenha stakeholders informados sobre riscos críticos
- Inclua análise de riscos nas reuniões de status
- Use visualizações claras para comunicar a situação atual
- Destaque tendências e padrões importantes
- Celebre o tratamento bem-sucedido de riscos

## Próximos Passos

Agora que você conhece o Módulo de Riscos, explore o [Módulo de Custos](/docs/user-guide/modules/costs) para aprender como gerenciar o orçamento e as despesas dos seus projetos.
