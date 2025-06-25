# PatchedUserRequest

Serializer para operações de usuário (leitura, atualização).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **string** |  | [optional] [default to undefined]
**email** | **string** |  | [optional] [default to undefined]
**full_name** | **string** |  | [optional] [default to undefined]
**role** | [**RoleEnum**](RoleEnum.md) |  | [optional] [default to undefined]
**profile** | [**UserProfileRequest**](UserProfileRequest.md) |  | [optional] [default to undefined]
**is_active** | **boolean** |  | [optional] [default to undefined]
**password** | **string** |  | [optional] [default to undefined]

## Example

```typescript
import { PatchedUserRequest } from './api';

const instance: PatchedUserRequest = {
    username,
    email,
    full_name,
    role,
    profile,
    is_active,
    password,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
