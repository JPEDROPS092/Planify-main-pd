# Alerta

Serializer para o modelo Alerta.  Inclui todos os campos do modelo Alerta. Adiciona campos de leitura para exibir o valor textual dos campos de escolha (\'tipo\', \'status\') e nomes relacionados (projeto, tarefa, resolvedor).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**tipo** | [**AlertaTipoEnum**](AlertaTipoEnum.md) |  | [default to undefined]
**tipo_display** | **string** |  | [readonly] [default to undefined]
**projeto** | **number** |  | [default to undefined]
**projeto_nome** | **string** |  | [readonly] [default to undefined]
**tarefa** | **number** |  | [optional] [default to undefined]
**tarefa_titulo** | **string** |  | [readonly] [default to undefined]
**percentual** | **string** |  | [default to undefined]
**mensagem** | **string** |  | [default to undefined]
**status** | [**AlertaStatusEnum**](AlertaStatusEnum.md) |  | [optional] [default to undefined]
**status_display** | **string** |  | [readonly] [default to undefined]
**data_criacao** | **string** |  | [readonly] [default to undefined]
**data_resolucao** | **string** |  | [readonly] [default to undefined]
**resolvido_por** | **number** |  | [optional] [default to undefined]
**resolvido_por_nome** | **string** |  | [readonly] [default to undefined]

## Example

```typescript
import { Alerta } from './api';

const instance: Alerta = {
    id,
    tipo,
    tipo_display,
    projeto,
    projeto_nome,
    tarefa,
    tarefa_titulo,
    percentual,
    mensagem,
    status,
    status_display,
    data_criacao,
    data_resolucao,
    resolvido_por,
    resolvido_por_nome,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
