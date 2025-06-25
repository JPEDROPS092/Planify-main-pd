"""
Migração de dados para mover de ForeignKey diretas para GenericForeignKey.

Esta migração move os dados das colunas projeto_id e tarefa_id para
os novos campos content_type_id e object_id do GenericForeignKey.
"""

from django.db import migrations


def migrate_notifications_to_generic_fk(apps, schema_editor):
    """
    Migra dados existentes de ForeignKey para GenericForeignKey.
    """
    # Usar SQL direto para evitar problemas com modelos históricos
    db_alias = schema_editor.connection.alias
    
    # Obter IDs dos ContentTypes diretamente do banco
    with schema_editor.connection.cursor() as cursor:
        # Buscar ContentType para projeto
        cursor.execute("""
            SELECT id FROM django_content_type 
            WHERE app_label = 'projects' AND model = 'projeto'
        """)
        projeto_ct_result = cursor.fetchone()
        
        # Buscar ContentType para tarefa
        cursor.execute("""
            SELECT id FROM django_content_type 
            WHERE app_label = 'tasks' AND model = 'tarefa'
        """)
        tarefa_ct_result = cursor.fetchone()
        
        if projeto_ct_result:
            projeto_ct_id = projeto_ct_result[0]
            # Migrar notificações com projeto
            cursor.execute("""
                UPDATE communications_notificacao 
                SET content_type_id = %s, object_id = projeto_id 
                WHERE projeto_id IS NOT NULL
            """, [projeto_ct_id])
        
        if tarefa_ct_result:
            tarefa_ct_id = tarefa_ct_result[0]
            # Migrar notificações com tarefa
            cursor.execute("""
                UPDATE communications_notificacao 
                SET content_type_id = %s, object_id = tarefa_id 
                WHERE tarefa_id IS NOT NULL
            """, [tarefa_ct_id])


def reverse_migrate_notifications_from_generic_fk(apps, schema_editor):
    """
    Reverte a migração movendo dados do GenericForeignKey de volta para ForeignKey.
    """
    # Usar SQL direto para reverter
    with schema_editor.connection.cursor() as cursor:
        # Buscar ContentType para projeto
        cursor.execute("""
            SELECT id FROM django_content_type 
            WHERE app_label = 'projects' AND model = 'projeto'
        """)
        projeto_ct_result = cursor.fetchone()
        
        # Buscar ContentType para tarefa
        cursor.execute("""
            SELECT id FROM django_content_type 
            WHERE app_label = 'tasks' AND model = 'tarefa'
        """)
        tarefa_ct_result = cursor.fetchone()
        
        if projeto_ct_result:
            projeto_ct_id = projeto_ct_result[0]
            # Reverter notificações de projeto
            cursor.execute("""
                UPDATE communications_notificacao 
                SET projeto_id = object_id 
                WHERE content_type_id = %s
            """, [projeto_ct_id])
        
        if tarefa_ct_result:
            tarefa_ct_id = tarefa_ct_result[0]
            # Reverter notificações de tarefa
            cursor.execute("""
                UPDATE communications_notificacao 
                SET tarefa_id = object_id 
                WHERE content_type_id = %s
            """, [tarefa_ct_id])


class Migration(migrations.Migration):
    """
    Migração de dados para GenericForeignKey.
    """
    
    dependencies = [
        ('communications', '0004_add_generic_foreign_key'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(
            migrate_notifications_to_generic_fk,
            reverse_migrate_notifications_from_generic_fk,
            hints={'target_db': 'default'}
        ),
    ]
