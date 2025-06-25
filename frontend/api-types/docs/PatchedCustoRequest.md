# PatchedCustoRequest

Serializer detalhado para o modelo Custo.  Inclui todos os campos do modelo Custo e adiciona campos de leitura para exibir nomes relacionados de outros modelos (usuário, projeto, tarefa, categoria) e o valor textual dos campos de escolha (\'tipo\').

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**projeto** | **number** |  | [optional] [default to undefined]
**tarefa** | **number** |  | [optional] [default to undefined]
**categoria** | **number** |  | [optional] [default to undefined]
**descricao** | **string** |  | [optional] [default to undefined]
**valor** | **string** |  | [optional] [default to undefined]
**tipo** | [**CustoTipoEnum**](CustoTipoEnum.md) |  | [optional] [default to undefined]
**data** | **string** |  | [optional] [default to undefined]
**comprovante** | **File** |  | [optional] [default to undefined]
**observacoes** | **string** |  | [optional] [default to undefined]
**criado_por** | **number** |  | [optional] [default to undefined]

## Example

```typescript
import { PatchedCustoRequest } from './api';

const instance: PatchedCustoRequest = {
    projeto,
    tarefa,
    categoria,
    descricao,
    valor,
    tipo,
    data,
    comprovante,
    observacoes,
    criado_por,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
