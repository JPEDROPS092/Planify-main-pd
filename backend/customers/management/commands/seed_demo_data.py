"""Seed idempotente de **dev**: cria o tenant Demo, o owner Demo e dados de negocio.

Comando apenas de desenvolvimento. Garante o tenant ``Demo`` e o seu owner (antes
ficavam no ``seed_initial``) e em seguida popula dados de negocio idempotentes.
Em producao, tenants reais sao criados via ``provision_tenant`` (nunca por aqui).
Pre-requisito: o superuser SaaS, criado por ``seed_initial``.
"""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from communications.models import (
    ChatMensagem,
    ChatMensagemLeitura,
    Comunicacao,
    ConfiguracaoNotificacao,
    Notificacao,
)
from costs.models import Categoria, Custo, OrcamentoProjeto, OrcamentoTarefa
from customers import context
from customers.models import TenantMembership
from customers.provisioning import ensure_owner_membership, ensure_tenant, ensure_user
from documents.models import Comentario as ComentarioDocumento
from documents.models import Documento, HistoricoDocumento
from projects.models import MembroProjeto, Projeto, Sprint
from risks.models import HistoricoRisco, Risco
from tasks.models import AtribuicaoTarefa, ComentarioTarefa, HistoricoStatusTarefa, Tarefa
from teams.models import Equipe, MembroEquipe, PermissaoEquipe


class Command(BaseCommand):
    help = 'Cria o tenant Demo + owner Demo e semeia dados de negocio idempotentes (dev).'

    def add_arguments(self, parser):
        parser.add_argument('--tenant-name', default='Demo')
        parser.add_argument('--tenant-slug', default='demo')
        parser.add_argument('--owner-username', default='demo_owner')
        parser.add_argument('--owner-email', default='owner@demo.local')
        parser.add_argument('--owner-password', default='owner123')
        parser.add_argument('--owner-full-name', default='Owner Demo')
        parser.add_argument(
            '--reset-passwords',
            action='store_true',
            help='Tambem redefine a senha do owner se ele ja existir.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        tenant, _ = ensure_tenant(
            slug=options['tenant_slug'],
            name=options['tenant_name'],
        )
        owner = ensure_user(
            username=options['owner_username'],
            email=options['owner_email'],
            full_name=options['owner_full_name'],
            password=options['owner_password'],
            role='PROJECT_MANAGER',
            reset_password=options['reset_passwords'],
        )
        ensure_owner_membership(user=owner, tenant=tenant)

        with context.scope(tenant_id=tenant.id):
            users = self._tenant_users()
            actor = self._seed_actor(users)
            today = timezone.localdate()

            teams = self._seed_teams(users, actor)
            project = self._seed_project(actor, users, today)
            sprint = self._seed_sprint(project, actor, today)
            tasks = self._seed_tasks(project, sprint, actor, users, today)
            categories = self._seed_costs(project, tasks, actor, today)
            document = self._seed_documents(project, tasks[0], actor)
            risk = self._seed_risks(project, actor)
            self._seed_communications(project, tasks[0], document, users, actor)
            self._seed_team_permissions(teams)

        self.stdout.write(self.style.SUCCESS(
            f'Dados demo garantidos para tenant {tenant.name} '
            f'(slug={tenant.slug}, projeto="{project.titulo}", '
            f'tarefas={len(tasks)}, categorias={len(categories)}, risco={risk.id}).'
        ))

    def _tenant_users(self):
        User = get_user_model()
        users = list(
            User.objects.filter(
                tenant_memberships__tenant_id=context.get_tenant_id(),
                tenant_memberships__is_active=True,
                is_active=True,
            ).exclude(is_superuser=True).distinct().order_by('id')
        )
        if not users:
            raise CommandError(
                'Nenhum usuario ativo vinculado ao tenant. Rode `python manage.py seed_initial` antes.'
            )
        return users

    def _seed_actor(self, users):
        membership = (
            TenantMembership.objects
            .filter(
                tenant_id=context.get_tenant_id(),
                is_active=True,
                role__in=[TenantMembership.ROLE_OWNER, TenantMembership.ROLE_ADMIN],
                user__is_active=True,
            )
            .exclude(user__is_superuser=True)
            .select_related('user')
            .first()
        )
        return membership.user if membership else users[0]

    def _seed_teams(self, users, actor):
        teams = []
        for data in (
            {'nome': 'Time Demo Produto', 'descricao': 'Equipe principal do tenant Demo.'},
            {'nome': 'Time Demo Pesquisa', 'descricao': 'Equipe de pesquisa aplicada.'},
        ):
            team, _ = Equipe.objects.update_or_create(
                nome=data['nome'],
                defaults={'descricao': data['descricao'], 'criado_por': actor},
            )
            teams.append(team)
            for index, user in enumerate(users[:3] or [actor]):
                MembroEquipe.objects.update_or_create(
                    equipe=team,
                    usuario=user,
                    defaults={
                        'papel': ['PO', 'DEV', 'QA'][min(index, 2)],
                        'adicionado_por': actor,
                    },
                )
        return teams

    def _seed_project(self, actor, users, today):
        project, _ = Projeto.objects.update_or_create(
            titulo='Projeto Demo P&D',
            defaults={
                'descricao': 'Projeto demonstrativo para validar o fluxo multi-tenant.',
                'data_inicio': today,
                'data_fim': today + timedelta(days=120),
                'status': 'EM_ANDAMENTO',
                'prioridade': 'ALTA',
                'criado_por': actor,
                'arquivado': False,
            },
        )
        for index, user in enumerate(users):
            MembroProjeto.objects.update_or_create(
                projeto=project,
                usuario=user,
                defaults={'papel': 'GERENTE' if index == 0 else 'DESENVOLVEDOR'},
            )
        return project

    def _seed_sprint(self, project, actor, today):
        sprint, _ = Sprint.objects.update_or_create(
            projeto=project,
            nome='Sprint Demo 1',
            defaults={
                'descricao': 'Primeira sprint do projeto demo.',
                'data_inicio': today,
                'data_fim': today + timedelta(days=21),
                'status': 'EM_ANDAMENTO',
                'criado_por': actor,
            },
        )
        return sprint

    def _seed_tasks(self, project, sprint, actor, users, today):
        task_specs = (
            ('Mapear requisitos do tenant Demo', 'A_FAZER', 'ALTA', 7),
            ('Configurar quadro Kanban inicial', 'EM_ANDAMENTO', 'MEDIA', 14),
            ('Validar convite e aceite de membros', 'A_FAZER', 'ALTA', 21),
        )
        tasks = []
        for index, (title, status, priority, days) in enumerate(task_specs):
            task, _ = Tarefa.objects.update_or_create(
                projeto=project,
                titulo=title,
                defaults={
                    'descricao': f'Tarefa demo: {title}.',
                    'data_inicio': today,
                    'data_termino': today + timedelta(days=days),
                    'prioridade': priority,
                    'status': status,
                    'sprint': sprint,
                    'criado_por': actor,
                    'atualizado_por': actor,
                },
            )
            tasks.append(task)
            assignee = users[min(index, len(users) - 1)]
            AtribuicaoTarefa.objects.update_or_create(
                tarefa=task,
                usuario=assignee,
                defaults={'atribuido_por': actor},
            )
            ComentarioTarefa.objects.get_or_create(
                tarefa=task,
                autor=actor,
                texto='Comentario demo para validar colaboracao em tarefas.',
            )
            HistoricoStatusTarefa.objects.get_or_create(
                tarefa=task,
                status_anterior='A_FAZER',
                novo_status=status,
                defaults={'alterado_por': actor},
            )
        return tasks

    def _seed_costs(self, project, tasks, actor, today):
        categories = []
        for name in ('Pessoal', 'Software', 'Servicos'):
            category, _ = Categoria.objects.update_or_create(
                nome=name,
                defaults={'descricao': f'Categoria demo de custos: {name}.'},
            )
            categories.append(category)

        OrcamentoProjeto.objects.update_or_create(
            projeto=project,
            defaults={
                'valor_total': 250000,
                'aprovado_por': actor,
                'observacoes': 'Orcamento demo para validacao do modulo de custos.',
            },
        )
        for task in tasks[:2]:
            OrcamentoTarefa.objects.update_or_create(
                tarefa=task,
                defaults={
                    'valor': 25000,
                    'aprovado_por': actor,
                    'observacoes': 'Orcamento demo da tarefa.',
                },
            )

        Custo.objects.update_or_create(
            projeto=project,
            descricao='Licencas e ferramentas demo',
            defaults={
                'categoria': categories[1],
                'valor': 12000,
                'tipo': 'FIXO',
                'data': today,
                'observacoes': 'Custo demo idempotente.',
                'criado_por': actor,
            },
        )
        return categories

    def _seed_documents(self, project, task, actor):
        document, _ = Documento.objects.update_or_create(
            projeto=project,
            titulo='Plano do Projeto Demo',
            defaults={
                'tarefa': task,
                'descricao': 'Documento demo para validar repositorio de documentos.',
                'tipo': 'RELATORIO',
                'arquivo': 'documentos/demo/plano-projeto-demo.pdf',
                'tamanho_arquivo': 2048,
                'tipo_arquivo': 'application/pdf',
                'versao': '1.0',
                'enviado_por': actor,
            },
        )
        HistoricoDocumento.objects.get_or_create(
            documento=document,
            versao_anterior='0.9',
            defaults={
                'arquivo_anterior': 'documentos/demo/plano-projeto-demo-v0.pdf',
                'tamanho_arquivo': 1536,
                'alterado_por': actor,
                'observacao': 'Versao inicial demo.',
            },
        )
        ComentarioDocumento.objects.get_or_create(
            documento=document,
            autor=actor,
            texto='Comentario demo para validar discussoes em documentos.',
        )
        return document

    def _seed_risks(self, project, actor):
        risk, _ = Risco.objects.update_or_create(
            projeto=project,
            descricao='Dependencia de validacao frontend ponta-a-ponta',
            defaults={
                'probabilidade': 'MEDIA',
                'impacto': 'ALTO',
                'status': 'EM_ANALISE',
                'responsavel_mitigacao': actor,
                'plano_mitigacao': 'Validar login, convites e operacao do tenant Demo.',
                'plano_contingencia': 'Executar smoke manual via API antes do frontend.',
                'criado_por': actor,
            },
        )
        HistoricoRisco.objects.get_or_create(
            risco=risk,
            status_anterior='IDENTIFICADO',
            novo_status='EM_ANALISE',
            probabilidade_anterior='MEDIA',
            nova_probabilidade='MEDIA',
            impacto_anterior='ALTO',
            novo_impacto='ALTO',
            defaults={
                'alterado_por': actor,
                'observacao': 'Risco demo colocado em analise.',
            },
        )
        return risk

    def _seed_communications(self, project, task, document, users, actor):
        message, _ = ChatMensagem.objects.update_or_create(
            projeto=project,
            autor=actor,
            texto='Mensagem demo para validar o chat do projeto.',
            defaults={'editado': False},
        )
        for user in users:
            if user != actor:
                ChatMensagemLeitura.objects.get_or_create(mensagem=message, usuario=user)

        communication, _ = Comunicacao.objects.update_or_create(
            projeto=project,
            titulo='Comunicado Demo',
            defaults={
                'tipo': 'COMUNICADO',
                'texto': 'Comunicado demo para validar comunicacoes formais.',
                'remetente': actor,
            },
        )
        communication.destinatarios.set(users)

        for user in users:
            ConfiguracaoNotificacao.objects.update_or_create(
                usuario=user,
                defaults={
                    'tarefa_atribuida': 'SISTEMA',
                    'tarefa_comentario': 'SISTEMA',
                    'tarefa_prazo': 'AMBOS',
                    'projeto_status': 'SISTEMA',
                    'equipe_alteracao': 'SISTEMA',
                    'documento_novo': 'SISTEMA',
                    'risco_novo': 'SISTEMA',
                    'mensagem_chat': 'SISTEMA',
                },
            )
            Notificacao.objects.update_or_create(
                usuario=user,
                titulo='Bem-vindo ao tenant Demo',
                defaults={
                    'tipo': 'SISTEMA',
                    'mensagem': 'Dados demo foram preparados para validacao local.',
                    'prioridade': 'MEDIA',
                    'projeto': project,
                    'tarefa': task,
                    'url': f'http://localhost:3000/projects/{project.id}',
                    'lida': False,
                    'lida_em': None,
                },
            )
        return document

    def _seed_team_permissions(self, teams):
        for team in teams:
            for papel in ('PO', 'DEV', 'QA'):
                for modulo in ('TAREFAS', 'DOCUMENTOS'):
                    PermissaoEquipe.objects.get_or_create(
                        equipe=team,
                        papel=papel,
                        modulo=modulo,
                        permissao='VISUALIZAR',
                    )
