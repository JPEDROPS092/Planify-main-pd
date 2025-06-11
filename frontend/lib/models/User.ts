/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RoleEnum } from './RoleEnum';
import type { UserAccessProfile } from './UserAccessProfile';
import type { UserProfile } from './UserProfile';
/**
 * Serializer para operações de usuário (leitura, atualização).
 */
export type User = {
    username: string;
    email: string;
    full_name: string;
    role?: RoleEnum;
    profile?: UserProfile;
    readonly id: number;
    is_active?: boolean;
    readonly date_joined: string;
    readonly access_profiles: Array<UserAccessProfile>;
};

