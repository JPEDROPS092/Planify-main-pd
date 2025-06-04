<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const navigateToSignup = () => {
  router.push('/auth/registro');
};
</script>

<style scoped>
/* Estilos para CTA, se necessário */
</style>