<template>
  <div v-if="showDebugPanel" class="fixed bottom-4 right-4 z-50">
    <div
      class="bg-gray-900 text-white p-4 rounded-lg shadow-lg max-w-md max-h-96 overflow-y-auto"
    >
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-lg font-bold">🔧 Auth Debug Panel</h3>
        <button
          @click="showDebugPanel = false"
          class="text-gray-400 hover:text-white"
        >
          ✕
        </button>
      </div>

      <div class="space-y-2 text-sm">
        <div>
          <strong>Token Status:</strong>
          <span :class="tokenInfo?.valid ? 'text-green-400' : 'text-red-400'">
            {{ tokenInfo?.valid ? "✅ Valid" : "❌ Invalid/Missing" }}
          </span>
        </div>

        <div v-if="tokenInfo?.payload">
          <strong>User:</strong> {{ tokenInfo.payload.username }} (ID:
          {{ tokenInfo.payload.user_id }})
        </div>

        <div v-if="tokenInfo?.payload">
          <strong>Roles:</strong>
          <div class="ml-2">
            <div v-if="tokenInfo.payload.is_superuser" class="text-purple-400">
              🔮 Superuser
            </div>
            <div v-if="tokenInfo.payload.is_staff" class="text-blue-400">
              👨‍💼 Staff
            </div>
            <div
              v-if="tokenInfo.payload.groups?.length"
              class="text-yellow-400"
            >
              👥 Groups: {{ tokenInfo.payload.groups.join(", ") }}
            </div>
          </div>
        </div>

        <div v-if="tokenInfo?.payload?.permissions">
          <strong>Permissions:</strong>
          <div class="ml-2 max-h-20 overflow-y-auto">
            <div
              v-for="perm in tokenInfo.payload.permissions"
              :key="perm"
              class="text-xs text-gray-300"
            >
              • {{ perm }}
            </div>
          </div>
        </div>

        <div v-if="tokenInfo?.payload?.exp">
          <strong>Expires:</strong>
          <span :class="tokenInfo.expired ? 'text-red-400' : 'text-green-400'">
            {{ formatDate(tokenInfo.payload.exp) }}
          </span>
        </div>

        <div class="pt-2 border-t border-gray-700">
          <button
            @click="runDebugTests"
            class="bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded text-sm"
            :disabled="isRunningTests"
          >
            {{ isRunningTests ? "🔄 Running..." : "🧪 Run Tests" }}
          </button>

          <button
            @click="copyDebugInfo"
            class="bg-green-600 hover:bg-green-700 px-3 py-1 rounded text-sm ml-2"
          >
            📋 Copy Info
          </button>
        </div>

        <div v-if="debugResults.length" class="pt-2 border-t border-gray-700">
          <strong>Test Results:</strong>
          <div class="max-h-32 overflow-y-auto">
            <div
              v-for="result in debugResults"
              :key="result.id"
              class="text-xs mt-1"
            >
              <span :class="result.success ? 'text-green-400' : 'text-red-400'">
                {{ result.success ? "✅" : "❌" }}
              </span>
              {{ result.message }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Toggle button -->
  <button
    v-if="!showDebugPanel"
    @click="showDebugPanel = true"
    class="fixed bottom-4 right-4 z-40 bg-red-600 hover:bg-red-700 text-white p-2 rounded-full shadow-lg"
    title="Show Auth Debug Panel"
  >
    🔧
  </button>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import {
  debugAuthToken,
  testTaskAPIDirectly,
  diagnoseTaskAccess,
} from "@/utils/auth-debug";

const showDebugPanel = ref(false);
const tokenInfo = ref<any>(null);
const isRunningTests = ref(false);
const debugResults = ref<
  Array<{ id: string; success: boolean; message: string }>
>([]);

const props = defineProps<{
  taskId?: number;
}>();

onMounted(() => {
  refreshTokenInfo();

  // Auto-show debug panel if there are auth issues in dev mode
  if (!tokenInfo.value?.valid || tokenInfo.value?.expired) {
    showDebugPanel.value = true;
  }
});

const refreshTokenInfo = () => {
  const authInfo = debugAuthToken();
  if (authInfo) {
    tokenInfo.value = {
      valid: true,
      token: authInfo.token,
      payload: authInfo.payload,
      expired:
        authInfo.payload?.exp && authInfo.payload.exp * 1000 < Date.now(),
    };
  } else {
    tokenInfo.value = { valid: false };
  }
};

const formatDate = (timestamp: number) => {
  return new Date(timestamp * 1000).toLocaleString();
};

const runDebugTests = async () => {
  isRunningTests.value = true;
  debugResults.value = [];

  try {
    // Test 1: Token validation
    refreshTokenInfo();
    debugResults.value.push({
      id: "token",
      success: tokenInfo.value?.valid && !tokenInfo.value?.expired,
      message: `Token: ${tokenInfo.value?.valid ? "Valid" : "Invalid"} ${tokenInfo.value?.expired ? "(Expired)" : ""}`,
    });

    // Test 2: If taskId provided, test task access
    if (props.taskId) {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/tasks/tarefas/${props.taskId}/`,
          {
            headers: {
              Authorization: `Bearer ${tokenInfo.value?.token}`,
              "Content-Type": "application/json",
            },
          }
        );

        debugResults.value.push({
          id: "task-access",
          success: response.ok,
          message: `Task ${props.taskId}: ${response.status} ${response.statusText}`,
        });

        if (!response.ok && tokenInfo.value?.payload) {
          await diagnoseTaskAccess(props.taskId, tokenInfo.value.payload);
        }
      } catch (error) {
        debugResults.value.push({
          id: "task-access",
          success: false,
          message: `Task ${props.taskId}: Network error - ${error instanceof Error ? error.message : "Unknown error"}`,
        });
      }
    }

    // Test 3: Basic API connectivity
    try {
      const response = await fetch("http://127.0.0.1:8000/api/auth/user/", {
        headers: {
          Authorization: `Bearer ${tokenInfo.value?.token}`,
          "Content-Type": "application/json",
        },
      });

      debugResults.value.push({
        id: "api-connectivity",
        success: response.ok,
        message: `API Connectivity: ${response.status} ${response.statusText}`,
      });
    } catch (error) {
      debugResults.value.push({
        id: "api-connectivity",
        success: false,
        message: `API: Network error - ${error instanceof Error ? error.message : "Unknown error"}`,
      });
    }
  } finally {
    isRunningTests.value = false;
  }
};

const copyDebugInfo = () => {
  const info = {
    timestamp: new Date().toISOString(),
    tokenValid: tokenInfo.value?.valid,
    tokenExpired: tokenInfo.value?.expired,
    user: tokenInfo.value?.payload
      ? {
          id: tokenInfo.value.payload.user_id,
          username: tokenInfo.value.payload.username,
          email: tokenInfo.value.payload.email,
          is_staff: tokenInfo.value.payload.is_staff,
          is_superuser: tokenInfo.value.payload.is_superuser,
          groups: tokenInfo.value.payload.groups,
          permissions: tokenInfo.value.payload.permissions,
        }
      : null,
    taskId: props.taskId,
    testResults: debugResults.value,
  };

  navigator.clipboard.writeText(JSON.stringify(info, null, 2));
  alert("Debug info copied to clipboard!");
};
</script>
