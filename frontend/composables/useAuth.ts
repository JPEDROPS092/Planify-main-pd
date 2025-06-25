import { useAuthService } from '~/servicesMock/authService';
import type { User } from '~/api-types/api';

export const useAuth = () => {
  const user = useState<User | null>('user', () => null);
  const token = useState<string | null>('authToken', () => null);
  const isAuthenticated = useState<boolean>('isAuthenticated', () => false);
  const isLoading = useState<boolean>('authLoading', () => true);
  const permissions = useState<string[]>('userPermissions', () => []);
  
  const router = useRouter();
  const authService = useAuthService();
  
  const fetchUser = async () => {
    if (!process.client) return;
    
    const storedToken = localStorage.getItem('accessToken');
    if (!storedToken) {
      isLoading.value = false;
      isAuthenticated.value = false;
      return;
    }
    
    try {
      isLoading.value = true;
      token.value = storedToken;
      const userData = await authService.getUserProfile();
      user.value = userData;
      isAuthenticated.value = true;
      
      // Definir permissões baseadas no usuário
      permissions.value = userData.is_staff ? ['admin'] : ['user'];
    } catch (error) {
      console.error('Erro ao obter perfil do usuário:', error);
      isAuthenticated.value = false;
      user.value = null;
      token.value = null;
      // Limpar token inválido
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    } finally {
      isLoading.value = false;
    }
  };
  
  const login = async (credentials: { username: string; password: string }) => {
    try {
      isLoading.value = true;
      const response = await authService.login(credentials);
      
      // Armazenar tokens
      localStorage.setItem('accessToken', response.access);
      localStorage.setItem('refreshToken', response.refresh);
      token.value = response.access;
      
      // Buscar dados do usuário
      await fetchUser();
      
      return response;
    } catch (error) {
      console.error('Erro no login:', error);
      throw error;
    } finally {
      isLoading.value = false;
    }
  };
  
  const logout = async () => {
    try {
      isLoading.value = true;
      await authService.logout();
      
      // Limpar dados locais
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      user.value = null;
      isAuthenticated.value = false;
      permissions.value = [];
      token.value = null;
      
      // Redirecionar para login
      router.push('/login');
      
      return true;
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  const register = async (userData: any) => {
    try {
      isLoading.value = true;
      const response = await authService.register(userData);
      return response;
    } catch (error) {
      console.error('Erro ao registrar usuário:', error);
      throw error;
    } finally {
      isLoading.value = false;
    }
  };
  
  const hasPermission = (permissionName: string): boolean => {
    return permissions.value.includes(permissionName);
  };
  
  // Função para inicializar autenticação (deve ser chamada manualmente)
  const initialize = async () => {
    if (process.client) {
      await fetchUser();
    }
  };
  
  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    permissions,
    login,
    logout,
    register,
    fetchUser,
    hasPermission,
    initialize
  };
};
