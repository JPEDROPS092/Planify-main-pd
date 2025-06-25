# OrcamentoTarefaRequest

Serializer para o modelo OrcamentoTarefa.  Inclui campos para o orçamento de uma tarefa específica e informações de aprovação. Adiciona campos de leitura para nomes relacionados (aprovador, tarefa, projeto da tarefa) e campos calculados (valor utilizado, valor restante, percentual utilizado).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tarefa** | **number** |  | [default to undefined]
**valor** | **string** |  | [default to undefined]
**aprovado_por** | **number** |  | [optional] [default to undefined]
**observacoes** | **string** |  | [optional] [default to undefined]

## Example

```typescript
import { OrcamentoTarefaRequest } from './api';

const instance: OrcamentoTarefaRequest = {
    tarefa,
    valor,
    aprovado_por,
    observacoes,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
