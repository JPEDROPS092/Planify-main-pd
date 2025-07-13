<template>
  <div class="container mx-auto p-8">
    <h1 class="text-2xl font-bold mb-4">API Debug Test</h1>

    <div class="space-y-4">
      <button
        @click="testAuth"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Test Auth Token
      </button>

      <button
        @click="testTasksList"
        class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
      >
        Test Tasks List
      </button>

      <button
        @click="testTaskDetail"
        class="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
      >
        Test Task Detail (ID: 129)
      </button>

      <button
        @click="testSpecificTask"
        class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
      >
        Test Task Detail (Custom ID)
      </button>

      <input
        v-model="customTaskId"
        type="number"
        placeholder="Enter task ID"
        class="px-3 py-2 border rounded"
      />

      <div v-if="results" class="mt-4 p-4 bg-gray-100 dark:bg-gray-800 rounded">
        <h3 class="font-bold mb-2">Results:</h3>
        <pre class="whitespace-pre-wrap text-sm overflow-auto max-h-96">{{
          results
        }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { debugAuthToken } from "@/utils/auth-debug";

definePageMeta({
  middleware: "auth",
});

const results = ref("");
const customTaskId = ref(129);

const testAuth = () => {
  debugAuthToken();
  results.value = "Check console for auth token details";
};

const testTasksList = async () => {
  try {
    const token =
      localStorage.getItem("auth-token") ||
      sessionStorage.getItem("auth-token");
    console.log(
      "Testing tasks list with token:",
      token?.substring(0, 20) + "..."
    );

    const response = await $fetch("/api/tasks/tarefas/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    results.value = JSON.stringify(response, null, 2);
  } catch (error: any) {
    console.error("Tasks list error:", error);
    results.value = `Error: ${error.message}\n\nDetails:\n${JSON.stringify(
      {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
      },
      null,
      2
    )}`;
  }
};

const testTaskDetail = async () => {
  await testSpecificTaskId(129);
};

const testSpecificTask = async () => {
  await testSpecificTaskId(customTaskId.value);
};

const testSpecificTaskId = async (taskId: number) => {
  try {
    const token =
      localStorage.getItem("auth-token") ||
      sessionStorage.getItem("auth-token");
    console.log(
      `Testing task ${taskId} with token:`,
      token?.substring(0, 20) + "..."
    );

    const response = await $fetch(`/api/tasks/tarefas/${taskId}/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    results.value = JSON.stringify(response, null, 2);
  } catch (error: any) {
    console.error(`Task ${taskId} error:`, error);
    results.value = `Error accessing task ${taskId}:\n${error.message}\n\nDetails:\n${JSON.stringify(
      {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        headers: error.response?.headers,
      },
      null,
      2
    )}`;
  }
};
</script>
