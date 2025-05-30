# Generated by Django 4.2.10 on 2025-04-27 17:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("communications", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comunicacao",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("titulo", models.CharField(max_length=200)),
                ("texto", models.TextField()),
                ("criada_em", models.DateTimeField(auto_now_add=True)),
                ("atualizada_em", models.DateTimeField(auto_now=True)),
                (
                    "destinatarios",
                    models.ManyToManyField(
                        related_name="comunicacoes_recebidas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "projeto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comunicacoes",
                        to="projects.projeto",
                    ),
                ),
                (
                    "remetente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comunicacoes_enviadas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Comunicação",
                "verbose_name_plural": "Comunicações",
                "ordering": ["-criada_em"],
            },
        ),
        migrations.DeleteModel(
            name="Communication",
        ),
    ]
