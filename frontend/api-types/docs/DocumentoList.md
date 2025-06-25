# DocumentoList

Serializer simplificado para listagem de documentos

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**projeto** | **number** |  | [default to undefined]
**projeto_nome** | **string** |  | [readonly] [default to undefined]
**tarefa** | **number** |  | [optional] [default to undefined]
**tarefa_titulo** | **string** |  | [readonly] [default to undefined]
**titulo** | **string** |  | [default to undefined]
**tipo** | [**Tipo0e9Enum**](Tipo0e9Enum.md) |  | [optional] [default to undefined]
**tipo_display** | **string** |  | [readonly] [default to undefined]
**versao** | **string** |  | [optional] [default to undefined]
**enviado_por_nome** | **string** |  | [readonly] [default to undefined]
**data_upload** | **string** |  | [readonly] [default to undefined]
**tamanho_arquivo** | **number** | Tamanho em bytes | [default to undefined]
**tipo_arquivo** | **string** | Tipo MIME do arquivo | [default to undefined]

## Example

```typescript
import { DocumentoList } from './api';

const instance: DocumentoList = {
    id,
    projeto,
    projeto_nome,
    tarefa,
    tarefa_titulo,
    titulo,
    tipo,
    tipo_display,
    versao,
    enviado_por_nome,
    data_upload,
    tamanho_arquivo,
    tipo_arquivo,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
