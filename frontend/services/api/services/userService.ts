/**
 * User Service
 *
 * Delegates to the generated API client (ApiService).
 * Endpoint: /api/auth/users/ (apiAuthUsersList / apiAuthUsersRetrieve / apiAuthUsersMeRetrieve)
 */

import { ApiService } from '~/lib/api-client/services/ApiService';
import type { PaginatedUserList } from '~/lib/api-client/models/PaginatedUserList';
import type { User } from '~/lib/api-client/models/User';

export function useUserService() {
  /**
   * fetchUsers / getAllUsers — list all users (paginated).
   *
   * Call-sites:
   *   - comunicacoes/index.vue:  const { fetchUsers } = useUserService(); response.results
   *   - ProjectTeam.vue:         userService.getAllUsers(); result.results || result
   *
   * Maps to: ApiService.apiAuthUsersList(ordering?, page?, search?)
   */
  async function fetchUsers(params?: {
    ordering?: string;
    page?: number;
    search?: string;
  }): Promise<PaginatedUserList> {
    return ApiService.apiAuthUsersList(
      params?.ordering,
      params?.page,
      params?.search,
    );
  }

  // Alias used by ProjectTeam.vue
  const getAllUsers = fetchUsers;

  /**
   * getUserById — retrieve a single user by numeric ID.
   *
   * Call-sites:
   *   - ProjectRisks.vue:  userService.getUserById(risk.assignee)   → User
   *   - ProjectTasks.vue:  userService.getUserById(task.assignee)   → User
   *
   * Maps to: ApiService.apiAuthUsersRetrieve(id)
   */
  async function getUserById(id: number): Promise<User> {
    return ApiService.apiAuthUsersRetrieve(id);
  }

  /**
   * getMe — retrieve the currently authenticated user.
   *
   * No direct call-site today, but several components import the service
   * alongside useAuth and may need this in the future.
   *
   * Maps to: ApiService.apiAuthUsersMeRetrieve()
   */
  async function getMe(): Promise<User> {
    return ApiService.apiAuthUsersMeRetrieve();
  }

  /**
   * getUsers — alias used by ProjectForm.vue.
   *
   * Call-site:  userService.getUsers()  →  response.data  (array of User)
   *
   * ProjectForm.vue expects `response.data`, so we wrap the paginated
   * result into { data: User[] } to match that expectation.
   *
   * Maps to: ApiService.apiAuthUsersList()
   */
  async function getUsers(): Promise<{ data: User[] }> {
    const paginated = await ApiService.apiAuthUsersList();
    return { data: paginated.results ?? [] };
  }

  return {
    fetchUsers,
    getAllUsers,
    getUserById,
    getMe,
    getUsers,
  };
}
