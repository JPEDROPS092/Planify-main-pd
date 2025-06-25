# ChangePasswordRequest

Serializer para alteração de senha com validação da senha atual.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**old_password** | **string** |  | [default to undefined]
**new_password** | **string** |  | [default to undefined]

## Example

```typescript
import { ChangePasswordRequest } from './api';

const instance: ChangePasswordRequest = {
    old_password,
    new_password,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
