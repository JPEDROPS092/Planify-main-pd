from django.core.management.base import BaseCommand
from users.models import AccessProfile, Permission, User

class Command(BaseCommand):
    help = 'Cria perfis de acesso padrão para cada papel de usuário'

    def handle(self, *args, **kwargs):
        self.stdout.write('Criando perfis de acesso padrão...')
        
        # Criar perfil de Administrador
        admin_profile, created = AccessProfile.objects.get_or_create(
            name='Administrador',
            defaults={'description': 'Acesso completo a todas as funcionalidades do sistema'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Perfil de acesso "{admin_profile.name}" criado com sucesso'))
        else:
            self.stdout.write(f'Perfil de acesso "{admin_profile.name}" já existe')
            # Limpar permissões existentes para recriar
            Permission.objects.filter(access_profile=admin_profile).delete()
        
        # Adicionar todas as permissões possíveis para o Administrador
        modules = [choice[0] for choice in Permission.MODULE_CHOICES]
        actions = [choice[0] for choice in Permission.ACTION_CHOICES]
        
        for module in modules:
            for action in actions:
                Permission.objects.create(
                    access_profile=admin_profile,
                    module=module,
                    action=action
                )
        
        self.stdout.write(self.style.SUCCESS(f'Permissões para "{admin_profile.name}" configuradas'))
        
        # Criar perfil de Gerente de Projetos
        pm_profile, created = AccessProfile.objects.get_or_create(
            name='Gerente de Projetos',
            defaults={'description': 'Gerenciamento de projetos, tarefas e equipes'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Perfil de acesso "{pm_profile.name}" criado com sucesso'))
        else:
            self.stdout.write(f'Perfil de acesso "{pm_profile.name}" já existe')
            # Limpar permissões existentes para recriar
            Permission.objects.filter(access_profile=pm_profile).delete()
        
        # Permissões para Gerente de Projetos
        pm_permissions = [
            # Projetos - acesso total
            {'module': 'PROJECTS', 'action': 'VIEW'},
            {'module': 'PROJECTS', 'action': 'CREATE'},
            {'module': 'PROJECTS', 'action': 'EDIT'},
            {'module': 'PROJECTS', 'action': 'DELETE'},
            
            # Tarefas - acesso total
            {'module': 'TASKS', 'action': 'VIEW'},
            {'module': 'TASKS', 'action': 'CREATE'},
            {'module': 'TASKS', 'action': 'EDIT'},
            {'module': 'TASKS', 'action': 'DELETE'},
            {'module': 'TASKS', 'action': 'ASSIGN'},
            
            # Equipes - acesso total
            {'module': 'TEAMS', 'action': 'VIEW'},
            {'module': 'TEAMS', 'action': 'CREATE'},
            {'module': 'TEAMS', 'action': 'EDIT'},
            {'module': 'TEAMS', 'action': 'DELETE'},
            
            # Riscos - acesso total
            {'module': 'RISKS', 'action': 'VIEW'},
            {'module': 'RISKS', 'action': 'CREATE'},
            {'module': 'RISKS', 'action': 'EDIT'},
            {'module': 'RISKS', 'action': 'DELETE'},
            
            # Custos - acesso total
            {'module': 'COSTS', 'action': 'VIEW'},
            {'module': 'COSTS', 'action': 'CREATE'},
            {'module': 'COSTS', 'action': 'EDIT'},
            {'module': 'COSTS', 'action': 'DELETE'},
            
            # Documentos - acesso total
            {'module': 'DOCUMENTS', 'action': 'VIEW'},
            {'module': 'DOCUMENTS', 'action': 'CREATE'},
            {'module': 'DOCUMENTS', 'action': 'EDIT'},
            {'module': 'DOCUMENTS', 'action': 'DELETE'},
            {'module': 'DOCUMENTS', 'action': 'APPROVE'},
            
            # Comunicações - acesso total
            {'module': 'COMMUNICATIONS', 'action': 'VIEW'},
            {'module': 'COMMUNICATIONS', 'action': 'CREATE'},
            {'module': 'COMMUNICATIONS', 'action': 'EDIT'},
            {'module': 'COMMUNICATIONS', 'action': 'DELETE'},
            
            # Relatórios - visualização e exportação
            {'module': 'REPORTS', 'action': 'VIEW'},
            {'module': 'REPORTS', 'action': 'EXPORT'},
            
            # Usuários - visualização
            {'module': 'USERS', 'action': 'VIEW'},
            
            # Dashboard
            {'module': 'DASHBOARD', 'action': 'VIEW'},
            
            # Notificações
            {'module': 'NOTIFICATIONS', 'action': 'VIEW'},
            {'module': 'NOTIFICATIONS', 'action': 'EDIT'},
            
            # Aprovações
            {'module': 'APPROVALS', 'action': 'VIEW'},
            {'module': 'APPROVALS', 'action': 'APPROVE'},
            {'module': 'APPROVALS', 'action': 'EDIT'},
        ]
        
        for perm in pm_permissions:
            Permission.objects.create(
                access_profile=pm_profile,
                module=perm['module'],
                action=perm['action']
            )
        
        self.stdout.write(self.style.SUCCESS(f'Permissões para "{pm_profile.name}" configuradas'))
        
        # Criar perfil de Líder de Equipe
        tl_profile, created = AccessProfile.objects.get_or_create(
            name='Líder de Equipe',
            defaults={'description': 'Gerenciamento de tarefas e membros da equipe'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Perfil de acesso "{tl_profile.name}" criado com sucesso'))
        else:
            self.stdout.write(f'Perfil de acesso "{tl_profile.name}" já existe')
            # Limpar permissões existentes para recriar
            Permission.objects.filter(access_profile=tl_profile).delete()
        
        # Permissões para Líder de Equipe
        tl_permissions = [
            # Projetos - apenas visualização
            {'module': 'PROJECTS', 'action': 'VIEW'},
            
            # Tarefas - acesso total
            {'module': 'TASKS', 'action': 'VIEW'},
            {'module': 'TASKS', 'action': 'CREATE'},
            {'module': 'TASKS', 'action': 'EDIT'},
            {'module': 'TASKS', 'action': 'ASSIGN'},
            
            # Equipes - visualização e edição
            {'module': 'TEAMS', 'action': 'VIEW'},
            {'module': 'TEAMS', 'action': 'EDIT'},
            
            # Riscos - acesso parcial
            {'module': 'RISKS', 'action': 'VIEW'},
            {'module': 'RISKS', 'action': 'CREATE'},
            {'module': 'RISKS', 'action': 'EDIT'},
            
            # Documentos - visualização e edição
            {'module': 'DOCUMENTS', 'action': 'VIEW'},
            {'module': 'DOCUMENTS', 'action': 'CREATE'},
            {'module': 'DOCUMENTS', 'action': 'EDIT'},
            
            # Comunicações - acesso total
            {'module': 'COMMUNICATIONS', 'action': 'VIEW'},
            {'module': 'COMMUNICATIONS', 'action': 'CREATE'},
            {'module': 'COMMUNICATIONS', 'action': 'EDIT'},
            {'module': 'COMMUNICATIONS', 'action': 'DELETE'},
            
            # Relatórios - visualização
            {'module': 'REPORTS', 'action': 'VIEW'},
            {'module': 'REPORTS', 'action': 'EXPORT'},
            
            # Dashboard
            {'module': 'DASHBOARD', 'action': 'VIEW'},
            
            # Notificações
            {'module': 'NOTIFICATIONS', 'action': 'VIEW'},
            {'module': 'NOTIFICATIONS', 'action': 'EDIT'},
        ]
        
        for perm in tl_permissions:
            Permission.objects.create(
                access_profile=tl_profile,
                module=perm['module'],
                action=perm['action']
            )
        
        self.stdout.write(self.style.SUCCESS(f'Permissões para "{tl_profile.name}" configuradas'))
        
        # Criar perfil de Membro da Equipe
        member_profile, created = AccessProfile.objects.get_or_create(
            name='Membro da Equipe',
            defaults={'description': 'Execução de tarefas e comunicação com a equipe'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Perfil de acesso "{member_profile.name}" criado com sucesso'))
        else:
            self.stdout.write(f'Perfil de acesso "{member_profile.name}" já existe')
            # Limpar permissões existentes para recriar
            Permission.objects.filter(access_profile=member_profile).delete()
        
        # Permissões para Membro da Equipe
        member_permissions = [
            # Projetos - apenas visualização
            {'module': 'PROJECTS', 'action': 'VIEW'},
            
            # Tarefas - visualização e edição das próprias tarefas
            {'module': 'TASKS', 'action': 'VIEW'},
            {'module': 'TASKS', 'action': 'EDIT'},
            
            # Equipes - visualização
            {'module': 'TEAMS', 'action': 'VIEW'},
            
            # Riscos - visualização e criação
            {'module': 'RISKS', 'action': 'VIEW'},
            {'module': 'RISKS', 'action': 'CREATE'},
            
            # Documentos - visualização e criação
            {'module': 'DOCUMENTS', 'action': 'VIEW'},
            {'module': 'DOCUMENTS', 'action': 'CREATE'},
            
            # Comunicações - visualização, criação e edição das próprias
            {'module': 'COMMUNICATIONS', 'action': 'VIEW'},
            {'module': 'COMMUNICATIONS', 'action': 'CREATE'},
            {'module': 'COMMUNICATIONS', 'action': 'EDIT'},
            {'module': 'COMMUNICATIONS', 'action': 'COMMENT'},
            
            # Dashboard
            {'module': 'DASHBOARD', 'action': 'VIEW'},
            
            # Notificações
            {'module': 'NOTIFICATIONS', 'action': 'VIEW'},
        ]
        
        for perm in member_permissions:
            Permission.objects.create(
                access_profile=member_profile,
                module=perm['module'],
                action=perm['action']
            )
        
        self.stdout.write(self.style.SUCCESS(f'Permissões para "{member_profile.name}" configuradas'))
        
        # Criar perfil de Stakeholder/Cliente
        stakeholder_profile, created = AccessProfile.objects.get_or_create(
            name='Stakeholder',
            defaults={'description': 'Visualização de relatórios e aprovação de entregas'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Perfil de acesso "{stakeholder_profile.name}" criado com sucesso'))
        else:
            self.stdout.write(f'Perfil de acesso "{stakeholder_profile.name}" já existe')
            # Limpar permissões existentes para recriar
            Permission.objects.filter(access_profile=stakeholder_profile).delete()
        
        # Permissões para Stakeholder
        stakeholder_permissions = [
            # Projetos - apenas visualização
            {'module': 'PROJECTS', 'action': 'VIEW'},
            
            # Tarefas - apenas visualização
            {'module': 'TASKS', 'action': 'VIEW'},
            
            # Documentos - visualização e aprovação
            {'module': 'DOCUMENTS', 'action': 'VIEW'},
            {'module': 'DOCUMENTS', 'action': 'APPROVE'},
            
            # Comunicações - visualização e criação
            {'module': 'COMMUNICATIONS', 'action': 'VIEW'},
            {'module': 'COMMUNICATIONS', 'action': 'CREATE'},
            {'module': 'COMMUNICATIONS', 'action': 'COMMENT'},
            
            # Relatórios - visualização
            {'module': 'REPORTS', 'action': 'VIEW'},
            {'module': 'REPORTS', 'action': 'EXPORT'},
            
            # Dashboard
            {'module': 'DASHBOARD', 'action': 'VIEW'},
            
            # Notificações
            {'module': 'NOTIFICATIONS', 'action': 'VIEW'},
            
            # Aprovações
            {'module': 'APPROVALS', 'action': 'VIEW'},
            {'module': 'APPROVALS', 'action': 'APPROVE'},
        ]
        
        for perm in stakeholder_permissions:
            Permission.objects.create(
                access_profile=stakeholder_profile,
                module=perm['module'],
                action=perm['action']
            )
        
        self.stdout.write(self.style.SUCCESS(f'Permissões para "{stakeholder_profile.name}" configuradas'))
        
        # Criar perfil de Auditor
        auditor_profile, created = AccessProfile.objects.get_or_create(
            name='Auditor',
            defaults={'description': 'Visualização de logs, históricos e relatórios financeiros'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Perfil de acesso "{auditor_profile.name}" criado com sucesso'))
        else:
            self.stdout.write(f'Perfil de acesso "{auditor_profile.name}" já existe')
            # Limpar permissões existentes para recriar
            Permission.objects.filter(access_profile=auditor_profile).delete()
        
        # Permissões para Auditor
        auditor_permissions = [
            # Projetos - apenas visualização
            {'module': 'PROJECTS', 'action': 'VIEW'},
            
            # Tarefas - apenas visualização
            {'module': 'TASKS', 'action': 'VIEW'},
            
            # Riscos - visualização
            {'module': 'RISKS', 'action': 'VIEW'},
            
            # Custos - visualização
            {'module': 'COSTS', 'action': 'VIEW'},
            {'module': 'COSTS', 'action': 'EXPORT'},
            
            # Documentos - visualização
            {'module': 'DOCUMENTS', 'action': 'VIEW'},
            {'module': 'DOCUMENTS', 'action': 'EXPORT'},
            
            # Relatórios - visualização e exportação
            {'module': 'REPORTS', 'action': 'VIEW'},
            {'module': 'REPORTS', 'action': 'EXPORT'},
            
            # Dashboard
            {'module': 'DASHBOARD', 'action': 'VIEW'},
        ]
        
        for perm in auditor_permissions:
            Permission.objects.create(
                access_profile=auditor_profile,
                module=perm['module'],
                action=perm['action']
            )
        
        self.stdout.write(self.style.SUCCESS(f'Permissões para "{auditor_profile.name}" configuradas'))
        
        self.stdout.write(self.style.SUCCESS('Todos os perfis de acesso foram criados com sucesso!'))
