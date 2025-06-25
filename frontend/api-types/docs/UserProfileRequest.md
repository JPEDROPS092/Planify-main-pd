# UserProfileRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**phone** | **string** |  | [optional] [default to undefined]
**profile_picture** | **File** |  | [optional] [default to undefined]
**theme_preference** | [**ThemePreferenceEnum**](ThemePreferenceEnum.md) |  | [optional] [default to undefined]
**email_notifications** | **boolean** |  | [optional] [default to undefined]
**system_notifications** | **boolean** |  | [optional] [default to undefined]

## Example

```typescript
import { UserProfileRequest } from './api';

const instance: UserProfileRequest = {
    phone,
    profile_picture,
    theme_preference,
    email_notifications,
    system_notifications,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
