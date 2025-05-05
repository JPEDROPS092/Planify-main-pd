#!/usr/bin/env python3
import os
import sys
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar ambiente Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planify.settings')
django.setup()

from django.contrib.auth import get_user_model
from projects.models import Projeto, Sprint
from tasks.models import Tarefa, AtribuicaoTarefa
from teams.models import Equipe, MembroEquipe
from risks.models import Risco
from costs.models import Categoria, Custo, OrcamentoProjeto
from documents.models import Documento
from communications.models import Comunicacao

User = get_user_model()

def create_users():
    """Criar usuários de exemplo"""
    users_data = [
        {'username': 'admin', 'email': 'admin@planify.com', 'password': 'admin123', 'is_staff': True, 'is_superuser': True},
        {'username': 'gerente', 'email': 'gerente@planify.com', 'password': 'gerente123'},
        {'username': 'dev1', 'email': 'dev1@planify.com', 'password': 'dev123'},
        {'username': 'dev2', 'email': 'dev2@planify.com', 'password': 'dev123'},
        {'username': 'analista', 'email': 'analista@planify.com', 'password': 'analista123'},
    ]
    
    created_users = []
    for data in users_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            email=data['email'],
            defaults={
                'is_staff': data.get('is_staff', False),
                'is_superuser': data.get('is_superuser', False)
            }
        )
        if created:
            user.set_password(data['password'])
            user.save()
        created_users.append(user)
    return created_users

def create_teams():
    """Criar equipes de exemplo"""
    users = User.objects.all()
    admin = User.objects.get(username='admin')
    
    teams_data = [
        {'nome': 'Time Alpha', 'descricao': 'Equipe principal de desenvolvimento'},
        {'nome': 'Time Beta', 'descricao': 'Equipe de inovação'},
        {'nome': 'Time Gamma', 'descricao': 'Equipe de suporte'},
    ]
    
    created_teams = []
    for data in teams_data:
        team = Equipe.objects.create(
            nome=data['nome'],
            descricao=data['descricao'],
            criado_por=admin
        )
        
        # Adicionar membros aleatórios à equipe
        for user in random.sample(list(users), 3):
            MembroEquipe.objects.create(
                equipe=team,
                usuario=user,
                papel=random.choice(['PO', 'SM', 'DEV', 'QA', 'DESIGN', 'ANALISTA']),
                adicionado_por=admin
            )
        created_teams.append(team)
    return created_teams

def create_projects():
    """Criar projetos de exemplo"""
    users = User.objects.all()
    admin = User.objects.get(username='admin')
    teams = Equipe.objects.all()
    
    project_names = [
        'Sistema de Monitoramento IoT',
        'Plataforma de Machine Learning',
        'Aplicativo de Realidade Aumentada',
        'Sistema de Automação Industrial',
        'Blockchain para Rastreabilidade'
    ]
    
    created_projects = []
    for name in project_names:
        start_date = timezone.now() - timedelta(days=random.randint(1, 90))
        end_date = start_date + timedelta(days=random.randint(90, 180))
        
        # Criar projeto
        project = Projeto.objects.create(
            titulo=name,
            descricao=f'Projeto de P&D focado em {name}',
            data_inicio=start_date,
            data_fim=end_date,
            status=random.choice(['PLANEJADO', 'EM_ANDAMENTO', 'CONCLUIDO']),
            prioridade=random.choice(['BAIXA', 'MEDIA', 'ALTA']),
            criado_por=admin
        )
        
        # Criar orçamento
        orcamento = OrcamentoProjeto.objects.create(
            projeto=project,
            valor_total=random.randint(100000, 1000000),
            aprovado_por=admin,
            observacoes='Orçamento inicial do projeto'
        )
        
        # Criar sprints
        sprint_start = start_date
        for i in range(3):
            sprint_end = sprint_start + timedelta(days=30)
            Sprint.objects.create(
                projeto=project,
                nome=f'Sprint {i+1}',
                descricao=f'Sprint {i+1} do projeto {name}',
                data_inicio=sprint_start,
                data_fim=sprint_end,
                status=random.choice(['PLANEJADO', 'EM_ANDAMENTO', 'CONCLUIDO']),
                criado_por=admin
            )
            sprint_start = sprint_end
        
        created_projects.append(project)
    return created_projects

def create_tasks():
    """Criar tarefas de exemplo"""
    projects = Projeto.objects.all()
    sprints = Sprint.objects.all()
    users = User.objects.all()
    admin = User.objects.get(username='admin')
    
    task_titles = [
        'Análise de Requisitos',
        'Desenvolvimento de Frontend',
        'Desenvolvimento de Backend',
        'Testes de Integração',
        'Documentação',
        'Deploy'
    ]
    
    for project in projects:
        project_sprints = project.sprints.all()
        for title in random.sample(task_titles, 4):
            sprint = random.choice(project_sprints) if project_sprints else None
            start_date = sprint.data_inicio if sprint else project.data_inicio
            end_date = sprint.data_fim if sprint else project.data_fim
            
            task = Tarefa.objects.create(
                titulo=title,
                descricao=f'Tarefa de {title} para o projeto {project.titulo}',
                data_inicio=start_date,
                data_termino=end_date,
                prioridade=random.choice(['BAIXA', 'MEDIA', 'ALTA']),
                status=random.choice(['A_FAZER', 'EM_ANDAMENTO', 'FEITO']),
                projeto=project,
                sprint=sprint,
                criado_por=admin
            )
            
            # Atribuir a tarefa a um usuário aleatório
            AtribuicaoTarefa.objects.create(
                tarefa=task,
                usuario=random.choice(users),
                atribuido_por=admin
            )

def create_risks():
    projects = Projeto.objects.all()
    users = User.objects.all()
    admin = User.objects.get(username='admin')
    
    risk_types = ['Técnico', 'Financeiro', 'Operacional', 'Legal']
    descriptions = [
        'Atraso na entrega de componentes',
        'Problemas de integração',
        'Mudança de requisitos',
        'Falha de comunicação'
    ]
    
    for project in projects:
        for _ in range(random.randint(2, 5)):
            Risco.objects.create(
                projeto=project,
                descricao=random.choice(descriptions),
                probabilidade=random.choice(['BAIXA', 'MEDIA', 'ALTA']),
                impacto=random.choice(['BAIXO', 'MEDIO', 'ALTO']),
                status=random.choice(['IDENTIFICADO', 'EM_ANALISE', 'MITIGADO']),
                responsavel_mitigacao=random.choice(users),
                plano_mitigacao='Plano de mitigação detalhado...',
                plano_contingencia='Plano de contingência detalhado...',
                criado_por=admin
            )

def create_costs():
    projects = Projeto.objects.all()
    tasks = Tarefa.objects.all()
    users = User.objects.all()
    admin = User.objects.get(username='admin')
    
    # Criar categorias
    categorias = []
    for nome in ['Equipamentos', 'Software', 'Pessoal', 'Serviços', 'Materiais']:
        categoria = Categoria.objects.create(
            nome=nome,
            descricao=f'Custos relacionados a {nome.lower()}'
        )
        categorias.append(categoria)
    
    for project in projects:
        # Custos do projeto
        for _ in range(random.randint(3, 6)):
            Custo.objects.create(
                projeto=project,
                categoria=random.choice(categorias),
                descricao=f'Custo de {random.choice(categorias).nome.lower()}',
                valor=random.randint(1000, 10000),
                tipo=random.choice(['FIXO', 'VARIAVEL', 'RECORRENTE']),
                data=timezone.now().date() - timedelta(days=random.randint(0, 30)),
                observacoes='Observações sobre o custo...',
                criado_por=admin
            )
        
        # Custos das tarefas
        project_tasks = tasks.filter(projeto=project)
        for task in project_tasks:
            if random.choice([True, False]):
                Custo.objects.create(
                    projeto=project,
                    tarefa=task,
                    categoria=random.choice(categorias),
                    descricao=f'Custo da tarefa: {task.titulo}',
                    valor=random.randint(500, 5000),
                    tipo=random.choice(['FIXO', 'VARIAVEL']),
                    data=task.data_inicio,
                    observacoes='Custo específico da tarefa...',
                    criado_por=admin
                )

def create_documents():
    projects = Projeto.objects.all()
    tasks = Tarefa.objects.all()
    users = User.objects.all()
    admin = User.objects.get(username='admin')
    
    doc_types = ['REQUISITO', 'DESIGN', 'MANUAL', 'RELATORIO', 'ATA', 'OUTRO']
    
    for project in projects:
        # Documentos do projeto
        for _ in range(random.randint(2, 5)):
            tipo = random.choice(doc_types)
            Documento.objects.create(
                projeto=project,
                titulo=f'{tipo.title()} - {project.titulo}',
                descricao=f'Documento de {tipo.lower()} do projeto',
                tipo=tipo,
                tamanho_arquivo=random.randint(1024, 5120),  # 1KB a 5KB
                tipo_arquivo='application/pdf',
                versao=f'1.{random.randint(0,9)}',
                enviado_por=admin
            )
        
        # Documentos das tarefas
        project_tasks = tasks.filter(projeto=project)
        for task in project_tasks:
            if random.choice([True, False]):
                tipo = random.choice(doc_types)
                Documento.objects.create(
                    projeto=project,
                    tarefa=task,
                    titulo=f'{tipo.title()} - {task.titulo}',
                    descricao=f'Documento de {tipo.lower()} da tarefa',
                    tipo=tipo,
                    tamanho_arquivo=random.randint(1024, 5120),  # 1KB a 5KB
                    tipo_arquivo='application/pdf',
                    versao='1.0',
                    enviado_por=admin
                )

def create_communications():
    """Criar comunicações e notificações de exemplo"""
    projects = Projeto.objects.all()
    users = User.objects.all()
    
    # Criar comunicações
    for project in projects:
        for _ in range(random.randint(3, 6)):
            remetente = random.choice(users)
            comunicacao = Comunicacao.objects.create(
                projeto=project,
                titulo=f'Comunicação sobre {project.titulo}',
                texto=f'Esta é uma comunicação de teste enviada por {remetente.username}',
                remetente=remetente,
                criada_em=timezone.now() - timedelta(days=random.randint(0, 30))
            )
            # Adicionar destinatários aleatórios
            destinatarios = random.sample(list(users), random.randint(1, len(users)))
            comunicacao.destinatarios.add(*destinatarios)
    
    # Criar notificações
    tipos = ['TAREFA', 'PROJETO', 'EQUIPE', 'RISCO', 'DOCUMENTO', 'SISTEMA']
    for user in users:
        for _ in range(random.randint(2, 5)):
            tipo = random.choice(tipos)
            Notificacao.objects.create(
                usuario=user,
                tipo=tipo,
                titulo=f'Notificação de {tipo.lower()}',
                mensagem=f'Esta é uma notificação de teste do tipo {tipo.lower()}',
                prioridade=random.choice(['BAIXA', 'MEDIA', 'ALTA']),
                projeto=random.choice(projects)
            )

def run_seeds():
    print("Iniciando seed do banco de dados...")
    
    print("Criando usuários...")
    create_users()
    
    print("Criando equipes...")
    create_teams()
    
    print("Criando projetos...")
    create_projects()
    
    print("Criando tarefas...")
    create_tasks()
    
    print("Criando riscos...")
    create_risks()
    
    print("Criando custos...")
    create_costs()
    
    print("Criando documentos...")
    create_documents()
    
    print("Criando comunicações...")
    create_communications()
    
    print("Seed concluído com sucesso!")

if __name__ == '__main__':
    run_seeds()
