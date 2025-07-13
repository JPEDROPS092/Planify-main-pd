export const debugAuthToken = () => {
  const token =
    localStorage.getItem("auth-token") || sessionStorage.getItem("auth-token");

  if (!token) {
    console.warn("No auth token found");
    return null;
  }

  console.log("Auth token found:", token.substring(0, 50) + "...");

  // If it's a JWT token, decode it (basic decode, not verification)
  if (token.includes(".")) {
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      console.log("Full Token payload:", payload);
      console.log("Token payload summary:", {
        user_id: payload.user_id,
        username: payload.username,
        email: payload.email,
        is_staff: payload.is_staff,
        is_superuser: payload.is_superuser,
        exp: payload.exp ? new Date(payload.exp * 1000) : "No expiration",
        iat: payload.iat ? new Date(payload.iat * 1000) : "No issued at",
        permissions: payload.permissions || "No permissions in token",
        groups: payload.groups || "No groups in token",
      });

      // Check if token is expired
      if (payload.exp && payload.exp * 1000 < Date.now()) {
        console.error("🔴 Token is expired!");
        return null;
      } else {
        console.log("✅ Token is valid and not expired");
      }

      return { token, payload };
    } catch (e) {
      console.error("Could not decode token payload:", e);
    }
  }

  return { token, payload: null };
};

export const checkTaskPermissions = (taskId: number) => {
  console.log(`🔍 Checking permissions for task ${taskId}`);
  const authInfo = debugAuthToken();

  if (!authInfo) {
    console.error("❌ No valid token available");
    return;
  }

  const { token, payload } = authInfo;

  // Add detailed permission analysis
  console.log("🔑 User permissions summary:", {
    isStaff: payload?.is_staff,
    isSuperuser: payload?.is_superuser,
    userId: payload?.user_id,
    userGroups: payload?.groups,
    permissions: payload?.permissions || [],
  });

  // Check for task-related permissions
  const taskPermissions =
    payload?.permissions?.filter(
      (p: string) =>
        p.includes("task") ||
        p.includes("tarefa") ||
        p.includes("view") ||
        p.includes("change") ||
        p.includes("add") ||
        p.includes("delete")
    ) || [];

  if (taskPermissions.length > 0) {
    console.log("📋 Task-related permissions found:", taskPermissions);
  } else {
    console.warn("⚠️ No explicit task permissions found in token");
  }

  // Check for team/project permissions that might affect task access
  if (payload?.team_permissions) {
    console.log("👥 Team permissions:", payload.team_permissions);
  }
  if (payload?.project_permissions) {
    console.log("📁 Project permissions:", payload.project_permissions);
  }
};

export const testTaskAPIDirectly = async (taskId: number) => {
  console.log(`🧪 Testing direct API call to task ${taskId}`);

  const authInfo = debugAuthToken();
  if (!authInfo?.token) {
    console.error("❌ No token available for direct API test");
    return;
  }

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/tasks/tarefas/${taskId}/`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${authInfo.token}`,
          "Content-Type": "application/json",
        },
      }
    );

    console.log(
      `📡 Direct API Response Status: ${response.status} ${response.statusText}`
    );

    if (!response.ok) {
      const errorText = await response.text();
      console.error("❌ Direct API Error Response:", errorText);
      try {
        const errorJson = JSON.parse(errorText);
        console.error("📋 Error Details:", errorJson);

        // Provide troubleshooting suggestions for 403 errors
        if (response.status === 403) {
          console.log("🔧 TROUBLESHOOTING SUGGESTIONS FOR 403 ERROR:");
          console.log("1. Check if you are the task owner or assignee");
          console.log("2. Verify you have 'view_tarefa' permission");
          console.log(
            "3. Check if the task is in a project you have access to"
          );
          console.log("4. Confirm you are in the correct team for this task");
          console.log("5. Contact admin if you believe you should have access");

          // Try to fetch user's current projects/teams
          await diagnoseTaskAccess(taskId, authInfo.payload);
        }
      } catch (e) {
        console.error("📋 Error Text:", errorText);
      }
    } else {
      const data = await response.json();
      console.log("✅ Direct API Success:", data);
      console.log("📋 Task details:", {
        id: data.id,
        titulo: data.titulo,
        criado_por: data.criado_por,
        responsavel: data.responsavel,
        projeto: data.projeto,
        status: data.status,
      });
    }
  } catch (error) {
    console.error("🚨 Direct API Call Failed:", error);
  }
};

export const diagnoseTaskAccess = async (taskId: number, userPayload: any) => {
  console.log(`🔍 Diagnosing task access for task ${taskId}...`);

  try {
    // Try to get user's projects
    const projectsResponse = await fetch(
      "http://127.0.0.1:8000/api/projetos/projetos/",
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("auth-token") || sessionStorage.getItem("auth-token")}`,
          "Content-Type": "application/json",
        },
      }
    );

    if (projectsResponse.ok) {
      const projects = await projectsResponse.json();
      console.log(
        "📁 User's accessible projects:",
        projects.results || projects
      );
    } else {
      console.log("⚠️ Could not fetch user's projects");
    }

    // Try to get user's teams
    const teamsResponse = await fetch(
      "http://127.0.0.1:8000/api/equipes/equipes/",
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("auth-token") || sessionStorage.getItem("auth-token")}`,
          "Content-Type": "application/json",
        },
      }
    );

    if (teamsResponse.ok) {
      const teams = await teamsResponse.json();
      console.log("👥 User's teams:", teams.results || teams);
    } else {
      console.log("⚠️ Could not fetch user's teams");
    }
  } catch (error) {
    console.error("🚨 Error during access diagnosis:", error);
  }
};
