<template>
  <NuxtLayout name="dashboard">
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold tracking-tight">Projetos</h1>
        <button
          @click="openNewProjectModal"
          class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-4 w-4 mr-2"
          >
            <path d="M5 12h14"></path>
            <path d="M12 5v14"></path>
          </svg>
          Novo Projeto
        </button>
      </div>

      <!-- Filtros -->
      <div class="flex flex-wrap gap-4">
        <div class="relative w-64">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar projetos..."
            class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="absolute right-3 top-2.5 h-4 w-4 text-gray-400"
          >
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.3-4.3"></path>
          </svg>
        </div>
        <select
          v-model="statusFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          <option value="">Todos os status</option>
          <option value="PLANEJADO">Planejado</option>
          <option value="EM_ANDAMENTO">Em Andamento</option>
          <option value="PAUSADO">Pausado</option>
          <option value="CONCLUIDO">Concluído</option>
          <option value="CANCELADO">Cancelado</option>
        </select>
        <select
          v-model="priorityFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          <option value="">Todas as prioridades</option>
          <option value="BAIXA">Baixa</option>
          <option value="MEDIA">Média</option>
          <option value="ALTA">Alta</option>
        </select>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center py-8">
        <div
          class="h-8 w-8 animate-spin rounded-full border-2 border-blue-600 border-t-transparent"
        ></div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="rounded-md bg-red-50 p-4 text-red-700">
        <p>{{ error }}</p>
        <button
          @click="fetchProjects"
          class="mt-2 text-sm font-medium underline"
        >
          Tentar novamente
        </button>
      </div>

      <!-- Empty state -->
      <div
        v-else-if="filteredProjects.length === 0"
        class="flex flex-col items-center justify-center rounded-lg border border-dashed border-gray-300 bg-gray-50 p-12 text-center"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="h-12 w-12 text-gray-400"
        >
          <path d="M3 3v18h18"></path>
          <path d="M7 12v5"></path>
          <path d="m14 7 3-3 3 3"></path>
          <path d="M7 19h5"></path>
          <path d="M19 15v4"></path>
          <path d="M11 12v5"></path>
          <path d="M14 12v5"></path>
        </svg>
        <h3 class="mt-4 text-lg font-medium text-gray-900">
          Nenhum projeto encontrado
        </h3>
        <p class="mt-1 text-sm text-gray-500">
          {{
            projects.length === 0
              ? 'Comece criando seu primeiro projeto.'
              : 'Nenhum projeto corresponde aos filtros aplicados.'
          }}
        </p>
        <button
          v-if="projects.length === 0"
          @click="openNewProjectModal"
          class="mt-4 inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-4 w-4 mr-2"
          >
            <path d="M5 12h14"></path>
            <path d="M12 5v14"></path>
          </svg>
          Criar Projeto
        </button>
      </div>

      <!-- Project list -->
      <div v-else class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="project in filteredProjects"
          :key="project.id"
          class="flex flex-col rounded-lg border bg-white shadow-sm transition-all hover:shadow-md"
        >
          <div class="p-4">
            <div class="flex items-center justify-between">
              <span
                :class="{
                  'bg-yellow-100 text-yellow-800':
                    project.status === 'PLANEJADO',
                  'bg-blue-100 text-blue-800':
                    project.status === 'EM_ANDAMENTO',
                  'bg-orange-100 text-orange-800': project.status === 'PAUSADO',
                  'bg-green-100 text-green-800': project.status === 'CONCLUIDO',
                  'bg-red-100 text-red-800': project.status === 'CANCELADO',
                }"
                class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
              >
                {{ getStatusLabel(project.status) }}
              </span>
              <span
                :class="{
                  'bg-green-100 text-green-800': project.prioridade === 'BAIXA',
                  'bg-yellow-100 text-yellow-800':
                    project.prioridade === 'MEDIA',
                  'bg-red-100 text-red-800': project.prioridade === 'ALTA',
                }"
                class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
              >
                {{ getPriorityLabel(project.prioridade) }}
              </span>
            </div>
            <h3 class="mt-2 text-lg font-semibold text-gray-900">
              {{ project.titulo }}
            </h3>
            <p class="mt-1 line-clamp-2 text-sm text-gray-500">
              {{ project.descricao }}
            </p>
            <div class="mt-4 flex items-center justify-between">
              <div class="flex items-center gap-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  class="h-4 w-4 text-gray-400"
                >
                  <rect width="18" height="18" x="3" y="4" rx="2" ry="2"></rect>
                  <line x1="16" x2="16" y1="2" y2="6"></line>
                  <line x1="8" x2="8" y1="2" y2="6"></line>
                  <line x1="3" x2="21" y1="10" y2="10"></line>
                </svg>
                <span class="text-xs text-gray-500">
                  {{ formatDate(project.data_inicio) }} -
                  {{ formatDate(project.data_fim) }}
                </span>
              </div>
              <div class="flex items-center gap-2">
                <button
                  @click="openEditProjectModal(project)"
                  class="inline-flex items-center justify-center rounded-md p-1 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                  title="Editar projeto"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="h-4 w-4"
                  >
                    <path
                      d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"
                    ></path>
                    <path d="m15 5 4 4"></path>
                  </svg>
                </button>
                <button
                  @click="deleteProject(project.id)"
                  class="inline-flex items-center justify-center rounded-md p-1 text-sm font-medium text-red-600 hover:bg-red-50 hover:text-red-700"
                  title="Excluir projeto"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="h-4 w-4"
                  >
                    <path d="M3 6h18"></path>
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                  </svg>
                </button>
                <button
                  @click="viewProject(project.id)"
                  class="inline-flex items-center justify-center rounded-md text-sm font-medium text-blue-600 hover:text-blue-700"
                >
                  Ver detalhes
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="ml-1 h-4 w-4"
                  >
                    <path d="M5 12h14"></path>
                    <path d="m12 5 7 7-7 7"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div
        v-if="totalPages > 1"
        class="flex items-center justify-center space-x-2 pt-4"
      >
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-gray-300 text-sm font-medium text-gray-700 disabled:opacity-50"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-4 w-4"
          >
            <path d="M15 18-6-6 6-6"></path>
          </svg>
        </button>
        <div
          v-for="page in paginationRange"
          :key="page"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md text-sm font-medium"
          :class="
            page === currentPage
              ? 'bg-blue-600 text-white'
              : 'border border-gray-300 text-gray-700 hover:bg-gray-50'
          "
          @click="changePage(page)"
        >
          {{ page }}
        </div>
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-gray-300 text-sm font-medium text-gray-700 disabled:opacity-50"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-4 w-4"
          >
            <path d="M9 18 15 12 9 6"></path>
          </svg>
        </button>
      </div>

      <!-- Modal para novo projeto -->
      <div
        v-if="showNewProjectModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4"
      >
        <div class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium">Novo Projeto</h3>
            <button
              @click="showNewProjectModal = false"
              class="rounded-md p-1 text-gray-500 hover:bg-gray-100 hover:text-gray-700"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="h-5 w-5"
              >
                <path d="M18 6 6 18"></path>
                <path d="m6 6 12 12"></path>
              </svg>
            </button>
          </div>
          <div class="mt-4 space-y-4">
            <div>
              <label
                for="titulo"
                class="block text-sm font-medium text-gray-700"
                >Título</label
              >
              <input
                id="titulo"
                v-model="newProject.titulo"
                type="text"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                :class="{
                  'border-red-500 focus:border-red-500 focus:ring-red-500':
                    formErrors.titulo,
                }"
              />
              <p v-if="formErrors.titulo" class="mt-1 text-xs text-red-500">
                {{ formErrors.titulo }}
              </p>
            </div>
            <div>
              <label
                for="descricao"
                class="block text-sm font-medium text-gray-700"
                >Descrição</label
              >
              <textarea
                id="descricao"
                v-model="newProject.descricao"
                rows="3"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                :class="{
                  'border-red-500 focus:border-red-500 focus:ring-red-500':
                    formErrors.descricao,
                }"
              ></textarea>
              <p v-if="formErrors.descricao" class="mt-1 text-xs text-red-500">
                {{ formErrors.descricao }}
              </p>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label
                  for="data_inicio"
                  class="block text-sm font-medium text-gray-700"
                  >Data de Início</label
                >
                <input
                  id="data_inicio"
                  v-model="newProject.data_inicio"
                  type="date"
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  :class="{
                    'border-red-500 focus:border-red-500 focus:ring-red-500':
                      formErrors.data_inicio,
                  }"
                />
                <p
                  v-if="formErrors.data_inicio"
                  class="mt-1 text-xs text-red-500"
                >
                  {{ formErrors.data_inicio }}
                </p>
              </div>
              <div>
                <label
                  for="data_fim"
                  class="block text-sm font-medium text-gray-700"
                  >Data de Término</label
                >
                <input
                  id="data_fim"
                  v-model="newProject.data_fim"
                  type="date"
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  :class="{
                    'border-red-500 focus:border-red-500 focus:ring-red-500':
                      formErrors.data_fim,
                  }"
                />
                <p v-if="formErrors.data_fim" class="mt-1 text-xs text-red-500">
                  {{ formErrors.data_fim }}
                </p>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label
                  for="status"
                  class="block text-sm font-medium text-gray-700"
                  >Status</label
                >
                <select
                  id="status"
                  v-model="newProject.status"
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="PLANEJADO">Planejado</option>
                  <option value="EM_ANDAMENTO">Em Andamento</option>
                  <option value="PAUSADO">Pausado</option>
                  <option value="CONCLUIDO">Concluído</option>
                  <option value="CANCELADO">Cancelado</option>
                </select>
              </div>
              <div>
                <label
                  for="prioridade"
                  class="block text-sm font-medium text-gray-700"
                  >Prioridade</label
                >
                <select
                  id="prioridade"
                  v-model="newProject.prioridade"
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="BAIXA">Baixa</option>
                  <option value="MEDIA">Média</option>
                  <option value="ALTA">Alta</option>
                </select>
              </div>
            </div>
            <div>
              <label
                for="orcamento"
                class="block text-sm font-medium text-gray-700"
                >Orçamento (R$)</label
              >
              <input
                id="orcamento"
                v-model="newProject.orcamento"
                type="number"
                min="0"
                step="0.01"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <div>
              <label
                for="gerente"
                class="block text-sm font-medium text-gray-700"
                >Gerente do Projeto</label
              >
              <select
                id="gerente"
                v-model="newProject.gerente"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option :value="null">Selecione um gerente</option>
                <option v-for="user in users" :key="user.id" :value="user.id">
                  {{ user.full_name || user.username }}
                </option>
              </select>
            </div>
          </div>
          <div class="mt-6 flex justify-end gap-3">
            <button
              @click="showNewProjectModal = false"
              class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
            >
              Cancelar
            </button>
            <button
              @click="createProject"
              :disabled="isSubmitting"
              class="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 disabled:opacity-50"
            >
              <span v-if="isSubmitting" class="flex items-center">
                <svg
                  class="mr-2 h-4 w-4 animate-spin"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Criando...
              </span>
              <span v-else>Criar Projeto</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Modal para editar projeto -->
      <div
        v-if="showEditProjectModal && editingProject"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4"
      >
        <div class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium">Editar Projeto</h3>
            <button
              @click="showEditProjectModal = false"
              class="rounded-md p-1 text-gray-500 hover:bg-gray-100 hover:text-gray-700"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="h-5 w-5"
              >
                <path d="M18 6 6 18"></path>
                <path d="m6 6 12 12"></path>
              </svg>
            </button>
          </div>
          <div class="mt-4 space-y-4">
            <div>
              <label
                for="edit_titulo"
                class="block text-sm font-medium text-gray-700"
                >Título</label
              >
              <input
                id="edit_titulo"
                v-model="editingProject.titulo"
                type="text"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                :class="{
                  'border-red-500 focus:border-red-500 focus:ring-red-500':
                    formErrors.titulo,
                }"
              />
              <p v-if="formErrors.titulo" class="mt-1 text-xs text-red-500">
                {{ formErrors.titulo }}
              </p>
            </div>
            <div>
              <label
                for="edit_descricao"
                class="block text-sm font-medium text-gray-700"
                >Descrição</label
              >
              <textarea
                id="edit_descricao"
                v-model="editingProject.descricao"
                rows="3"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                :class="{
                  'border-red-500 focus:border-red-500 focus:ring-red-500':
                    formErrors.descricao,
                }"
              ></textarea>
              <p v-if="formErrors.descricao" class="mt-1 text-xs text-red-500">
                {{ formErrors.descricao }}
              </p>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label
                  for="edit_data_inicio"
                  class="block text-sm font-medium text-gray-700"
                  >Data de Início</label
                >
                <input
                  id="edit_data_inicio"
                  v-model="editingProject.data_inicio"
                  type="date"
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  :class="{
                    'border-red-500 focus:border-red-500 focus:ring-red-500':
                      formErrors.data_inicio,
                  }"
                />
                <p
                  v-if="formErrors.data_inicio"
                  class="mt-1 text-xs text-red-500"
                >
                  {{ formErrors.data_inicio }}
                </p>
              </div>
              <div>
                <label
                  for="edit_data_fim"
                  class="block text-sm font-medium text-gray-700"
                  >Data de Término</label
                >
                <input
                  id="edit_data_fim"
                  v-model="editingProject.data_fim"
                  type="date"
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  :class="{
                    'border-red-500 focus:border-red-500 focus:ring-red-500':
                      formErrors.data_fim,
                  }"
                />
                <p v-if="formErrors.data_fim" class="mt-1 text-xs text-red-500">
                  {{ formErrors.data_fim }}
                </p>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label
                  for="edit_status"
                  class="block text-sm font-medium text-gray-700"
                  >Status</label
                >
                <select
                  id="edit_status"
                  v-model="editingProject.status"
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="PLANEJADO">Planejado</option>
                  <option value="EM_ANDAMENTO">Em Andamento</option>
                  <option value="PAUSADO">Pausado</option>
                  <option value="CONCLUIDO">Concluído</option>
                  <option value="CANCELADO">Cancelado</option>
                </select>
              </div>
              <div>
                <label
                  for="edit_prioridade"
                  class="block text-sm font-medium text-gray-700"
                  >Prioridade</label
                >
                <select
                  id="edit_prioridade"
                  v-model="editingProject.prioridade"
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="BAIXA">Baixa</option>
                  <option value="MEDIA">Média</option>
                  <option value="ALTA">Alta</option>
                </select>
              </div>
            </div>
            <div>
              <label
                for="edit_orcamento"
                class="block text-sm font-medium text-gray-700"
                >Orçamento (R$)</label
              >
              <input
                id="edit_orcamento"
                v-model="editingProject.orcamento"
                type="number"
                min="0"
                step="0.01"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <div>
              <label
                for="edit_gerente"
                class="block text-sm font-medium text-gray-700"
                >Gerente do Projeto</label
              >
              <select
                id="edit_gerente"
                v-model="editingProject.gerente"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option :value="null">Selecione um gerente</option>
                <option v-for="user in users" :key="user.id" :value="user.id">
                  {{ user.full_name || user.username }}
                </option>
              </select>
            </div>
          </div>
          <div class="mt-6 flex justify-end gap-3">
            <button
              @click="showEditProjectModal = false"
              class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
            >
              Cancelar
            </button>
            <button
              @click="updateProject"
              :disabled="isSubmitting"
              class="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 disabled:opacity-50"
            >
              <span v-if="isSubmitting" class="flex items-center">
                <svg
                  class="mr-2 h-4 w-4 animate-spin"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Salvando...
              </span>
              <span v-else>Salvar Alterações</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, onBeforeMount } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useProjectService } from '~/services/api/services/projectService';
import { useUserService } from '~/services/api/services/userService';
import { useAuth } from '~/stores/composables/useAuth';
import { useNotification } from '~/stores/composables/useNotification';

const router = useRouter();
const route = useRoute();
const projectService = useProjectService();
const { user } = useAuth();
const notification = useNotification();

// Estado
const projects = ref([]);
const loading = ref(false);
const error = ref(null);
const searchQuery = ref('');
const statusFilter = ref('');
const priorityFilter = ref('');
const currentPage = ref(1);
const totalPages = ref(1);
const itemsPerPage = ref(9);
const totalItems = ref(0);

// Estado do formulário de novo projeto
const showNewProjectModal = ref(false);
const newProject = ref({
  titulo: '',
  descricao: '',
  data_inicio: '',
  data_fim: '',
  status: 'PLANEJADO',
  prioridade: 'MEDIA',
});
const formErrors = ref({});
const isSubmitting = ref(false);

// Estado para edição de projeto
const showEditProjectModal = ref(false);
const editingProject = ref(null);

// Lista de usuários para seleção de gerente
const users = ref([]);
const loadingUsers = ref(false);

// Permissões baseadas em papel
const userRole = computed(() => user?.role || 'viewer');
const userCanCreate = computed(() => ['admin', 'manager'].includes(userRole.value));
const userCanEdit = computed(() => ['admin', 'manager', 'editor'].includes(userRole.value));
const userCanDelete = computed(() => ['admin', 'manager'].includes(userRole.value));

// Projetos filtrados
const filteredProjects = computed(() => {
  if (!searchQuery.value && !statusFilter.value && !priorityFilter.value) {
    return projects.value;
  }

  return projects.value.filter((project) => {
    const matchesSearch = searchQuery.value
      ? project.titulo
          .toLowerCase()
          .includes(searchQuery.value.toLowerCase()) ||
        project.descricao
          .toLowerCase()
          .includes(searchQuery.value.toLowerCase())
      : true;

    const matchesStatus = statusFilter.value
      ? project.status === statusFilter.value
      : true;

    const matchesPriority = priorityFilter.value
      ? project.prioridade === priorityFilter.value
      : true;

    return matchesSearch && matchesStatus && matchesPriority;
  });
});

// Range de páginas para paginação
const paginationRange = computed(() => {
  const range = [];
  const maxVisiblePages = 5;

  if (totalPages.value <= maxVisiblePages) {
    for (let i = 1; i <= totalPages.value; i++) {
      range.push(i);
    }
  } else {
    let start = Math.max(
      1,
      currentPage.value - Math.floor(maxVisiblePages / 2)
    );
    let end = Math.min(totalPages.value, start + maxVisiblePages - 1);

    if (end - start + 1 < maxVisiblePages) {
      start = Math.max(1, end - maxVisiblePages + 1);
    }

    for (let i = start; i <= end; i++) {
      range.push(i);
    }
  }

  return range;
});

// Buscar projetos do servidor
const fetchProjects = async () => {
  loading.value = true;
  error.value = null;

  try {
    const params = {
      page: currentPage.value,
      ordering: '-data_criacao',
    };

    if (statusFilter.value) {
      params.status = statusFilter.value;
    }

    if (searchQuery.value) {
      params.search = searchQuery.value;
    }

    // Usar o novo serviço de projetos
    const response = await projectService.fetchProjects(params);

    // Processar dados da resposta paginada
    projects.value = response.results.map((project) => ({
      id: project.id,
      titulo: project.nome,
      descricao: project.descricao,
      data_inicio: project.data_inicio,
      data_fim: project.data_fim,
      status: project.status,
      prioridade: project.prioridade,
      status_display: project.status_display,
      progresso: project.progresso,
      gerente: project.gerente,
      gerente_nome: project.gerente_nome,
    }));

    totalItems.value = response.count;
    totalPages.value = Math.ceil(response.count / itemsPerPage.value);
  } catch (err) {
    console.error('Erro ao buscar projetos:', err);
    error.value =
      'Não foi possível carregar os projetos. Por favor, tente novamente.';
    notification.error('Erro ao carregar projetos', {
      title: 'Erro',
      duration: 5000,
    });
  } finally {
    loading.value = false;
  }
};

// Buscar usuários para seleção de gerente
const fetchUsers = async () => {
  try {
    const userService = useUserService();
    const response = await userService.fetchUsers();
    users.value = response.map((user) => ({
      id: user.id,
      nome: user.full_name || `${user.first_name} ${user.last_name}`,
      email: user.email,
      username: user.username
    }));
  } catch (err) {
    console.error('Erro ao buscar usuários:', err);
    notification.error('Erro ao carregar usuários', {
      title: 'Erro',
      duration: 5000,
    });
  }
};

// Mudar página
const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
  fetchProjects();
};

// Formatar data
const formatDate = (dateString) => {
  if (!dateString) return '';

  const date = new Date(dateString);
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(date);
};

// Obter label do status
const getStatusLabel = (status) => {
  const statusMap = {
    PLANEJADO: 'Planejado',
    EM_ANDAMENTO: 'Em Andamento',
    PAUSADO: 'Pausado',
    CONCLUIDO: 'Concluído',
    CANCELADO: 'Cancelado',
  };

  return statusMap[status] || status;
};

// Obter label da prioridade
const getPriorityLabel = (priority) => {
  const priorityMap = {
    BAIXA: 'Baixa',
    MEDIA: 'Média',
    ALTA: 'Alta',
  };

  return priorityMap[priority] || priority;
};

// Abrir modal de novo projeto
const openNewProjectModal = () => {
  showNewProjectModal.value = true;
  fetchUsers();
};

// Abrir modal de edição de projeto
const openEditProjectModal = async (project) => {
  try {
    loading.value = true;
    const projectDetails = await projectService.fetchProject(project.id);
    editingProject.value = { ...projectDetails };
    showEditProjectModal.value = true;
    fetchUsers();
  } catch (err) {
    console.error('Erro ao buscar detalhes do projeto:', err);
    notification.error('Erro ao carregar detalhes do projeto', {
      title: 'Erro',
      duration: 5000,
    });
  } finally {
    loading.value = false;
  }
};

// Criar novo projeto
const createProject = async () => {
  if (!newProject.titulo || !newProject.data_inicio || !newProject.status) {
    notification.error('Preencha todos os campos obrigatórios', {
      title: 'Erro',
      duration: 5000,
    });
    return;
  }

  isSubmitting.value = true;

  try {
    // Preparar dados para o novo formato da API
    const projectData = {
      nome: newProject.titulo,
      descricao: newProject.descricao,
      data_inicio: newProject.data_inicio,
      data_fim: newProject.data_fim || null,
      status: newProject.status,
      gerente: newProject.gerente,
    };

    // Usar o serviço de projetos para criar projeto
    const response = await projectService.createProject(projectData);

    // Adicionar o novo projeto à lista
    projects.value.unshift({
      id: response.id,
      titulo: response.nome,
      descricao: response.descricao,
      data_inicio: response.data_inicio,
      data_fim: response.data_fim,
      status: response.status,
      status_display: response.status_display,
      progresso: response.progresso,
      gerente: response.gerente,
      gerente_nome: response.gerente_nome,
    });

    // Atualizar contagem total
    totalItems.value += 1;
    totalPages.value = Math.ceil(totalItems.value / itemsPerPage.value);

    // Fechar o modal e limpar o formulário
    showNewProjectModal.value = false;
    newProject.titulo = '';
    newProject.descricao = '';
    newProject.data_inicio = new Date().toISOString().split('T')[0];
    newProject.data_fim = '';
    newProject.status = 'PLANEJADO';
    newProject.prioridade = 'MEDIA';
    newProject.gerente = null;

    // Mostrar notificação de sucesso
    notification.success('Projeto criado com sucesso', {
      title: 'Sucesso',
      duration: 5000,
    });

    // Redirecionar para a página do novo projeto
    router.push(`/projetos/${response.id}`);
  } catch (err) {
    console.error('Erro ao criar projeto:', err);
    notification.error(
      'Não foi possível criar o projeto. Por favor, tente novamente.',
      {
        title: 'Erro',
        duration: 5000,
      }
    );
  } finally {
    isSubmitting.value = false;
  }
};

// Atualizar projeto
const updateProject = async () => {
  formErrors.value = {};
  isSubmitting.value = true;

  try {
    // Validar campos obrigatórios
    if (!editingProject.value.titulo) {
      formErrors.value.titulo = 'Título é obrigatório';
    }

    if (!editingProject.value.data_inicio) {
      formErrors.value.data_inicio = 'Data de início é obrigatória';
    }

    if (!editingProject.value.data_fim) {
      formErrors.value.data_fim = 'Data de término é obrigatória';
    }

    if (Object.keys(formErrors.value).length > 0) {
      return;
    }

    // Preparar dados para envio
    const projectData = {
      nome: editingProject.value.titulo,
      descricao: editingProject.value.descricao,
      data_inicio: editingProject.value.data_inicio,
      data_fim: editingProject.value.data_fim,
      status: editingProject.value.status,
      prioridade: editingProject.value.prioridade,
      gerente: editingProject.value.gerente,
    };

    // Enviar para a API usando o serviço de projetos
    await projectService.updateProject(editingProject.value.id, projectData);

    notification.success('Projeto atualizado com sucesso!', {
      title: 'Sucesso',
      duration: 5000,
    });

    showEditProjectModal.value = false;
    editingProject.value = null;

    fetchProjects();
  } catch (err) {
    console.error('Erro ao atualizar projeto:', err);

    if (err.response && err.response.data) {
      // Mapear erros da API para o formulário
      const apiErrors = err.response.data;
      Object.keys(apiErrors).forEach((key) => {
        formErrors.value[key] = Array.isArray(apiErrors[key])
          ? apiErrors[key][0]
          : apiErrors[key];
      });
    } else {
      notification.error(
        'Erro ao atualizar projeto. Por favor, tente novamente.',
        {
          title: 'Erro',
          duration: 5000,
        }
      );
    }
  } finally {
    isSubmitting.value = false;
  }
};

// Excluir projeto
const deleteProject = async (id) => {
  if (
    !confirm(
      'Tem certeza que deseja excluir este projeto? Esta ação não pode ser desfeita.'
    )
  ) {
    return;
  }

  try {
    loading.value = true;
    await projectService.deleteProject(id);

    notification.success('Projeto excluído com sucesso!', {
      title: 'Sucesso',
      duration: 5000,
    });

    fetchProjects();
  } catch (err) {
    console.error('Erro ao excluir projeto:', err);
    notification.error('Erro ao excluir projeto. Por favor, tente novamente.', {
      title: 'Erro',
      duration: 5000,
    });
  } finally {
    loading.value = false;
  }
};

// Ver detalhes do projeto
const viewProject = (id) => {
  router.push(`/projetos/${id}`);
};

// Observar mudanças nos filtros
watch([searchQuery, statusFilter, priorityFilter], () => {
  if (
    searchQuery.value === '' &&
    statusFilter.value === '' &&
    priorityFilter.value === ''
  ) {
    fetchProjects();
  } else {
    currentPage.value = 1;
    fetchProjects();
  }
});

// Verificar se deve abrir modal de novo projeto
onMounted(() => {
  if (route.query.new === 'true') {
    openNewProjectModal();
  }

  fetchProjects();
});
</script>
