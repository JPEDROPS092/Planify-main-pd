/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BaseHttpRequest } from './core/BaseHttpRequest';
import type { OpenAPIConfig } from './core/OpenAPI';
import { AxiosHttpRequest } from './core/AxiosHttpRequest';
import { ApiService } from './services/ApiService';
import { AutenticaOService } from './services/AutenticaOService';
import { ComentRiosService } from './services/ComentRiosService';
import { ComunicaOService } from './services/ComunicaOService';
import { CustoService } from './services/CustoService';
import { DocumentosService } from './services/DocumentosService';
import { EquipesService } from './services/EquipesService';
import { HistRicoService } from './services/HistRicoService';
import { ProjetosService } from './services/ProjetosService';
import { RiscosService } from './services/RiscosService';
import { TarefasService } from './services/TarefasService';
type HttpRequestConstructor = new (config: OpenAPIConfig) => BaseHttpRequest;
export class PlanifyApiClient.ts {
    public readonly api: ApiService;
    public readonly autenticaO: AutenticaOService;
    public readonly comentRios: ComentRiosService;
    public readonly comunicaO: ComunicaOService;
    public readonly custo: CustoService;
    public readonly documentos: DocumentosService;
    public readonly equipes: EquipesService;
    public readonly histRico: HistRicoService;
    public readonly projetos: ProjetosService;
    public readonly riscos: RiscosService;
    public readonly tarefas: TarefasService;
    public readonly request: BaseHttpRequest;
    constructor(config?: Partial<OpenAPIConfig>, HttpRequest: HttpRequestConstructor = AxiosHttpRequest) {
        this.request = new HttpRequest({
            BASE: config?.BASE ?? '',
            VERSION: config?.VERSION ?? '1.0.0',
            WITH_CREDENTIALS: config?.WITH_CREDENTIALS ?? false,
            CREDENTIALS: config?.CREDENTIALS ?? 'include',
            TOKEN: config?.TOKEN,
            USERNAME: config?.USERNAME,
            PASSWORD: config?.PASSWORD,
            HEADERS: config?.HEADERS,
            ENCODE_PATH: config?.ENCODE_PATH,
        });
        this.api = new ApiService(this.request);
        this.autenticaO = new AutenticaOService(this.request);
        this.comentRios = new ComentRiosService(this.request);
        this.comunicaO = new ComunicaOService(this.request);
        this.custo = new CustoService(this.request);
        this.documentos = new DocumentosService(this.request);
        this.equipes = new EquipesService(this.request);
        this.histRico = new HistRicoService(this.request);
        this.projetos = new ProjetosService(this.request);
        this.riscos = new RiscosService(this.request);
        this.tarefas = new TarefasService(this.request);
    }
}

