# Documento


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**projeto** | **number** |  | [default to undefined]
**projeto_nome** | **string** |  | [readonly] [default to undefined]
**tarefa** | **number** |  | [optional] [default to undefined]
**tarefa_titulo** | **string** |  | [readonly] [default to undefined]
**titulo** | **string** |  | [default to undefined]
**descricao** | **string** |  | [optional] [default to undefined]
**tipo** | [**Tipo0e9Enum**](Tipo0e9Enum.md) |  | [optional] [default to undefined]
**tipo_display** | **string** |  | [readonly] [default to undefined]
**arquivo** | **string** |  | [default to undefined]
**tamanho_arquivo** | **number** | Tamanho em bytes | [readonly] [default to undefined]
**tipo_arquivo** | **string** | Tipo MIME do arquivo | [readonly] [default to undefined]
**versao** | **string** |  | [optional] [default to undefined]
**enviado_por** | **number** |  | [optional] [default to undefined]
**enviado_por_nome** | **string** |  | [readonly] [default to undefined]
**data_upload** | **string** |  | [readonly] [default to undefined]
**atualizado_em** | **string** |  | [readonly] [default to undefined]
**comentarios** | [**Array&lt;Comentario&gt;**](Comentario.md) |  | [readonly] [default to undefined]
**historico** | [**Array&lt;HistoricoDocumento&gt;**](HistoricoDocumento.md) |  | [readonly] [default to undefined]

## Example

```typescript
import { Documento } from './api';

const instance: Documento = {
    id,
    projeto,
    projeto_nome,
    tarefa,
    tarefa_titulo,
    titulo,
    descricao,
    tipo,
    tipo_display,
    arquivo,
    tamanho_arquivo,
    tipo_arquivo,
    versao,
    enviado_por,
    enviado_por_nome,
    data_upload,
    atualizado_em,
    comentarios,
    historico,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
