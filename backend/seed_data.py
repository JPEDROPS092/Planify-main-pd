#!/usr/bin/env python3
import os
import sys
import django
import random
import string
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar ambiente Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planify.settings')
django.setup()

from django.contrib.auth import get_user_model
from projects.models import Projeto, Sprint
from tasks.models import Tarefa, AtribuicaoTarefa, ComentarioTarefa, HistoricoStatusTarefa
from teams.models import Equipe, MembroEquipe
from risks.models import Risco, HistoricoRisco
from costs.models import Categoria, Custo, OrcamentoProjeto
from documents.models import Documento, HistoricoDocumento, Comentario
from communications.models import Comunicacao, Notificacao, ConfiguracaoNotificacao, ChatMensagem, ChatMensagemLeitura

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
        'Blockchain para Rastreabilidade',
        'Portal de Gestão de Conhecimento',
        'Aplicação de Análise de Dados',
        'Sistema de Gestão de Recursos',
        'Plataforma de E-commerce',
        'Aplicação Móvel Corporativa'
    ]
    
    # Verificar projetos existentes
    existing_titles = set(Projeto.objects.values_list('titulo', flat=True))
    
    created_projects = []
    for name in project_names:
        # Verificar se o projeto já existe e adicionar um sufixo aleatório se necessário
        base_name = name
        suffix = 1
        unique_name = base_name
        
        while unique_name in existing_titles:
            unique_name = f"{base_name} - V{suffix}"
            suffix += 1
        
        # Adicionar o título único à lista de títulos existentes
        existing_titles.add(unique_name)
        
        start_date = timezone.now() - timedelta(days=random.randint(1, 90))
        end_date = start_date + timedelta(days=random.randint(90, 180))
        
        try:
            # Criar projeto
            project = Projeto.objects.create(
                titulo=unique_name,
                descricao=f'Projeto de P&D focado em {base_name}',
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
                    descricao=f'Sprint {i+1} do projeto {unique_name}',
                    data_inicio=sprint_start,
                    data_fim=sprint_end,
                    status=random.choice(['PLANEJADO', 'EM_ANDAMENTO', 'CONCLUIDO']),
                    criado_por=admin
                )
                sprint_start = sprint_end
            
            created_projects.append(project)
            print(f"Projeto criado: {unique_name}")
        except Exception as e:
            print(f"Erro ao criar projeto {unique_name}: {str(e)}")
    
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
        'Deploy',
        'Revisão de Código',
        'Criação de Testes Unitários',
        'Design de Interface',
        'Otimização de Performance',
        'Configuração de Ambiente',
        'Migração de Dados'
    ]
    
    # Verificar tarefas existentes por projeto
    for project in projects:
        try:
            project_sprints = project.sprints.all()
            
            # Obter tarefas existentes para este projeto
            existing_tasks = set(Tarefa.objects.filter(projeto=project).values_list('titulo', flat=True))
            
            # Selecionar títulos aleatórios que ainda não existem para este projeto
            available_titles = [t for t in task_titles if t not in existing_tasks]
            
            # Se não houver títulos disponíveis, adicionar sufixos aos existentes
            if not available_titles:
                available_titles = [f"{t} - {random.randint(1, 100)}" for t in task_titles]
            
            # Criar entre 2 e 6 tarefas por projeto
            for title in random.sample(available_titles, min(random.randint(2, 6), len(available_titles))):
                try:
                    sprint = random.choice(project_sprints) if project_sprints.exists() else None
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
                    
                    print(f"Tarefa criada: {title} para o projeto {project.titulo}")
                except Exception as e:
                    print(f"Erro ao criar tarefa {title} para o projeto {project.titulo}: {str(e)}")
        except Exception as e:
            print(f"Erro ao processar tarefas para o projeto {project.titulo}: {str(e)}")

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
            projeto = random.choice(projects)
            tarefa = None
            if tipo == 'TAREFA' and Tarefa.objects.filter(projeto=projeto).exists():
                tarefa = random.choice(Tarefa.objects.filter(projeto=projeto))
            
            Notificacao.objects.create(
                usuario=user,
                tipo=tipo,
                titulo=f'Notificação de {tipo.lower()}',
                mensagem=f'Esta é uma notificação de teste do tipo {tipo.lower()}',
                prioridade=random.choice(['BAIXA', 'MEDIA', 'ALTA']),
                projeto=projeto,
                tarefa=tarefa,
                lida=random.choice([True, False]),
                lida_em=timezone.now() if random.choice([True, False]) else None,
                url=f'/projetos/{projeto.id}/' if random.choice([True, False]) else None
            )

def create_notification_settings():
    """Criar configurações de notificação para usuários"""
    users = User.objects.all()
    canal_choices = ['EMAIL', 'SISTEMA', 'AMBOS', 'NENHUM']
    
    for user in users:
        ConfiguracaoNotificacao.objects.get_or_create(
            usuario=user,
            defaults={
                'tarefa_atribuida': random.choice(canal_choices),
                'tarefa_comentario': random.choice(canal_choices),
                'tarefa_prazo': random.choice(canal_choices),
                'projeto_status': random.choice(canal_choices),
                'equipe_alteracao': random.choice(canal_choices),
                'documento_novo': random.choice(canal_choices),
                'risco_novo': random.choice(canal_choices),
                'mensagem_chat': random.choice(canal_choices),
            }
        )

def create_chat_messages():
    """Criar mensagens de chat para projetos"""
    projects = Projeto.objects.all()
    users = User.objects.all()
    
    for project in projects:
        # Criar entre 5 e 15 mensagens de chat por projeto
        for _ in range(random.randint(5, 15)):
            autor = random.choice(users)
            mensagem = ChatMensagem.objects.create(
                projeto=project,
                autor=autor,
                texto=f'Mensagem de teste enviada por {autor.username}: ' + \
                      ''.join(random.choice(string.ascii_letters + ' ') for _ in range(random.randint(20, 100))),
                enviado_em=timezone.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23)),
                editado=random.choice([True, False])
            )
            
            # Marcar algumas mensagens como lidas por alguns usuários
            for user in random.sample(list(users), random.randint(0, len(users))):
                if user != autor:  # Não criar leitura para o próprio autor
                    ChatMensagemLeitura.objects.create(
                        mensagem=mensagem,
                        usuario=user,
                        lido_em=mensagem.enviado_em + timedelta(minutes=random.randint(1, 60))
                    )

def create_task_comments():
    """Criar comentários para tarefas"""
    tasks = Tarefa.objects.all()
    users = User.objects.all()
    
    for task in tasks:
        # Criar entre 0 e 5 comentários por tarefa
        for _ in range(random.randint(0, 5)):
            autor = random.choice(users)
            ComentarioTarefa.objects.create(
                tarefa=task,
                autor=autor,
                texto=f'Comentário de {autor.username}: ' + \
                      ''.join(random.choice(string.ascii_letters + ' ,.!?') for _ in range(random.randint(20, 150))),
                criado_em=timezone.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            )

def create_task_history():
    """Criar histórico de alterações para tarefas"""
    tasks = Tarefa.objects.all()
    users = User.objects.all()
    
    for task in tasks:
        # Criar entre 2 e 6 registros de histórico por tarefa
        for i in range(random.randint(2, 6)):
            usuario = random.choice(users)
            
            # O HistoricoStatusTarefa só armazena mudanças de status
            status_anterior = random.choice(['A_FAZER', 'EM_ANDAMENTO', 'FEITO'])
            novo_status = random.choice(['A_FAZER', 'EM_ANDAMENTO', 'FEITO'])
            while status_anterior == novo_status:  # Garantir que o status mudou
                novo_status = random.choice(['A_FAZER', 'EM_ANDAMENTO', 'FEITO'])
            
            HistoricoStatusTarefa.objects.create(
                tarefa=task,
                status_anterior=status_anterior,
                novo_status=novo_status,
                alterado_por=usuario,
                alterado_em=timezone.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            )

# Esta função foi removida pois o modelo CategoriaRisco não existe no projeto

def create_risk_history():
    """Criar histórico de alterações para riscos"""
    risks = Risco.objects.all()
    users = User.objects.all()
    
    for risk in risks:
        # Criar entre 2 e 5 registros de histórico por risco
        for i in range(random.randint(2, 5)):
            # Gerar valores aleatórios para status, probabilidade e impacto
            status_anterior = random.choice(['IDENTIFICADO', 'EM_ANALISE', 'MITIGADO', 'ACEITO', 'ELIMINADO'])
            novo_status = random.choice(['IDENTIFICADO', 'EM_ANALISE', 'MITIGADO', 'ACEITO', 'ELIMINADO'])
            while novo_status == status_anterior:  # Garantir que o status mudou
                novo_status = random.choice(['IDENTIFICADO', 'EM_ANALISE', 'MITIGADO', 'ACEITO', 'ELIMINADO'])
            
            probabilidade_anterior = random.choice(['BAIXA', 'MEDIA', 'ALTA'])
            nova_probabilidade = random.choice(['BAIXA', 'MEDIA', 'ALTA'])
            
            impacto_anterior = random.choice(['BAIXO', 'MEDIO', 'ALTO'])
            novo_impacto = random.choice(['BAIXO', 'MEDIO', 'ALTO'])
            
            # Criar o registro de histórico
            HistoricoRisco.objects.create(
                risco=risk,
                status_anterior=status_anterior,
                novo_status=novo_status,
                probabilidade_anterior=probabilidade_anterior,
                nova_probabilidade=nova_probabilidade,
                impacto_anterior=impacto_anterior,
                novo_impacto=novo_impacto,
                alterado_por=random.choice(users),
                observacao=f'Atualização de risco em {timezone.now().strftime("%d/%m/%Y")}.'
            )

def create_document_versions():
    """Atualizar versões de documentos existentes"""
    documents = Documento.objects.all()
    users = User.objects.all()
    
    for doc in documents:
        # Atualizar a versão de alguns documentos
        if random.choice([True, False]):
            version_num = f'1.{random.randint(1, 5)}'  # Versões incrementais: 1.1, 1.2, etc.
            usuario = random.choice(users)
            
            # Atualizar a versão do documento existente
            doc.versao = version_num
            doc.enviado_por = usuario
            doc.atualizado_em = timezone.now() - timedelta(days=random.randint(0, 30))
            doc.save()
            
            # Criar um registro no histórico para esta atualização
            HistoricoDocumento.objects.create(
                documento=doc,
                versao_anterior='1.0',
                arquivo_anterior=doc.arquivo if hasattr(doc, 'arquivo') and doc.arquivo else None,
                tamanho_arquivo=doc.tamanho_arquivo,
                alterado_por=usuario,
                data_alteracao=doc.atualizado_em,
                observacao=f'Atualização para versão {version_num}'
            )

def create_document_history():
    """Criar histórico de alterações para documentos"""
    documents = Documento.objects.all()
    users = User.objects.all()
    
    for doc in documents:
        # Criar entre 1 e 3 registros de histórico por documento
        for i in range(random.randint(1, 3)):
            # Selecionar um usuário aleatório como o responsável pela alteração
            usuario = random.choice(users)
            
            # Gerar uma versão anterior aleatória
            versao_anterior = f"1.{random.randint(0, 5)}"
            
            # Criar o registro de histórico
            try:
                HistoricoDocumento.objects.create(
                    documento=doc,
                    versao_anterior=versao_anterior,
                    arquivo_anterior=None,  # Não temos um arquivo real para usar aqui
                    tamanho_arquivo=random.randint(1024, 10240),  # 1KB a 10KB
                    alterado_por=usuario,
                    observacao=f"Atualização da versão {versao_anterior} para {doc.versao}"
                )
                print(f"Histórico criado para documento: {doc.titulo}")
            except Exception as e:
                print(f"Erro ao criar histórico para documento {doc.titulo}: {str(e)}")
                traceback.print_exc()

def create_document_comments():
    """Criar comentários para documentos"""
    documents = Documento.objects.all()
    users = User.objects.all()
    
    for doc in documents:
        # Criar entre 0 e 4 comentários por documento
        for _ in range(random.randint(0, 4)):
            autor = random.choice(users)
            Comentario.objects.create(
                documento=doc,
                autor=autor,
                texto=f'Comentário de {autor.username} sobre o documento: ' + \
                      ''.join(random.choice(string.ascii_letters + ' ,.!?') for _ in range(random.randint(20, 150))),
                criado_em=timezone.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            )

import traceback

def run_seeds():
    print("Iniciando seed do banco de dados...")
    
    try:
        print("Criando usuários...")
        create_users()
        print("Usuários criados com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar usuários: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando equipes...")
        create_teams()
        print("Equipes criadas com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar equipes: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando projetos...")
        create_projects()
        print("Projetos criados com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar projetos: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando tarefas...")
        create_tasks()
        print("Tarefas criadas com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar tarefas: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando comentários de tarefas...")
        create_task_comments()
        print("Comentários de tarefas criados com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar comentários de tarefas: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando histórico de tarefas...")
        create_task_history()
        print("Histórico de tarefas criado com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar histórico de tarefas: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando riscos...")
        create_risks()
        print("Riscos criados com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar riscos: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando histórico de riscos...")
        create_risk_history()
        print("Histórico de riscos criado com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar histórico de riscos: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando custos...")
        create_costs()
        print("Custos criados com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar custos: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando documentos...")
        create_documents()
        print("Documentos criados com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar documentos: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando versões de documentos...")
        create_document_versions()
        print("Versões de documentos criadas com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar versões de documentos: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando histórico de documentos...")
        create_document_history()
        print("Histórico de documentos criado com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar histórico de documentos: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando comunicações...")
        create_communications()
        print("Comunicações criadas com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar comunicações: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando configurações de notificação...")
        create_notification_settings()
        print("Configurações de notificação criadas com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar configurações de notificação: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando mensagens de chat...")
        create_chat_messages()
        print("Mensagens de chat criadas com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar mensagens de chat: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    try:
        print("Criando comentários de documentos...")
        create_document_comments()
        print("Comentários de documentos criados com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar comentários de documentos: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("\n")
    
    print("\nSeed concluído com sucesso! Alguns erros podem ter ocorrido, mas o processo continuou.\n")

if __name__ == '__main__':
    run_seeds()
