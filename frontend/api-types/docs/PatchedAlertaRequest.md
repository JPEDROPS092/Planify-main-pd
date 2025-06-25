# PatchedAlertaRequest

Serializer para o modelo Alerta.  Inclui todos os campos do modelo Alerta. Adiciona campos de leitura para exibir o valor textual dos campos de escolha (\'tipo\', \'status\') e nomes relacionados (projeto, tarefa, resolvedor).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tipo** | [**AlertaTipoEnum**](AlertaTipoEnum.md) |  | [optional] [default to undefined]
**projeto** | **number** |  | [optional] [default to undefined]
**tarefa** | **number** |  | [optional] [default to undefined]
**percentual** | **string** |  | [optional] [default to undefined]
**mensagem** | **string** |  | [optional] [default to undefined]
**status** | [**AlertaStatusEnum**](AlertaStatusEnum.md) |  | [optional] [default to undefined]
**resolvido_por** | **number** |  | [optional] [default to undefined]

## Example

```typescript
import { PatchedAlertaRequest } from './api';

const instance: PatchedAlertaRequest = {
    tipo,
    projeto,
    tarefa,
    percentual,
    mensagem,
    status,
    resolvido_por,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
