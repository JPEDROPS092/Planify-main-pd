/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RoleEnum } from './RoleEnum';
import type { UserProfileRequest } from './UserProfileRequest';
/**
 * Serializer para criação de usuários com validação de senha.
 */
export type UserCreateRequest = {
    username: string;
    email: string;
    full_name: string;
    role?: RoleEnum;
    profile?: UserProfileRequest;
    password: string;
};

