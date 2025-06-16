/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import { BaseHttpRequest } from './core/BaseHttpRequest';
import type { OpenAPIConfig } from './core/OpenAPI';
import { ApiService } from '../services/ApiService';
import { AuthService } from '../services/AuthService';
import { ComentariosService } from '../services/ComentariosService';
import { ComunicacaoService } from '../services/ComunicacaoService';
import { CustoService } from '../services/CustoService';
import { DocumentosService } from '../services/DocumentosService';
import { EquipesService } from '../services/EquipesService';
import { HistoricoService } from '../services/HistoricoService';
import { ProjetosService } from '../services/ProjetosService';
import { RiscosService } from '../services/RiscosService';
import { TarefasService } from '../services/TarefasService';

type HttpRequestConstructor = new (config: OpenAPIConfig) => BaseHttpRequest;
export class PlanifyApiClient {
    public readonly api: ApiService;
    public readonly autenticaO: AuthService;
    public readonly comentarios: ComentariosService;
    public readonly comunicacao: ComunicacaoService;
    public readonly custo: CustoService;
    public readonly documentos: DocumentosService;
    public readonly equipes: EquipesService;
    public readonly historico: HistoricoService;
    public readonly projetos: ProjetosService;
    public readonly riscos: RiscosService;
    public readonly tarefas: TarefasService;
    public readonly request: BaseHttpRequest;
    constructor(config?: Partial<OpenAPIConfig>, HttpRequest: HttpRequestConstructor = BaseHttpRequest as HttpRequestConstructor) {
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
        this.autenticaO = new AuthService(this.request);
        this.comentarios = new ComentariosService(this.request);
        this.comunicacao = new ComunicacaoService(this.request);
        this.custo = new CustoService(this.request);
        this.documentos = new DocumentosService(this.request);
        this.equipes = new EquipesService(this.request);
        this.historico = new HistoricoService(this.request);
        this.projetos = new ProjetosService(this.request);
        this.riscos = new RiscosService(this.request);
        this.tarefas = new TarefasService(this.request);
    }
}

