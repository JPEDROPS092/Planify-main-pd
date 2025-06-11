/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ThemePreferenceEnum } from './ThemePreferenceEnum';
export type UserProfileRequest = {
    phone?: string | null;
    profile_picture?: Blob | null;
    theme_preference?: ThemePreferenceEnum;
    email_notifications?: boolean;
    system_notifications?: boolean;
};

