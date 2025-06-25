export default defineNuxtPlugin(async () => {
  const { initialize } = useAuth();
  
  // Inicializar autenticação no lado do cliente
  await initialize();
});
