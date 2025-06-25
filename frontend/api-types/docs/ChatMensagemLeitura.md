# ChatMensagemLeitura


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**mensagem** | **number** | Mensagem que foi lida | [default to undefined]
**usuario** | **number** | Usuário que leu a mensagem | [default to undefined]
**usuario_nome** | **string** |  | [readonly] [default to undefined]
**lido_em** | **string** | Data e hora em que a mensagem foi lida | [readonly] [default to undefined]

## Example

```typescript
import { ChatMensagemLeitura } from './api';

const instance: ChatMensagemLeitura = {
    id,
    mensagem,
    usuario,
    usuario_nome,
    lido_em,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
