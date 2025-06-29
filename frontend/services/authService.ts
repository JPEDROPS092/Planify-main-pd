import type { LoginRequestRequest, RefreshRequestRequest, User } from '~/api-types';
import { AutenticaoApi, UsuriosApi, Configuration } from '~/api-types';
import axios from 'axios';
import { useRuntimeConfig } from '#imports';

export const useAuthService = () => {
  const config = useRuntimeConfig();
  
  // Criar configuração e instâncias diretas para evitar dependência circular
  const configuration = new Configuration({
    basePath: config.public.apiBaseUrl || 'http://localhost:8000',
  });

  const axiosInstance = axios.create({
    baseURL: config.public.apiBaseUrl || 'http://localhost:8000',
    timeout: 10000,
  });

  const authApi = new AutenticaoApi(configuration, undefined, axiosInstance);
  const usersApi = new UsuriosApi(configuration, undefined, axiosInstance);

  /**
   * Realiza login do usuário
   * @param credentials Credenciais de login
   */
  const login = async (credentials: { username: string; password: string }) => {
    // Enviar dados diretamente conforme documentação da API
    const response = await axiosInstance.post('/api/auth/jwt/create/', {
      "username": credentials.username,
      "password": credentials.password
    });
    
    return response.data;
  };

  /**
   * Realiza logout do usuário
   */
  const logout = async () => {
    try {
      await axiosInstance.post('/api/auth/logout/');
    } catch (error) {
      // Mesmo se der erro no backend, limpar dados locais
      console.warn('Erro no logout:', error);
    }
  };

  /**
   * Registra um novo usuário
   * @param userData Dados do usuário para registro
   */
  const register = async (userData: any) => {
    try {
      console.log('Enviando dados de registro para:', '/api/auth/users/');
      console.log('Dados:', userData);
      
      const response = await axiosInstance.post('/api/auth/users/', userData);
      return response.data;
    } catch (error: any) {
      console.error('Erro no registro:', error);
      console.error('Response data:', error.response?.data);
      console.error('Response status:', error.response?.status);
      throw error;
    }
  };

  /**
   * Renova o token de acesso
   * @param refreshToken Token de refresh
   */
  const refreshToken = async (refreshToken: string) => {
    const response = await axiosInstance.post('/api/auth/jwt/refresh/', {
      refresh: refreshToken
    });
    
    return response.data;
  };

  /**
   * Obtém o perfil do usuário atual
   */
  const getUserProfile = async (): Promise<User> => {
    // Configurar token para esta requisição
    const token = typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;
    if (token) {
      axiosInstance.defaults.headers.common['Authorization'] = `JWT ${token}`;
    }
    
    // Usar endpoint de lista de usuários e pegar o primeiro
    const response = await axiosInstance.get('/api/auth/users/');
    
    if (response.data.results && response.data.results.length > 0) {
      return response.data.results[0];
    }
    
    throw new Error('Usuário não encontrado');
  };

  /**
   * Altera a senha do usuário
   * @param oldPassword Senha atual
   * @param newPassword Nova senha
   */
  const changePassword = async (oldPassword: string, newPassword: string) => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;
    if (token) {
      axiosInstance.defaults.headers.common['Authorization'] = `JWT ${token}`;
    }
    
    // Assumindo que existe um endpoint para mudança de senha
    const response = await axiosInstance.post('/api/auth/users/change-password/', {
      old_password: oldPassword,
      new_password: newPassword
    });
    
    return response.data;
  };

  return {
    login,
    logout,
    register,
    refreshToken,
    getUserProfile,
    changePassword
  };
};
