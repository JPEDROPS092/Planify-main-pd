# CustoList

Serializer simplificado para listagem de custos.  Projetado para exibir uma visão concisa dos custos, ideal para listas ou tabelas onde nem todos os detalhes do Custo são necessários. Inclui campos de leitura para nomes relacionados e o valor \'display\' do tipo.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**projeto** | **number** |  | [default to undefined]
**projeto_nome** | **string** |  | [readonly] [default to undefined]
**tarefa** | **number** |  | [optional] [default to undefined]
**tarefa_titulo** | **string** |  | [readonly] [default to undefined]
**categoria_nome** | **string** |  | [readonly] [default to undefined]
**descricao** | **string** |  | [default to undefined]
**valor** | **string** |  | [default to undefined]
**tipo_display** | **string** |  | [readonly] [default to undefined]
**data** | **string** |  | [default to undefined]

## Example

```typescript
import { CustoList } from './api';

const instance: CustoList = {
    id,
    projeto,
    projeto_nome,
    tarefa,
    tarefa_titulo,
    categoria_nome,
    descricao,
    valor,
    tipo_display,
    data,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
