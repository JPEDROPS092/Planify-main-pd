<template>
  <div class="fixed top-4 right-4 z-50 space-y-4">
    <Notification
      v-for="notification in notifications"
      :key="notification.id"
      :type="notification.type"
      :message="notification.message"
      :title="notification.title"
      :duration="notification.duration"
      :auto-close="notification.autoClose"
      @close="removeNotification(notification.id)"
    />
  </div>
</template>

<script setup lang="ts">
import { useNotification } from '~/stores/composables/useNotification';
import Notification from './Notification.vue';

const { notifications, remove: removeNotification } = useNotification();
</script>
