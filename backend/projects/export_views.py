from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import csv
import json
from datetime import datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from .models import Projeto, MembroProjeto, Sprint
from tasks.models import Tarefa, AtribuicaoTarefa
from .api_schemas import ExportResponseSerializer, ErrorResponseSerializer


@extend_schema(
    summary="Exportar dados do projeto",
    description="Exporta dados do projeto em diferentes formatos (CSV, JSON)",
    parameters=[
        OpenApiParameter(name='projeto_id', description='ID do projeto', required=True, type=int),
        OpenApiParameter(name='format', description='Formato de exportação (csv, json)', required=False, type=str, default='csv'),
        OpenApiParameter(name='include_project', description='Incluir dados do projeto', required=False, type=bool, default=True),
        OpenApiParameter(name='include_tasks', description='Incluir tarefas do projeto', required=False, type=bool, default=True),
        OpenApiParameter(name='include_team', description='Incluir equipe do projeto', required=False, type=bool, default=False),
        OpenApiParameter(name='include_risks', description='Incluir riscos do projeto', required=False, type=bool, default=False),
        OpenApiParameter(name='include_costs', description='Incluir custos do projeto', required=False, type=bool, default=False)
    ],
    responses={
        200: OpenApiTypes.BINARY,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer
    },
    tags=["Projetos", "Exportação"]
)
class ProjetoExportView(APIView):
    """
    View para exportar dados do projeto em diferentes formatos (CSV, JSON).
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, projeto_id, format=None):
        # Buscar o projeto pelo ID
        projeto = get_object_or_404(Projeto, id=projeto_id)
        
        # Verificar se o usuário tem acesso ao projeto
        if not MembroProjeto.objects.filter(projeto=projeto, usuario=request.user).exists() and not request.user.is_staff:
            return Response(
                {"detail": "Você não tem permissão para acessar este projeto."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Determinar o formato de exportação
        export_format = request.query_params.get('format', 'csv').lower()
        
        # Verificar quais dados devem ser incluídos
        include_project = request.query_params.get('include_project', 'true').lower() == 'true'
        include_tasks = request.query_params.get('include_tasks', 'true').lower() == 'true'
        include_team = request.query_params.get('include_team', 'false').lower() == 'true'
        include_risks = request.query_params.get('include_risks', 'false').lower() == 'true'
        include_costs = request.query_params.get('include_costs', 'false').lower() == 'true'
        
        # Se nenhuma opção for selecionada, retornar erro
        if not any([include_project, include_tasks, include_team, include_risks, include_costs]):
            return Response(
                {"detail": "Selecione pelo menos um tipo de dado para exportar."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Preparar os dados para exportação
        export_data = {}
        
        if include_project:
            export_data['projeto'] = self._get_projeto_data(projeto)
            
        if include_tasks:
            export_data['tarefas'] = self._get_tarefas_data(projeto)
            export_data['kanban'] = self._get_kanban_data(projeto)
            export_data['gantt'] = self._get_gantt_data(projeto)
            
        if include_team:
            export_data['equipe'] = self._get_equipe_data(projeto)
            
        if include_risks:
            export_data['riscos'] = self._get_riscos_data(projeto)
            
        if include_costs:
            export_data['custos'] = self._get_custos_data(projeto)
        
        # Nome do arquivo
        filename = f"projeto_{projeto.id}_{projeto.titulo.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        
        # Exportar no formato solicitado
        if export_format == 'csv':
            return self._export_csv(export_data, filename)
        elif export_format == 'json':
            return self._export_json(export_data, filename)
        else:
            return Response(
                {"detail": "Formato de exportação inválido. Opções: csv, json"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def _get_tarefas_data(self, projeto):
        """Obtém dados das tarefas do projeto."""
        tarefas = Tarefa.objects.filter(projeto=projeto)
        data = []
        
        for tarefa in tarefas:
            responsaveis = AtribuicaoTarefa.objects.filter(tarefa=tarefa).values_list('usuario__username', flat=True)
            responsaveis_str = ", ".join(responsaveis)
            
            data.append({
                'id': tarefa.id,
                'titulo': tarefa.titulo,
                'descricao': tarefa.descricao,
                'data_inicio': tarefa.data_inicio.strftime('%Y-%m-%d'),
                'data_termino': tarefa.data_termino.strftime('%Y-%m-%d'),
                'status': dict(Tarefa.STATUS_CHOICES).get(tarefa.status, tarefa.status),
                'prioridade': dict(Tarefa.PRIORITY_CHOICES).get(tarefa.prioridade, tarefa.prioridade),
                'responsaveis': responsaveis_str,
                'sprint': tarefa.sprint.nome if tarefa.sprint else 'Sem Sprint',
                'criado_por': tarefa.criado_por.username if tarefa.criado_por else 'Desconhecido',
                'criado_em': tarefa.criado_em.strftime('%Y-%m-%d %H:%M')
            })
        
        return data
    
    def _get_kanban_data(self, projeto):
        """Obtém dados do Kanban do projeto."""
        tarefas = Tarefa.objects.filter(projeto=projeto)
        kanban_data = {
            'A_FAZER': [],
            'EM_ANDAMENTO': [],
            'FEITO': []
        }
        
        for status in kanban_data.keys():
            tarefas_status = tarefas.filter(status=status)
            
            for tarefa in tarefas_status:
                responsaveis = AtribuicaoTarefa.objects.filter(tarefa=tarefa).values_list('usuario__username', flat=True)
                responsaveis_str = ", ".join(responsaveis)
                
                kanban_data[status].append({
                    'id': tarefa.id,
                    'titulo': tarefa.titulo,
                    'descricao': tarefa.descricao,
                    'data_inicio': tarefa.data_inicio.strftime('%Y-%m-%d'),
                    'data_termino': tarefa.data_termino.strftime('%Y-%m-%d'),
                    'prioridade': dict(Tarefa.PRIORITY_CHOICES).get(tarefa.prioridade, tarefa.prioridade),
                    'responsaveis': responsaveis_str,
                    'sprint': tarefa.sprint.nome if tarefa.sprint else 'Sem Sprint'
                })
        
        # Converter para formato de lista para CSV
        result = []
        for status, tarefas in kanban_data.items():
            status_nome = dict(Tarefa.STATUS_CHOICES).get(status, status)
            for tarefa in tarefas:
                tarefa_data = tarefa.copy()
                tarefa_data['status'] = status_nome
                result.append(tarefa_data)
        
        return result
    
    def _get_gantt_data(self, projeto):
        """Obtém dados do Gantt do projeto."""
        tarefas = Tarefa.objects.filter(projeto=projeto)
        gantt_data = []
        
        # Adicionar o projeto
        gantt_data.append({
            'id': f"projeto_{projeto.id}",
            'titulo': f"Projeto: {projeto.titulo}",
            'tipo': 'projeto',
            'data_inicio': projeto.data_inicio.strftime('%Y-%m-%d'),
            'data_fim': projeto.data_fim.strftime('%Y-%m-%d'),
            'status': dict(Projeto.STATUS_CHOICES).get(projeto.status, projeto.status),
            'progresso': '100%' if projeto.status == 'CONCLUIDO' else ('50%' if projeto.status == 'EM_ANDAMENTO' else '0%')
        })
        
        # Adicionar sprints
        sprints = Sprint.objects.filter(projeto=projeto)
        for sprint in sprints:
            gantt_data.append({
                'id': f"sprint_{sprint.id}",
                'titulo': f"Sprint: {sprint.nome}",
                'tipo': 'sprint',
                'data_inicio': sprint.data_inicio.strftime('%Y-%m-%d'),
                'data_fim': sprint.data_fim.strftime('%Y-%m-%d'),
                'status': dict(Sprint.STATUS_CHOICES).get(sprint.status, sprint.status),
                'progresso': '100%' if sprint.status == 'CONCLUIDO' else ('50%' if sprint.status == 'EM_ANDAMENTO' else '0%')
            })
        
        # Adicionar tarefas
        for tarefa in tarefas:
            responsaveis = AtribuicaoTarefa.objects.filter(tarefa=tarefa).values_list('usuario__username', flat=True)
            responsaveis_str = ", ".join(responsaveis)
            
            gantt_data.append({
                'id': f"tarefa_{tarefa.id}",
                'titulo': tarefa.titulo,
                'tipo': 'tarefa',
                'data_inicio': tarefa.data_inicio.strftime('%Y-%m-%d'),
                'data_fim': tarefa.data_termino.strftime('%Y-%m-%d'),
                'status': dict(Tarefa.STATUS_CHOICES).get(tarefa.status, tarefa.status),
                'prioridade': dict(Tarefa.PRIORITY_CHOICES).get(tarefa.prioridade, tarefa.prioridade),
                'responsaveis': responsaveis_str,
                'sprint': tarefa.sprint.nome if tarefa.sprint else 'Sem Sprint',
                'progresso': '100%' if tarefa.status == 'FEITO' else ('50%' if tarefa.status == 'EM_ANDAMENTO' else '0%')
            })
        
        return gantt_data
    
    def _get_projeto_data(self, projeto):
        """Obtém dados básicos do projeto."""
        return {
            'id': projeto.id,
            'titulo': projeto.titulo,
            'descricao': projeto.descricao,
            'data_inicio': projeto.data_inicio.strftime('%Y-%m-%d'),
            'data_fim': projeto.data_fim.strftime('%Y-%m-%d') if projeto.data_fim else None,
            'status': dict(Projeto.STATUS_CHOICES).get(projeto.status, projeto.status),
            'prioridade': dict(Projeto.PRIORIDADE_CHOICES).get(projeto.prioridade, projeto.prioridade),
            'gerente': projeto.gerente.username if projeto.gerente else None,
            'gerente_nome': f"{projeto.gerente.first_name} {projeto.gerente.last_name}" if projeto.gerente else None,
            'criado_por': projeto.criado_por.username if projeto.criado_por else None,
            'criado_em': projeto.criado_em.strftime('%Y-%m-%d %H:%M'),
            'atualizado_em': projeto.atualizado_em.strftime('%Y-%m-%d %H:%M'),
            'arquivado': projeto.arquivado
        }
    
    def _get_equipe_data(self, projeto):
        """Obtém dados da equipe do projeto."""
        membros = MembroProjeto.objects.filter(projeto=projeto)
        equipe_data = []
        
        for membro in membros:
            equipe_data.append({
                'id': membro.id,
                'usuario_id': membro.usuario.id,
                'usuario': membro.usuario.username,
                'nome': f"{membro.usuario.first_name} {membro.usuario.last_name}".strip(),
                'email': membro.usuario.email,
                'papel': dict(MembroProjeto.PAPEL_CHOICES).get(membro.papel, membro.papel),
                'data_adicao': membro.data_adicao.strftime('%Y-%m-%d')
            })
        
        return equipe_data
    
    def _get_riscos_data(self, projeto):
        """Obtém dados dos riscos do projeto."""
        from risks.models import Risco
        
        riscos = Risco.objects.filter(projeto=projeto)
        riscos_data = []
        
        for risco in riscos:
            riscos_data.append({
                'id': risco.id,
                'descricao': risco.descricao,
                'probabilidade': dict(Risco.PROBABILIDADE_CHOICES).get(risco.probabilidade, risco.probabilidade),
                'impacto': dict(Risco.IMPACTO_CHOICES).get(risco.impacto, risco.impacto),
                'status': dict(Risco.STATUS_CHOICES).get(risco.status, risco.status),
                'responsavel': risco.responsavel_mitigacao.username if risco.responsavel_mitigacao else None,
                'responsavel_nome': f"{risco.responsavel_mitigacao.first_name} {risco.responsavel_mitigacao.last_name}" if risco.responsavel_mitigacao else None,
                'plano_mitigacao': risco.plano_mitigacao,
                'plano_contingencia': risco.plano_contingencia,
                'data_identificacao': risco.data_identificacao.strftime('%Y-%m-%d'),
                'nivel_risco': risco.nivel_risco
            })
        
        return riscos_data
    
    def _get_custos_data(self, projeto):
        """Obtém dados dos custos do projeto."""
        from costs.models import Custo
        
        custos = Custo.objects.filter(projeto=projeto)
        custos_data = []
        
        for custo in custos:
            custos_data.append({
                'id': custo.id,
                'descricao': custo.descricao,
                'valor': str(custo.valor),
                'tipo': dict(Custo.TIPO_CHOICES).get(custo.tipo, custo.tipo),
                'categoria': custo.categoria.nome if custo.categoria else None,
                'data': custo.data.strftime('%Y-%m-%d'),
                'observacoes': custo.observacoes,
                'tarefa': custo.tarefa.titulo if custo.tarefa else None,
                'criado_por': custo.criado_por.username if custo.criado_por else None,
                'criado_em': custo.criado_em.strftime('%Y-%m-%d %H:%M')
            })
        
        return custos_data
    
    def _export_csv(self, data, filename):
        """Exporta dados para CSV."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        response.write(u'\ufeff'.encode('utf8'))  # BOM para Excel
        
        # Se os dados estão em formato de dicionário com múltiplas seções
        if isinstance(data, dict):
            # Criar um arquivo CSV com múltiplas seções
            writer = csv.writer(response)
            
            for section_name, section_data in data.items():
                if not section_data:  # Pular seções vazias
                    continue
                    
                # Adicionar cabeçalho da seção
                writer.writerow([f"# {section_name.upper()}"])
                writer.writerow([])
                
                if isinstance(section_data, list) and section_data:
                    # Adicionar cabeçalhos das colunas
                    writer.writerow(section_data[0].keys())
                    
                    # Adicionar dados
                    for item in section_data:
                        writer.writerow(item.values())
                    
                    # Adicionar linha em branco entre seções
                    writer.writerow([])
                    writer.writerow([])
                elif isinstance(section_data, dict):
                    # Para dados em formato de dicionário simples
                    writer.writerow(section_data.keys())
                    writer.writerow(section_data.values())
                    writer.writerow([])
                    writer.writerow([])
        else:
            # Formato antigo para compatibilidade
            if data and isinstance(data, list):
                writer = csv.DictWriter(response, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        
        return response
    
    def _export_json(self, data, filename):
        """Exporta dados para JSON."""
        response = HttpResponse(json.dumps(data, ensure_ascii=False, indent=4), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}.json"'
        return response
