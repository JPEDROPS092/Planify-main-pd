/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ActionEnum } from './ActionEnum';
import type { ModuleEnum } from './ModuleEnum';
export type Permission = {
    readonly id: number;
    module: ModuleEnum;
    readonly module_display: string;
    action: ActionEnum;
    readonly action_display: string;
};

