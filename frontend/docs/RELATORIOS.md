# Módulo de Relatórios de Custos

Este módulo fornece funcionalidades avançadas de relatórios para o sistema de custos do Planify.

## Funcionalidades

### 1. Relatório Mensal
- **Endpoint**: `GET /api/costs/custos/relatorio_mensal/`
- **Descrição**: Exibe gastos mensais com gráfico de linha temporal
- **Funcionalidades**:
  - Visualização de gastos por mês
  - Gráfico de linha interativo
  - Tabela com variação percentual
  - Exportação de dados

### 2. Relatório por Categoria
- **Endpoint**: `GET /api/costs/custos/relatorio_por_categoria/`
- **Descrição**: Análise de gastos distribuídos por categoria
- **Funcionalidades**:
  - Gráfico de pizza (doughnut)
  - Tabela com percentuais
  - Cores diferenciadas por categoria
  - Exportação de dados

### 3. Relatório por Projeto
- **Endpoint**: `GET /api/costs/custos/relatorio_por_projeto/`
- **Descrição**: Comparação de gastos vs orçamento por projeto
- **Funcionalidades**:
  - Gráfico de barras comparativo
  - Indicadores de utilização do orçamento
  - Status visual (Normal/Atenção/Crítico/Excedido)
  - Exportação de dados

## Estrutura de Arquivos

```
frontend/
├── pages/costs/reports.vue          # Página principal de relatórios
├── components/charts/
│   ├── MonthlyChart.vue            # Gráfico mensal
│   ├── CategoryChart.vue           # Gráfico por categoria
│   └── ProjectChart.vue            # Gráfico por projeto
└── docs/RELATORIOS.md              # Esta documentação
```

## Tecnologias Utilizadas

- **Chart.js**: Biblioteca para gráficos interativos
- **Vue Query**: Gerenciamento de estado e cache de dados
- **Tailwind CSS**: Estilização responsiva
- **File-saver**: Exportação de relatórios
- **Iconify**: Ícones

## Como Usar

### Acessando os Relatórios

1. Navegue para a página de custos (`/costs`)
2. Clique no botão "Relatórios" no cabeçalho
3. Selecione a aba desejada (Mensal, Por Categoria, Por Projeto)

### Exportando Dados

Cada relatório possui um botão "Exportar" que permite baixar os dados em formato JSON.

## Componentes de Gráfico

### MonthlyChart.vue
- Gráfico de linha temporal
- Mostra evolução dos gastos ao longo dos meses
- Formatação automática de moeda brasileira

### CategoryChart.vue
- Gráfico de pizza (doughnut)
- Distribuição visual por categorias
- Cores automáticas e legendas

### ProjectChart.vue
- Gráfico de barras comparativo
- Compara gastos reais vs orçamento
- Visualização clara de performance

## Estados da Interface

### Loading
- Spinner animado durante carregamento
- Mensagem informativa

### Error
- Tratamento de erros com mensagens claras
- Botão para tentar novamente

### Empty State
- Mensagens quando não há dados
- Orientações para o usuário

## Responsividade

- Layout adaptável para desktop e mobile
- Gráficos responsivos
- Tabelas com scroll horizontal em telas pequenas

## Integração com API

O módulo utiliza as funções geradas pelo Orval:
- `useCostsCustosRelatorioMensalRetrieve`
- `useCostsCustosRelatorioPorCategoriaRetrieve`
- `useCostsCustosRelatorioPorProjetoRetrieve`

## Melhorias Futuras

- [ ] Filtros por período personalizado
- [ ] Exportação em PDF
- [ ] Relatórios agendados
- [ ] Comparação entre períodos
- [ ] Drill-down nos gráficos
- [ ] Relatórios personalizáveis

## Troubleshooting

### Gráficos não aparecem
- Verifique se Chart.js está instalado
- Confirme se os dados estão no formato correto

### Erro de importação
- Execute `npm install` para instalar dependências
- Verifique se os caminhos dos imports estão corretos

### Dados não carregam
- Verifique conectividade com a API
- Confirme se o usuário tem permissões adequadas
