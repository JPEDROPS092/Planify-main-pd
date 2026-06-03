/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Permission } from './Permission';
export type AccessProfile = {
    readonly id: number;
    name: string;
    description?: string | null;
    readonly permissions: Array<Permission>;
    readonly created_at: string;
    readonly updated_at: string;
};

