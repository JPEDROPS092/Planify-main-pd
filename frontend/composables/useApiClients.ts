import { 
  AutenticaoApi, 
  ProjetosApi, 
  TarefasApi, 
  EquipesApi, 
  DocumentosApi, 
  CustoApi, 
  RiscosApi, 
  ComunicaoApi,
  UsuriosApi,
  Configuration
} from '~/api-types';
import axios from 'axios';

export const useApiClients = () => {
  const config = useRuntimeConfig();
  
  // Obter token diretamente do localStorage para evitar dependência circular
  const getToken = () => {
    if (process.client) {
      return localStorage.getItem('accessToken');
    }
    return null;
  };

  // Configuração base para todas as APIs
  const configuration = new Configuration({
    basePath: config.public.apiBaseUrl || 'http://localhost:8000',
    accessToken: getToken() || undefined,
  });

  // Instância do axios configurada
  const axiosInstance = axios.create({
    baseURL: config.public.apiBaseUrl || 'http://localhost:8000',
    timeout: 10000,
  });

  // Interceptor para adicionar token automaticamente
  axiosInstance.interceptors.request.use((config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  // Interceptor para lidar com erros de autenticação
  axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response?.status === 401) {
        // Token expirado, limpar dados e redirecionar
        if (process.client) {
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          await navigateTo('/login');
        }
      }
      return Promise.reject(error);
    }
  );

  // Instâncias das APIs
  const authApi = new AutenticaoApi(configuration, undefined, axiosInstance);
  const projectsApi = new ProjetosApi(configuration, undefined, axiosInstance);
  const tasksApi = new TarefasApi(configuration, undefined, axiosInstance);
  const teamsApi = new EquipesApi(configuration, undefined, axiosInstance);
  const documentsApi = new DocumentosApi(configuration, undefined, axiosInstance);
  const costsApi = new CustoApi(configuration, undefined, axiosInstance);
  const risksApi = new RiscosApi(configuration, undefined, axiosInstance);
  const communicationApi = new ComunicaoApi(configuration, undefined, axiosInstance);
  const usersApi = new UsuriosApi(configuration, undefined, axiosInstance);

  return {
    authApi,
    projectsApi,
    tasksApi,
    teamsApi,
    documentsApi,
    costsApi,
    risksApi,
    communicationApi,
    usersApi,
    axiosInstance
  };
};
