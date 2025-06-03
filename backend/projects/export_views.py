from rest_framework import status, permissions  # Ensure 'djangorestframework' is installed
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse  # Removed unused HttpRequest
import csv
import json
from datetime import datetime
from typing import List, Dict, Any, Union, Optional # For type hinting

from drf_spectacular.utils import extend_schema, OpenApiParameter  # Removed unused OpenApiResponse
from drf_spectacular.types import OpenApiTypes

# Assuming models are correctly imported from the current app (.) and tasks app
from .models import Projeto, MembroProjeto, Sprint
from tasks.models import Tarefa  # Removed unused AtribuicaoTarefa
from costs.models import Custo  # Ensure Custo is used in the code
from .api_schemas import ErrorResponseSerializer  # Removed unused ExportResponseSerializer

# For type hinting specific model instances
from risks.models import Risco  # Ensure Risco is used in the code
# from costs.models import Custo # Only if needed for type hints outside methods


@extend_schema(
    summary="Exportar dados do projeto",
    description="Exporta dados detalhados de um projeto específico em formatos CSV ou JSON. "
                "O usuário deve ser membro do projeto ou um administrador para acessá-lo. "
                "É possível selecionar diferentes seções de dados para incluir na exportação, "
                "como informações básicas do projeto, lista de tarefas, equipe, riscos e custos.",
    parameters=[
        OpenApiParameter(name='projeto_id', description='ID do projeto a ser exportado.', required=True, type=int, location=OpenApiParameter.PATH),
        OpenApiParameter(name='format', description='Formato de exportação desejado. Opções: "csv" ou "json".', required=False, type=str, default='csv', location=OpenApiParameter.QUERY),
        OpenApiParameter(name='include_project', description='Define se os dados básicos do projeto devem ser incluídos.', required=False, type=bool, default=True, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='include_tasks', description='Define se as tarefas (incluindo dados para Kanban e Gantt) do projeto devem ser incluídas.', required=False, type=bool, default=True, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='include_team', description='Define se os dados da equipe do projeto devem ser incluídos.', required=False, type=bool, default=False, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='include_risks', description='Define se os riscos associados ao projeto devem ser incluídos.', required=False, type=bool, default=False, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='include_costs', description='Define se os custos associados ao projeto devem ser incluídos.', required=False, type=bool, default=False, location=OpenApiParameter.QUERY)
    ],
    responses={
        200: OpenApiTypes.BINARY, # Indicates a file download
        400: ErrorResponseSerializer, # For bad requests (e.g., invalid format, no data selected)
        403: ErrorResponseSerializer, # For permission denied
        404: ErrorResponseSerializer  # For project not found
    },
    tags=["Projetos", "Exportação"]
)
class ProjetoExportView(APIView):
    """
    Permite a exportação de dados de um projeto específico.

    Esta view habilita usuários autenticados a exportar informações detalhadas
    de um projeto do qual são membros ou administradores. Os dados podem ser
    exportados nos formatos CSV ou JSON. Diversas seções de dados podem ser
    selecionadas para inclusão, como detalhes do projeto, tarefas, equipe,
    riscos e custos.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: 'rest_framework.request.Request', projeto_id: int, format: Optional[str] = None) -> Union[HttpResponse, Response]:
        """
        Manipula requisições GET para exportar dados do projeto.

        Valida o acesso do usuário ao projeto, processa os parâmetros da query
        para determinar quais dados incluir e em qual formato, coleta os dados
        e os retorna como um arquivo CSV ou JSON.

        Args:
            request: O objeto HttpRequest.
            projeto_id: O ID do projeto a ser exportado.
            format: O formato de exportação (passado como parte do path, mas
                    aqui para compatibilidade, embora seja pego dos query_params).

        Returns:
            HttpResponse com o arquivo de dados (CSV/JSON) ou
            Response com uma mensagem de erro.
        """
        projeto = get_object_or_404(Projeto, id=projeto_id)

        # Verificar se o usuário tem acesso ao projeto
        # Staff users have access to all projects for export, or user must be a member.
        is_member = MembroProjeto.objects.filter(projeto=projeto, usuario=request.user).exists()
        if not is_member and not request.user.is_staff:
            return Response(
                {"detail": "Você não tem permissão para acessar este projeto."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Determinar o formato de exportação a partir dos query params
        export_format = request.query_params.get('format', 'csv').lower()
        if export_format not in ['csv', 'json']:
            return Response(
                {"detail": "Formato de exportação inválido. Opções: csv, json"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Query params arrive as strings 'true'/'false'
        include_project = request.query_params.get('include_project', 'true').strip().lower() in ['true', '1']
        include_tasks = request.query_params.get('include_tasks', 'true').strip().lower() in ['true', '1']
        include_team = request.query_params.get('include_team', 'false').strip().lower() in ['true', '1']
        include_risks = request.query_params.get('include_risks', 'false').strip().lower() in ['true', '1']
        include_costs = request.query_params.get('include_costs', 'false').strip().lower() in ['true', '1']

        if not any([include_project, include_tasks, include_team, include_risks, include_costs]):
            return Response(
                {"detail": "Selecione pelo menos um tipo de dado para exportar."},
                status=status.HTTP_400_BAD_REQUEST
            )

        export_data: Dict[str, Any] = {}

        if include_project:
            export_data['projeto'] = self._get_projeto_data(projeto)

        if include_tasks:
            export_data['tarefas'] = self._get_tarefas_data(projeto)
            export_data['kanban'] = self._get_kanban_data(projeto) # Kanban data is derived from tasks
            export_data['gantt'] = self._get_gantt_data(projeto)   # Gantt data includes project, sprints, tasks

        if include_team:
            export_data['equipe'] = self._get_equipe_data(projeto)

        if include_risks:
            # Risco model is already imported at the top
            export_data['riscos'] = self._get_riscos_data(projeto)

        if include_costs:
            # Local import
            from costs.models import Custo # noqa
            export_data['custos'] = self._get_custos_data(projeto)

        # Nome do arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        from slugify import slugify  # Ensure 'python-slugify' is installed
        safe_titulo = slugify(projeto.titulo)
        filename = f"projeto_{projeto.id}_{safe_titulo}_{timestamp}"

        if export_format == 'csv':
            return self._export_csv(export_data, filename)
        # No need for elif export_format == 'json', as it's the only other valid option
        return self._export_json(export_data, filename)

    def _get_projeto_data(self, projeto: Projeto) -> Dict[str, Any]:
        """
        Coleta e formata os dados básicos de um projeto.

        Args:
            projeto: A instância do modelo Projeto.

        Returns:
            Um dicionário contendo os dados formatados do projeto.
        """
        return {
            'id': projeto.id,
            'titulo': projeto.titulo,
            'descricao': projeto.descricao,
            'data_inicio': projeto.data_inicio.strftime('%Y-%m-%d') if projeto.data_inicio else None,
            'data_fim': projeto.data_fim.strftime('%Y-%m-%d') if projeto.data_fim else None,
            'status': dict(Projeto.STATUS_CHOICES).get(projeto.status, projeto.status),
            'prioridade': dict(Projeto.PRIORIDADE_CHOICES).get(projeto.prioridade, projeto.prioridade),
            'gerente_username': projeto.gerente.username if projeto.gerente else None,
            'gerente_nome_completo': f"{projeto.gerente.first_name} {projeto.gerente.last_name}".strip() if projeto.gerente else None,
            'criado_por_username': projeto.criado_por.username if projeto.criado_por else None,
            'criado_em': projeto.criado_em.strftime('%Y-%m-%d %H:%M') if projeto.criado_em else None,
            'atualizado_em': projeto.atualizado_em.strftime('%Y-%m-%d %H:%M') if projeto.atualizado_em else None,
            'arquivado': projeto.arquivado
        }

    def _get_tarefas_data(self, projeto: Projeto) -> List[Dict[str, Any]]:
        """
        Coleta e formata os dados das tarefas associadas a um projeto.

        Args:
            projeto: A instância do modelo Projeto.

        Returns:
            Uma lista de dicionários, cada um representando uma tarefa.
        """
        tarefas = Tarefa.objects.filter(projeto=projeto).select_related('sprint', 'criado_por')
        data: List[Dict[str, Any]] = []

        # Prefetch atribuicoes for all tarefas at once to avoid N+1 queries
        tarefas = tarefas.prefetch_related('atribuicoes__usuario')

        for tarefa in tarefas:
            # Using prefetch_related for atribuicoes should make this efficient
            responsaveis = [atr.usuario.username for atr in tarefa.atribuicoes.all() if atr.usuario]
            responsaveis_str = ", ".join(responsaveis)

            data.append({
                'id_tarefa': tarefa.id,
                'titulo_tarefa': tarefa.titulo,
                'descricao_tarefa': tarefa.descricao,
                'data_inicio_tarefa': tarefa.data_inicio.strftime('%Y-%m-%d') if tarefa.data_inicio else None,
                'data_termino_tarefa': tarefa.data_termino.strftime('%Y-%m-%d') if tarefa.data_termino else None,
                'status_tarefa': dict(Tarefa.STATUS_CHOICES).get(tarefa.status, tarefa.status),
                'prioridade_tarefa': dict(Tarefa.PRIORITY_CHOICES).get(tarefa.prioridade, tarefa.prioridade),
                'responsaveis_tarefa': responsaveis_str,
                'sprint_tarefa': tarefa.sprint.nome if tarefa.sprint else 'Sem Sprint',
                'criado_por_tarefa': tarefa.criado_por.username if tarefa.criado_por else 'Desconhecido',
                'criado_em_tarefa': tarefa.criado_em.strftime('%Y-%m-%d %H:%M') if tarefa.criado_em else None,
            })
        return data

    def _get_kanban_data(self, projeto: Projeto) -> List[Dict[str, Any]]:
        """
        Coleta e formata os dados das tarefas para uma visualização Kanban.
        As tarefas são agrupadas por status.

        Args:
            projeto: A instância do modelo Projeto.

        Returns:
            Uma lista de dicionários, cada um representando uma tarefa com seu status Kanban.
        """
        # These statuses should ideally align with Tarefa.STATUS_CHOICES keys
        # For simplicity, we keep them hardcoded as in the original code.
        # If Tarefa.STATUS_CHOICES were ('A_FAZER', 'A Fazer'), ('EM_ANDAMENTO', 'Em Andamento'), etc.
        
        # Removed duplicate tarefas fetching and use direct DB query instead of _get_tarefas_data
        tarefas = Tarefa.objects.filter(projeto=projeto).select_related('sprint').prefetch_related('atribuicoes__usuario')
        
        result_list: List[Dict[str, Any]] = []

        for tarefa in tarefas:
            responsaveis = [atr.usuario.username for atr in tarefa.atribuicoes.all() if atr.usuario]
            responsaveis_str = ", ".join(responsaveis)

            result_list.append({
                'id_kanban_tarefa': tarefa.id,
                'titulo_kanban_tarefa': tarefa.titulo,
                'descricao_kanban_tarefa': tarefa.descricao, # Potentially long for Kanban, but included
                'data_inicio_kanban_tarefa': tarefa.data_inicio.strftime('%Y-%m-%d') if tarefa.data_inicio else None,
                'data_termino_kanban_tarefa': tarefa.data_termino.strftime('%Y-%m-%d') if tarefa.data_termino else None,
                'prioridade_kanban_tarefa': dict(Tarefa.PRIORITY_CHOICES).get(tarefa.prioridade, tarefa.prioridade),
                'responsaveis_kanban_tarefa': responsaveis_str,
                'sprint_kanban_tarefa': tarefa.sprint.nome if tarefa.sprint else 'Sem Sprint',
                'status_kanban_coluna': dict(Tarefa.STATUS_CHOICES).get(tarefa.status, tarefa.status), # The column it belongs to
            })
        return result_list


    def _get_gantt_data(self, projeto: Projeto) -> List[Dict[str, Any]]:
        """
        Coleta e formata os dados do projeto, sprints e tarefas para um diagrama de Gantt.

        Args:
            projeto: A instância do modelo Projeto.

        Returns:
            Uma lista de dicionários, cada um representando um item no Gantt (projeto, sprint ou tarefa).
        """
        gantt_data: List[Dict[str, Any]] = []

        # Adicionar o projeto
        gantt_data.append({
            'id_gantt': f"projeto_{projeto.id}",
            'titulo_gantt': f"Projeto: {projeto.titulo}",
            'tipo_gantt': 'projeto',
            'data_inicio_gantt': projeto.data_inicio.strftime('%Y-%m-%d') if projeto.data_inicio else None,
            'data_fim_gantt': projeto.data_fim.strftime('%Y-%m-%d') if projeto.data_fim else None,
            'status_gantt': dict(Projeto.STATUS_CHOICES).get(projeto.status, projeto.status),
            'progresso_gantt_percentual': 100 if projeto.status == 'CONCLUIDO' else (50 if projeto.status == 'EM_ANDAMENTO' else 0)
        })

        # Adicionar sprints
        sprints = Sprint.objects.filter(projeto=projeto).select_related('projeto')
        for sprint in sprints:
            gantt_data.append({
                'id_gantt': f"sprint_{sprint.id}",
                'titulo_gantt': f"Sprint: {sprint.nome}",
                'tipo_gantt': 'sprint',
                'data_inicio_gantt': sprint.data_inicio.strftime('%Y-%m-%d') if sprint.data_inicio else None,
                'data_fim_gantt': sprint.data_fim.strftime('%Y-%m-%d') if sprint.data_fim else None,
                'status_gantt': dict(Sprint.STATUS_CHOICES).get(sprint.status, sprint.status),
                'progresso_gantt_percentual': 100 if sprint.status == 'CONCLUIDO' else (50 if sprint.status == 'EM_ANDAMENTO' else 0)
            })

        # Adicionar tarefas
        tarefas_gantt = Tarefa.objects.filter(projeto=projeto).select_related('sprint').prefetch_related('atribuicoes__usuario')
        for tarefa in tarefas_gantt:
            responsaveis = [atr.usuario.username for atr in tarefa.atribuicoes.all() if atr.usuario]
            responsaveis_str = ", ".join(responsaveis)

            gantt_data.append({
                'id_gantt': f"tarefa_{tarefa.id}",
                'titulo_gantt': tarefa.titulo,
                'tipo_gantt': 'tarefa',
                'data_inicio_gantt': tarefa.data_inicio.strftime('%Y-%m-%d') if tarefa.data_inicio else None,
                'data_fim_gantt': tarefa.data_termino.strftime('%Y-%m-%d') if tarefa.data_termino else None,
                'status_gantt': dict(Tarefa.STATUS_CHOICES).get(tarefa.status, tarefa.status),
                'prioridade_gantt': dict(Tarefa.PRIORITY_CHOICES).get(tarefa.prioridade, tarefa.prioridade),
                'responsaveis_gantt': responsaveis_str,
                'sprint_associado_gantt': tarefa.sprint.nome if tarefa.sprint else 'Sem Sprint',
                'progresso_gantt_percentual': 100 if tarefa.status == 'FEITO' else (50 if tarefa.status == 'EM_ANDAMENTO' else 0)
            })
        return gantt_data

    def _get_equipe_data(self, projeto: Projeto) -> List[Dict[str, Any]]:
        """
        Coleta e formata os dados da equipe (membros) de um projeto.

        Args:
            projeto: A instância do modelo Projeto.

        Returns:
            Uma lista de dicionários, cada um representando um membro da equipe.
        """
        membros = MembroProjeto.objects.filter(projeto=projeto).select_related('usuario')
        equipe_data: List[Dict[str, Any]] = []

        for membro in membros:
            usuario = membro.usuario
            equipe_data.append({
                'id_membro': membro.id,
                'usuario_id': usuario.id,
                'usuario_username': usuario.username,
                'nome_completo_usuario': f"{usuario.first_name} {usuario.last_name}".strip(),
                'email_usuario': usuario.email,
                'papel_projeto': dict(MembroProjeto.PAPEL_CHOICES).get(membro.papel, membro.papel),
                'data_adicao_membro': membro.data_adicao.strftime('%Y-%m-%d') if membro.data_adicao else None,
            })
        return equipe_data

    def _get_riscos_data(self, projeto: Projeto) -> List[Dict[str, Any]]:
        """
        Coleta e formata os dados dos riscos associados a um projeto.
        Requer que o modelo Risco esteja disponível.

        Args:
            projeto: A instância do modelo Projeto.

        Returns:
            Uma lista de dicionários, cada um representando um risco.
        """
        from risks.models import Risco # Local import as in original

        riscos = Risco.objects.filter(projeto=projeto).select_related('responsavel_mitigacao')
        riscos_data: List[Dict[str, Any]] = []

        for risco in riscos:
            responsavel = risco.responsavel_mitigacao
            riscos_data.append({
                'id_risco': risco.id,
                'descricao_risco': risco.descricao,
                'probabilidade_risco': dict(Risco.PROBABILIDADE_CHOICES).get(risco.probabilidade, risco.probabilidade),
                'impacto_risco': dict(Risco.IMPACTO_CHOICES).get(risco.impacto, risco.impacto),
                'status_risco': dict(Risco.STATUS_CHOICES).get(risco.status, risco.status),
                'responsavel_mitigacao_username': responsavel.username if responsavel else None,
                'responsavel_mitigacao_nome_completo': f"{responsavel.first_name} {responsavel.last_name}".strip() if responsavel else None,
                'plano_mitigacao_risco': risco.plano_mitigacao,
                'plano_contingencia_risco': risco.plano_contingencia,
                'data_identificacao_risco': risco.data_identificacao.strftime('%Y-%m-%d') if risco.data_identificacao else None,
                'nivel_risco_calculado': risco.nivel_risco # Assuming this is a property or calculated field
            })
        return riscos_data

    def _get_custos_data(self, projeto: Projeto) -> List[Dict[str, Any]]:
        """
        Coleta e formata os dados dos custos associados a um projeto.
        Requer que o modelo Custo esteja disponível.

        Args:
            projeto: A instância do modelo Projeto.

        Returns:
            Uma lista de dicionários, cada um representando um custo.
        """
        from costs.models import Custo # Local import as in original
        # Removed the local import as it is now at the top of the file
        custos = Custo.objects.filter(projeto=projeto).select_related('categoria', 'tarefa', 'criado_por')
        custos_data: List[Dict[str, Any]] = []

        for custo in custos:
            custos_data.append({
                'id_custo': custo.id,
                'descricao_custo': custo.descricao,
                'valor_custo': str(custo.valor), # Decimal to string for serialization
                'tipo_custo': dict(Custo.TIPO_CHOICES).get(custo.tipo, custo.tipo),
                'categoria_custo': custo.categoria.nome if custo.categoria else None,
                'data_custo': custo.data.strftime('%Y-%m-%d') if custo.data else None,
                'observacoes_custo': custo.observacoes,
                'tarefa_associada_custo': custo.tarefa.titulo if custo.tarefa else None,
                'criado_por_custo': custo.criado_por.username if custo.criado_por else None,
                'criado_em_custo': custo.criado_em.strftime('%Y-%m-%d %H:%M') if custo.criado_em else None,
            })
        return custos_data

    def _export_csv(self, data: Dict[str, Any], filename: str) -> HttpResponse:
        """
        Exporta os dados coletados para um arquivo CSV.
        Cada chave principal no dicionário 'data' se torna uma seção no CSV.

        Args:
            data: Um dicionário onde as chaves são nomes de seção (e.g., 'projeto', 'tarefas')
                  e os valores são ou um dicionário (para seções de item único)
                  ou uma lista de dicionários (para seções de múltiplos itens).
            filename: O nome base para o arquivo CSV (sem a extensão .csv).

        Returns:
            HttpResponse contendo o arquivo CSV para download.
        """
        response = HttpResponse(content_type='text/csv; charset=utf-8') # Ensure UTF-8
        # Add UTF-8 BOM to ensure compatibility with Excel, which may misinterpret encoding without it.
        response.write(u'\ufeff'.encode('utf8'))
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

        writer = csv.writer(response)

        for section_name, section_data in data.items():
            if not section_data:  # Pular seções vazias
                continue

            writer.writerow([f"# SEÇÃO: {section_name.upper()}"]) # Cabeçalho da seção
            writer.writerow([]) # Linha em branco para espaçamento

            if isinstance(section_data, list) and section_data:
                # Seção com múltiplos itens (lista de dicionários)
                if isinstance(section_data[0], dict):
                    headers = list(section_data[0].keys())
                    writer.writerow(headers) # Cabeçalhos das colunas
                    for item in section_data:
                        writer.writerow([item.get(header, '') for header in headers])
                else: # Lista de itens simples (menos comum para esta estrutura)
                    for item in section_data:
                        writer.writerow([item])
            elif isinstance(section_data, dict):
                # Seção com item único (dicionário)
                headers = list(section_data.keys())
                writer.writerow(headers) # Chaves como cabeçalhos
                writer.writerow(list(section_data.values())) # Valores
            else:
                # Caso inesperado, apenas escreve o dado
                writer.writerow([str(section_data)])

            writer.writerow([]) # Linha em branco após a seção
            writer.writerow([]) # Mais uma linha em branco para melhor separação visual

        return response
        
    def _export_json(self, data: Dict[str, Any], filename: str, ensure_ascii: bool = False, indent: Optional[int] = 4) -> HttpResponse:
        """
        Exporta os dados coletados para um arquivo JSON.

        Args:
            data: Um dicionário contendo todos os dados a serem exportados.
            filename: O nome base para o arquivo JSON (sem a extensão .json).
            ensure_ascii: Define se os caracteres não-ASCII devem ser escapados.
            indent: Define o número de espaços para indentação no JSON. Use None para minificar.

        Returns:
            HttpResponse contendo o arquivo JSON para download.
        """
        response_content = json.dumps(data, ensure_ascii=ensure_ascii, indent=indent)
        response = HttpResponse(response_content, content_type='application/json; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}.json"'
        return response