/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RoleEnum } from './RoleEnum';
import type { UserProfileRequest } from './UserProfileRequest';
/**
 * Serializer para operações de usuário (leitura, atualização).
 */
export type UserRequest = {
    username: string;
    email: string;
    full_name: string;
    role?: RoleEnum;
    profile?: UserProfileRequest;
    is_active?: boolean;
    password?: string;
};

