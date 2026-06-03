#!/usr/bin/env python3
"""Compatibilidade para o seed antigo.

O seed de negocio agora vive no comando Django ``seed_demo_data``. Este wrapper
mantem o fluxo ``python seed_data.py`` usado na documentacao e em scripts locais.
"""
import os
import sys

import django
from django.core.management import call_command


def main():
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planify.settings')
    django.setup()

    tenant_slug = os.environ.get('SEED_TENANT', 'demo')
    call_command('seed_demo_data', tenant_slug=tenant_slug)


if __name__ == '__main__':
    main()
