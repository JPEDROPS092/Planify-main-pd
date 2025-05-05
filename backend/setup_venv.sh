#!/bin/bash

# Script para configurar ambiente virtual para o Planify Backend
echo "Configurando ambiente virtual para o Planify Backend..."

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Criar superusuário (opcional)
echo "Deseja criar um superusuário? (s/n)"
read criar_super
if [ "$criar_super" = "s" ]; then
    python manage.py createsuperuser
fi

echo "Ambiente virtual configurado com sucesso!"
echo "Para ativar o ambiente virtual, execute: source venv/bin/activate"
echo "Para iniciar o servidor, execute: python manage.py runserver"
