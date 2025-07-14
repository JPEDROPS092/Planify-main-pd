#!/usr/bin/env python3
import os
import sys
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils import timezone

# Configurar ambiente Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planify.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import UserProfile
from projects.models import Projeto, Sprint, MembroProjeto
from tasks.models import Tarefa, AtribuicaoTarefa, ComentarioTarefa
from teams.models import Equipe, MembroEquipe
from risks.models import Risco
from costs.models import Categoria, Custo, OrcamentoProjeto, OrcamentoTarefa, Alerta
from documents.models import Documento, Comentario
from communications.models import Comunicacao, Notificacao, ChatMensagem

User = get_user_model()

def create_comprehensive_cost_data():
    """Criar dados abrangentes de custos"""
    print("Criando dados abrangentes de custos...")
    
    # Obter usuário admin
    admin_user = User.objects.get(email='admin@planify.com')
    
    # Criar categorias de custo mais detalhadas
    categorias_data = [
        {'nome': 'Desenvolvimento', 'descricao': 'Custos relacionados ao desenvolvimento de software'},
        {'nome': 'Infraestrutura', 'descricao': 'Custos de servidores, cloud e infraestrutura'},
        {'nome': 'Licenças', 'descricao': 'Licenças de software e ferramentas'},
        {'nome': 'Recursos Humanos', 'descricao': 'Salários e benefícios da equipe'},
        {'nome': 'Marketing', 'descricao': 'Custos de marketing e publicidade'},
        {'nome': 'Consultoria', 'descricao': 'Serviços de consultoria externa'},
        {'nome': 'Treinamento', 'descricao': 'Cursos e treinamentos para a equipe'},
        {'nome': 'Equipamentos', 'descricao': 'Hardware e equipamentos'},
        {'nome': 'Viagens', 'descricao': 'Despesas de viagem e hospedagem'},
        {'nome': 'Outros', 'descricao': 'Outros custos diversos'},
    ]
    
    categorias = []
    for cat_data in categorias_data:
        categoria, created = Categoria.objects.get_or_create(
            nome=cat_data['nome'],
            defaults={'descricao': cat_data['descricao']}
        )
        categorias.append(categoria)
        if created:
            print(f"Categoria criada: {categoria.nome}")
    
    # Obter projetos existentes
    projetos = list(Projeto.objects.all())
    
    # Criar orçamentos para projetos
    for projeto in projetos:
        orcamento, created = OrcamentoProjeto.objects.get_or_create(
            projeto=projeto,
            defaults={
                'valor_total': Decimal(random.randint(50000, 500000)),
                'valor_utilizado': Decimal(0),
                'data_inicio': timezone.now().date() - timedelta(days=random.randint(30, 180)),
                'data_fim': timezone.now().date() + timedelta(days=random.randint(30, 365)),
            }
        )
        if created:
            print(f"Orçamento criado para projeto: {projeto.titulo}")
    
    # Criar custos variados para os últimos 12 meses
    start_date = timezone.now().date() - timedelta(days=365)
    
    custos_exemplos = [
        # Desenvolvimento
        {'descricao': 'Desenvolvimento Frontend React', 'valor_min': 5000, 'valor_max': 15000, 'categoria': 'Desenvolvimento'},
        {'descricao': 'Desenvolvimento Backend Django', 'valor_min': 8000, 'valor_max': 20000, 'categoria': 'Desenvolvimento'},
        {'descricao': 'Desenvolvimento Mobile Flutter', 'valor_min': 6000, 'valor_max': 18000, 'categoria': 'Desenvolvimento'},
        {'descricao': 'Integração de APIs', 'valor_min': 2000, 'valor_max': 8000, 'categoria': 'Desenvolvimento'},
        
        # Infraestrutura
        {'descricao': 'AWS EC2 Instances', 'valor_min': 500, 'valor_max': 3000, 'categoria': 'Infraestrutura'},
        {'descricao': 'AWS RDS Database', 'valor_min': 300, 'valor_max': 1500, 'categoria': 'Infraestrutura'},
        {'descricao': 'CDN CloudFlare', 'valor_min': 100, 'valor_max': 500, 'categoria': 'Infraestrutura'},
        {'descricao': 'Backup e Storage', 'valor_min': 200, 'valor_max': 800, 'categoria': 'Infraestrutura'},
        
        # Licenças
        {'descricao': 'Licença JetBrains', 'valor_min': 200, 'valor_max': 600, 'categoria': 'Licenças'},
        {'descricao': 'Licença Adobe Creative Suite', 'valor_min': 300, 'valor_max': 800, 'categoria': 'Licenças'},
        {'descricao': 'Licença Microsoft Office', 'valor_min': 150, 'valor_max': 400, 'categoria': 'Licenças'},
        {'descricao': 'Licença Figma Pro', 'valor_min': 100, 'valor_max': 300, 'categoria': 'Licenças'},
        
        # Recursos Humanos
        {'descricao': 'Salário Desenvolvedor Senior', 'valor_min': 8000, 'valor_max': 15000, 'categoria': 'Recursos Humanos'},
        {'descricao': 'Salário Desenvolvedor Pleno', 'valor_min': 5000, 'valor_max': 10000, 'categoria': 'Recursos Humanos'},
        {'descricao': 'Salário Designer UX/UI', 'valor_min': 4000, 'valor_max': 8000, 'categoria': 'Recursos Humanos'},
        {'descricao': 'Benefícios e Encargos', 'valor_min': 2000, 'valor_max': 5000, 'categoria': 'Recursos Humanos'},
        
        # Consultoria
        {'descricao': 'Consultoria em Arquitetura', 'valor_min': 3000, 'valor_max': 10000, 'categoria': 'Consultoria'},
        {'descricao': 'Auditoria de Segurança', 'valor_min': 2000, 'valor_max': 8000, 'categoria': 'Consultoria'},
        {'descricao': 'Consultoria DevOps', 'valor_min': 2500, 'valor_max': 7000, 'categoria': 'Consultoria'},
        
        # Equipamentos
        {'descricao': 'MacBook Pro para Desenvolvedor', 'valor_min': 8000, 'valor_max': 15000, 'categoria': 'Equipamentos'},
        {'descricao': 'Monitor 4K', 'valor_min': 1500, 'valor_max': 3000, 'categoria': 'Equipamentos'},
        {'descricao': 'Cadeira Ergonômica', 'valor_min': 800, 'valor_max': 2000, 'categoria': 'Equipamentos'},
        
        # Treinamento
        {'descricao': 'Curso AWS Certification', 'valor_min': 500, 'valor_max': 1500, 'categoria': 'Treinamento'},
        {'descricao': 'Conferência Tech', 'valor_min': 1000, 'valor_max': 3000, 'categoria': 'Treinamento'},
        {'descricao': 'Workshop Agile', 'valor_min': 800, 'valor_max': 2000, 'categoria': 'Treinamento'},
    ]
    
    # Criar custos para os últimos 12 meses
    for mes in range(12):
        data_custo = start_date + timedelta(days=mes * 30)
        
        # Criar 5-15 custos por mês
        num_custos = random.randint(5, 15)
        
        for _ in range(num_custos):
            custo_exemplo = random.choice(custos_exemplos)
            categoria = next((cat for cat in categorias if cat.nome == custo_exemplo['categoria']), categorias[0])
            projeto = random.choice(projetos)
            
            # Adicionar variação no nome para tornar único
            variacao = random.choice(['', ' - Fase 1', ' - Fase 2', ' - Sprint', ' - Manutenção', ' - Upgrade'])
            descricao = custo_exemplo['descricao'] + variacao
            
            valor = Decimal(random.randint(custo_exemplo['valor_min'], custo_exemplo['valor_max']))
            
            custo = Custo.objects.create(
                descricao=descricao,
                valor=valor,
                data=data_custo + timedelta(days=random.randint(0, 29)),
                tipo=random.choice(['FIXO', 'VARIAVEL']),
                projeto=projeto,
                categoria=categoria,
                criado_por=admin_user
            )
            
            # Atualizar orçamento do projeto
            try:
                orcamento = OrcamentoProjeto.objects.get(projeto=projeto)
                orcamento.valor_utilizado += valor
                orcamento.save()
            except OrcamentoProjeto.DoesNotExist:
                pass
    
    print(f"Criados {Custo.objects.count()} custos no total")

def create_comprehensive_project_data():
    """Criar dados abrangentes de projetos"""
    print("Criando dados abrangentes de projetos...")
    
    admin_user = User.objects.get(email='admin@planify.com')
    
    # Criar projetos mais detalhados se não existirem
    projetos_data = [
        {
            'titulo': 'E-commerce Platform Modernization',
            'descricao': 'Modernização completa da plataforma de e-commerce com microserviços',
            'status': 'EM_ANDAMENTO',
            'prioridade': 'ALTA',
            'orcamento': 250000
        },
        {
            'titulo': 'Mobile App Development',
            'descricao': 'Desenvolvimento de aplicativo móvel nativo para iOS e Android',
            'status': 'EM_ANDAMENTO',
            'prioridade': 'ALTA',
            'orcamento': 180000
        },
        {
            'titulo': 'Data Analytics Dashboard',
            'descricao': 'Dashboard de analytics em tempo real com visualizações interativas',
            'status': 'PLANEJADO',
            'prioridade': 'MEDIA',
            'orcamento': 120000
        },
        {
            'titulo': 'AI Chatbot Integration',
            'descricao': 'Integração de chatbot com IA para atendimento ao cliente',
            'status': 'EM_ANDAMENTO',
            'prioridade': 'MEDIA',
            'orcamento': 95000
        },
        {
            'titulo': 'Security Audit & Compliance',
            'descricao': 'Auditoria de segurança e implementação de compliance LGPD',
            'status': 'CONCLUIDO',
            'prioridade': 'ALTA',
            'orcamento': 75000
        }
    ]
    
    for projeto_data in projetos_data:
        projeto, created = Projeto.objects.get_or_create(
            titulo=projeto_data['titulo'],
            defaults={
                'descricao': projeto_data['descricao'],
                'status': projeto_data['status'],
                'prioridade': projeto_data['prioridade'],
                'data_inicio': timezone.now().date() - timedelta(days=random.randint(30, 180)),
                'data_fim': timezone.now().date() + timedelta(days=random.randint(60, 365)),
                'criado_por': admin_user
            }
        )
        if created:
            print(f"Projeto criado: {projeto.titulo}")

def create_comprehensive_task_data():
    """Criar dados abrangentes de tarefas"""
    print("Criando dados abrangentes de tarefas...")
    
    admin_user = User.objects.get(email='admin@planify.com')
    projetos = list(Projeto.objects.all())
    
    tipos_tarefa = [
        'Análise de Requisitos', 'Design de Interface', 'Desenvolvimento Frontend',
        'Desenvolvimento Backend', 'Testes Unitários', 'Testes de Integração',
        'Deploy', 'Documentação', 'Revisão de Código', 'Configuração de Ambiente',
        'Otimização de Performance', 'Correção de Bugs', 'Migração de Dados',
        'Integração de APIs', 'Implementação de Segurança'
    ]
    
    for projeto in projetos:
        # Criar 8-15 tarefas por projeto
        num_tarefas = random.randint(8, 15)
        
        for i in range(num_tarefas):
            tipo = random.choice(tipos_tarefa)
            
            tarefa = Tarefa.objects.create(
                titulo=f"{tipo} - {projeto.titulo}",
                descricao=f"Implementar {tipo.lower()} para o projeto {projeto.titulo}",
                projeto=projeto,
                status=random.choice(['A_FAZER', 'EM_ANDAMENTO', 'FEITO']),
                prioridade=random.choice(['BAIXA', 'MEDIA', 'ALTA']),
                data_inicio=timezone.now().date() - timedelta(days=random.randint(0, 60)),
                data_termino=timezone.now().date() + timedelta(days=random.randint(1, 30)),
                criado_por=admin_user
            )
            
            # Atribuir tarefa ao admin
            AtribuicaoTarefa.objects.create(
                tarefa=tarefa,
                usuario=admin_user,
                atribuido_por=admin_user
            )

def create_comprehensive_risk_data():
    """Criar dados abrangentes de riscos"""
    print("Criando dados abrangentes de riscos...")
    
    admin_user = User.objects.get(email='admin@planify.com')
    projetos = list(Projeto.objects.all())
    
    riscos_exemplos = [
        {
            'titulo': 'Atraso na Entrega de APIs Externas',
            'descricao': 'Dependência de APIs de terceiros pode causar atrasos no cronograma',
            'probabilidade': 'MEDIA',
            'impacto': 'ALTO'
        },
        {
            'titulo': 'Mudança de Requisitos pelo Cliente',
            'descricao': 'Cliente pode solicitar mudanças significativas nos requisitos',
            'probabilidade': 'ALTA',
            'impacto': 'MEDIO'
        },
        {
            'titulo': 'Problemas de Performance em Produção',
            'descricao': 'Sistema pode apresentar lentidão com alto volume de usuários',
            'probabilidade': 'MEDIA',
            'impacto': 'ALTO'
        },
        {
            'titulo': 'Saída de Desenvolvedor Chave',
            'descricao': 'Perda de conhecimento crítico com saída de membro da equipe',
            'probabilidade': 'BAIXA',
            'impacto': 'ALTO'
        },
        {
            'titulo': 'Problemas de Integração',
            'descricao': 'Dificuldades na integração entre diferentes sistemas',
            'probabilidade': 'MEDIA',
            'impacto': 'MEDIO'
        }
    ]
    
    for projeto in projetos:
        # Criar 2-4 riscos por projeto
        num_riscos = random.randint(2, 4)
        
        for i in range(num_riscos):
            risco_exemplo = random.choice(riscos_exemplos)
            
            Risco.objects.create(
                titulo=f"{risco_exemplo['titulo']} - {projeto.titulo}",
                descricao=risco_exemplo['descricao'],
                projeto=projeto,
                probabilidade=risco_exemplo['probabilidade'],
                impacto=risco_exemplo['impacto'],
                status=random.choice(['IDENTIFICADO', 'EM_MONITORAMENTO', 'MITIGADO', 'OCORRIDO']),
                data_identificacao=timezone.now().date() - timedelta(days=random.randint(0, 90)),
                responsavel=admin_user,
                criado_por=admin_user
            )

def create_comprehensive_document_data():
    """Criar dados abrangentes de documentos"""
    print("Criando dados abrangentes de documentos...")
    
    admin_user = User.objects.get(email='admin@planify.com')
    projetos = list(Projeto.objects.all())
    
    tipos_documento = [
        'Especificação de Requisitos', 'Documento de Arquitetura', 'Manual do Usuário',
        'Plano de Testes', 'Documentação de API', 'Guia de Deploy',
        'Relatório de Progresso', 'Ata de Reunião', 'Análise de Riscos',
        'Plano de Projeto', 'Documentação Técnica'
    ]
    
    for projeto in projetos:
        # Criar 3-6 documentos por projeto
        num_docs = random.randint(3, 6)
        
        for i in range(num_docs):
            tipo = random.choice(tipos_documento)
            
            Documento.objects.create(
                titulo=f"{tipo} - {projeto.titulo}",
                descricao=f"{tipo} detalhado para o projeto {projeto.titulo}",
                projeto=projeto,
                tipo=random.choice(['ESPECIFICACAO', 'MANUAL', 'RELATORIO', 'OUTROS']),
                versao='1.0',
                status=random.choice(['RASCUNHO', 'EM_REVISAO', 'APROVADO', 'ARQUIVADO']),
                criado_por=admin_user
            )

def run_comprehensive_population():
    """Executar população completa de todos os módulos"""
    print("=== INICIANDO POPULAÇÃO COMPLETA DE TODOS OS MÓDULOS ===")
    
    try:
        create_comprehensive_project_data()
        create_comprehensive_task_data()
        create_comprehensive_cost_data()
        create_comprehensive_risk_data()
        create_comprehensive_document_data()
        
        print("\n=== RESUMO DOS DADOS CRIADOS ===")
        print(f"Projetos: {Projeto.objects.count()}")
        print(f"Tarefas: {Tarefa.objects.count()}")
        print(f"Custos: {Custo.objects.count()}")
        print(f"Categorias de Custo: {Categoria.objects.count()}")
        print(f"Orçamentos de Projeto: {OrcamentoProjeto.objects.count()}")
        print(f"Riscos: {Risco.objects.count()}")
        print(f"Documentos: {Documento.objects.count()}")
        
        print("\n=== POPULAÇÃO COMPLETA FINALIZADA COM SUCESSO! ===")
        
    except Exception as e:
        print(f"Erro durante a população: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_comprehensive_population()
