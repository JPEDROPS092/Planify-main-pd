# Generated manually for SaaS tenant metadata.

from django.db import migrations, models
from django.utils.text import slugify


def populate_client_slugs(apps, schema_editor):
    Client = apps.get_model('customers', 'Client')
    used = set()

    for client in Client.objects.order_by('id'):
        base = slugify(client.name) or 'tenant'
        slug = base[:120]
        suffix = 2

        while slug in used or Client.objects.filter(slug=slug).exclude(pk=client.pk).exists():
            suffix_text = f'-{suffix}'
            slug = f'{base[:120 - len(suffix_text)]}{suffix_text}'
            suffix += 1

        client.slug = slug
        client.save(update_fields=['slug'])
        used.add(slug)


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_native_rls'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='slug',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='status',
            field=models.CharField(
                choices=[('active', 'Ativo'), ('suspended', 'Suspenso')],
                default='active',
                max_length=20,
            ),
        ),
        migrations.RunPython(populate_client_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='client',
            name='slug',
            field=models.SlugField(blank=True, max_length=120, unique=True),
        ),
    ]
