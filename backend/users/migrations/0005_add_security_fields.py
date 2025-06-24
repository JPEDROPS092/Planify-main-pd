# users/migrations/0005_add_security_fields.py
import uuid
from django.db import migrations, models


def populate_uuid_field(apps, schema_editor):
    """
    Popula o campo UUID com valores únicos para registros existentes
    """
    User = apps.get_model('users', 'User')
    for user in User.objects.all():
        user.uuid = uuid.uuid4()
        user.save()


def reverse_populate_uuid_field(apps, schema_editor):
    """
    Função de reversão - não faz nada
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_blacklistedtokens_options_and_more'),
    ]

    operations = [
        # Primeiro adicionar campos não únicos
        migrations.AddField(
            model_name='user',
            name='force_password_change',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='locked_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        # Popullar UUIDs únicos
        migrations.RunPython(
            populate_uuid_field,
            reverse_populate_uuid_field,
        ),
        # Tornar o campo unique e not null
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
