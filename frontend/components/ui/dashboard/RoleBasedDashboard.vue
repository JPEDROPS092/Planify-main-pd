<template>
  <div>
    <!-- Dashboard baseado no papel do usuário -->
    <AdminDashboard v-if="userRole === 'ADMIN'" />
    <ProjectManagerDashboard v-else-if="userRole === 'PROJECT_MANAGER'" />
    <TeamLeaderDashboard v-else-if="userRole === 'TEAM_LEADER'" />
    <TeamMemberDashboard v-else-if="userRole === 'TEAM_MEMBER'" />
    <StakeholderDashboard v-else-if="userRole === 'STAKEHOLDER'" />
    <AuditorDashboard v-else-if="userRole === 'AUDITOR'" />
    
    <!-- Dashboard padrão caso o papel não seja reconhecido -->
    <div v-else class="flex flex-col items-center justify-center py-12">
      <AlertTriangle class="h-12 w-12 text-yellow-500" />
      <h2 class="mt-4 text-xl font-semibold">Papel de usuário não reconhecido</h2>
      <p class="mt-2 text-center text-muted-foreground">
        Não foi possível determinar seu papel no sistema. Por favor, entre em contato com o administrador.
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { AlertTriangle } from 'lucide-vue-next'
import AdminDashboard from './AdminDashboard.vue'
import ProjectManagerDashboard from './ProjectManagerDashboard.vue'
import TeamLeaderDashboard from './TeamLeaderDashboard.vue'
import TeamMemberDashboard from './TeamMemberDashboard.vue'
import StakeholderDashboard from './StakeholderDashboard.vue'
import AuditorDashboard from './AuditorDashboard.vue'

// Importar o composable de autenticação
const { user, userRole } = useAuth()
</script>
