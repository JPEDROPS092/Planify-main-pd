import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { useToast } from '~/composables/useToast';

export const useApiClient = (): AxiosInstance => {
  const config = useRuntimeConfig();
  const router = useRouter();
  const { toast } = useToast();
  
  const apiClient = axios.create({
    baseURL: config.public.apiBase,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Adicionar token de autenticação
  apiClient.interceptors.request.use((config: AxiosRequestConfig) => {
    // Verificar se estamos no cliente
    if (process.client) {
      const token = localStorage.getItem('accessToken');
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  });

  // Tratamento de erros e refresh token
  apiClient.interceptors.response.use(
    (response: AxiosResponse) => response,
    async (error: AxiosError) => {
      const originalRequest = error.config as any;
      
      // Se o erro for 401 e não for uma tentativa de refresh token
      if (error.response?.status === 401 && !originalRequest._retry && originalRequest.url !== 'auth/token/refresh/') {
        originalRequest._retry = true;
        
        try {
          if (!process.client) {
            throw new Error('Not in client');
          }
          
          const refreshToken = localStorage.getItem('refreshToken');
          
          if (!refreshToken) {
            throw new Error('No refresh token');
          }
          
          // Tenta obter um novo token de acesso
          const response = await axios.post(`${config.public.apiBase}auth/token/refresh/`, {
            refresh: refreshToken
          });
          
          const { access } = response.data;
          localStorage.setItem('accessToken', access);
          
          // Reenviar a requisição original
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return apiClient(originalRequest);
        } catch (err) {
          // Se falhar, logout e redireciona para login
          if (process.client) {
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            
            toast({
              title: 'Sessão expirada',
              description: 'Por favor, faça login novamente.',
              variant: 'destructive'
            });
            
            router.push('/login');
          }
          return Promise.reject(error);
        }
      }
      
      // Para outros erros, exibe mensagem
      if (error.response?.data?.detail) {
        toast({
          title: 'Erro',
          description: error.response.data.detail,
          variant: 'destructive'
        });
      } else if (error.message) {
        toast({
          title: 'Erro',
          description: error.message,
          variant: 'destructive'
        });
      }
      
      return Promise.reject(error);
    }
  );

  return apiClient;
};
