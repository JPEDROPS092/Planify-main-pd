# Custo

Serializer detalhado para o modelo Custo.  Inclui todos os campos do modelo Custo e adiciona campos de leitura para exibir nomes relacionados de outros modelos (usuário, projeto, tarefa, categoria) e o valor textual dos campos de escolha (\'tipo\').

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**projeto** | **number** |  | [default to undefined]
**projeto_nome** | **string** |  | [readonly] [default to undefined]
**tarefa** | **number** |  | [optional] [default to undefined]
**tarefa_titulo** | **string** |  | [readonly] [default to undefined]
**categoria** | **number** |  | [optional] [default to undefined]
**categoria_nome** | **string** |  | [readonly] [default to undefined]
**descricao** | **string** |  | [default to undefined]
**valor** | **string** |  | [default to undefined]
**tipo** | [**CustoTipoEnum**](CustoTipoEnum.md) |  | [optional] [default to undefined]
**tipo_display** | **string** |  | [readonly] [default to undefined]
**data** | **string** |  | [default to undefined]
**comprovante** | **string** |  | [optional] [default to undefined]
**observacoes** | **string** |  | [optional] [default to undefined]
**criado_por** | **number** |  | [optional] [default to undefined]
**criado_por_nome** | **string** |  | [readonly] [default to undefined]
**criado_em** | **string** |  | [readonly] [default to undefined]
**atualizado_em** | **string** |  | [readonly] [default to undefined]

## Example

```typescript
import { Custo } from './api';

const instance: Custo = {
    id,
    projeto,
    projeto_nome,
    tarefa,
    tarefa_titulo,
    categoria,
    categoria_nome,
    descricao,
    valor,
    tipo,
    tipo_display,
    data,
    comprovante,
    observacoes,
    criado_por,
    criado_por_nome,
    criado_em,
    atualizado_em,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
