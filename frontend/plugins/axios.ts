import axios from "axios";
import { useAuth } from "~/composables/useAuth";

export default defineNuxtPlugin(() => {
  const router = useRouter();

  // Use a apiBase do runtimeConfig para o baseURL do Axios
  const config = useRuntimeConfig();
  axios.defaults.baseURL = config.public.apiBase.replace(
    "http://localhost:8000"
  ); // ex: http://localhost:8000

  // Flag para evitar loop de refresh
  let isRefreshing = false;
  // Fila para requisições que falharam enquanto o token era atualizado
  let failedQueue: Array<{
    resolve: (token: string) => void;
    reject: (error: any) => void;
  }> = [];

  const processQueue = (error: any, token: string | null = null) => {
    failedQueue.forEach((prom) => {
      if (error) {
        prom.reject(error);
      } else {
        prom.resolve(token as string);
      }
    });
    failedQueue = [];
  };

  // --- INTERCEPTADOR DE REQUISIÇÃO (REQUEST) ---
  axios.interceptors.request.use(
    (config) => {
      // Adiciona o token em todas as requisições, se ele existir
      if (typeof window !== "undefined") {
        const token = localStorage.getItem("access_token");
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // --- INTERCEPTADOR DE RESPOSTA (RESPONSE) ---
  axios.interceptors.response.use(
    (response) => {
      // Se a resposta for bem-sucedida, apenas a retorna.
      return response;
    },
    async (error) => {
      const originalRequest = error.config;

      // Se o erro for 401 (Não Autorizado) e não for uma tentativa de refresh que falhou
      if (error.response?.status === 401 && !originalRequest._retry) {
        if (isRefreshing) {
          // Se já estivermos atualizando o token, adicionamos a requisição na fila de espera
          return new Promise(function (resolve, reject) {
            failedQueue.push({ resolve, reject });
          }).then((token) => {
            originalRequest.headers["Authorization"] = "Bearer " + token;
            return axios(originalRequest);
          });
        }

        originalRequest._retry = true;
        isRefreshing = true;

        const { refreshToken, logout } = useAuth();

        try {
          // Tenta obter um novo access token usando o refreshToken
          await refreshToken();

          const newAccessToken = localStorage.getItem("access_token");
          axios.defaults.headers.common["Authorization"] =
            "Bearer " + newAccessToken;

          // Processa a fila de requisições que estavam esperando
          processQueue(null, newAccessToken);

          // Tenta novamente a requisição original que falhou
          return axios(originalRequest);
        } catch (refreshError) {
          // Se o refresh falhar (ex: refresh token inválido), desloga o usuário
          processQueue(refreshError, null);
          await logout();
          router.push("/login");
          return Promise.reject(refreshError);
        } finally {
          isRefreshing = false;
        }
      }

      // Para qualquer outro erro, apenas o retorna
      return Promise.reject(error);
    }
  );
});
