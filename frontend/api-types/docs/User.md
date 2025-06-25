# User

Serializer para operações de usuário (leitura, atualização).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **string** |  | [default to undefined]
**email** | **string** |  | [default to undefined]
**full_name** | **string** |  | [default to undefined]
**role** | [**RoleEnum**](RoleEnum.md) |  | [optional] [default to undefined]
**profile** | [**UserProfile**](UserProfile.md) |  | [optional] [default to undefined]
**id** | **number** |  | [readonly] [default to undefined]
**is_active** | **boolean** |  | [optional] [default to undefined]
**date_joined** | **string** |  | [readonly] [default to undefined]
**access_profiles** | [**Array&lt;UserAccessProfile&gt;**](UserAccessProfile.md) |  | [readonly] [default to undefined]

## Example

```typescript
import { User } from './api';

const instance: User = {
    username,
    email,
    full_name,
    role,
    profile,
    id,
    is_active,
    date_joined,
    access_profiles,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
