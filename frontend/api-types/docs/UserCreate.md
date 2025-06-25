# UserCreate

Serializer para criação de usuários com validação de senha.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **string** |  | [default to undefined]
**email** | **string** |  | [default to undefined]
**full_name** | **string** |  | [default to undefined]
**role** | [**RoleEnum**](RoleEnum.md) |  | [optional] [default to undefined]
**profile** | [**UserProfile**](UserProfile.md) |  | [optional] [default to undefined]

## Example

```typescript
import { UserCreate } from './api';

const instance: UserCreate = {
    username,
    email,
    full_name,
    role,
    profile,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
