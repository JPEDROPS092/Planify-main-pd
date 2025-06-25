# ChatMensagem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**projeto** | **number** | Projeto ao qual a mensagem pertence | [default to undefined]
**projeto_nome** | **string** |  | [readonly] [default to undefined]
**autor** | **number** | Usuário que enviou a mensagem | [readonly] [default to undefined]
**autor_nome** | **string** |  | [readonly] [default to undefined]
**autor_username** | **string** |  | [readonly] [default to undefined]
**texto** | **string** | Conteúdo da mensagem | [default to undefined]
**anexo** | **string** | Arquivo opcional anexado à mensagem | [optional] [default to undefined]
**enviado_em** | **string** | Data e hora em que a mensagem foi enviada | [readonly] [default to undefined]
**editado** | **boolean** | Indica se a mensagem foi editada após o envio inicial | [readonly] [default to undefined]
**leituras** | [**Array&lt;ChatMensagemLeitura&gt;**](ChatMensagemLeitura.md) |  | [readonly] [default to undefined]

## Example

```typescript
import { ChatMensagem } from './api';

const instance: ChatMensagem = {
    id,
    projeto,
    projeto_nome,
    autor,
    autor_nome,
    autor_username,
    texto,
    anexo,
    enviado_em,
    editado,
    leituras,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
