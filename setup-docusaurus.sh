#!/bin/bash

# Script para configurar e iniciar o Docusaurus para o projeto Planify
# Autor: Equipe Planify
# Data: 2025-05-12

set -e

DOCS_DIR="/home/jpcode092/projects/Planify-main/docs"
echo "🚀 Configurando Docusaurus para o projeto Planify..."

# Verificar se o diretório docs existe
if [ ! -d "$DOCS_DIR" ]; then
    echo "📁 Criando diretório de documentação..."
    mkdir -p "$DOCS_DIR"
fi

# Navegar para o diretório de documentação
cd "$DOCS_DIR"

# Verificar se o Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale o Node.js (versão 16.14.0 ou superior)."
    exit 1
fi

# Verificar se o npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ npm não encontrado. Por favor, instale o npm."
    exit 1
fi

# Verificar se o package.json já existe
if [ ! -f "$DOCS_DIR/package.json" ]; then
    echo "📦 Inicializando package.json..."
    npm init -y
    
    # Atualizar informações básicas do package.json
    npm pkg set name="planify-docs"
    npm pkg set version="0.0.1"
    npm pkg set description="Documentação do Planify - Sistema de Gerenciamento de Projetos de P&D"
    npm pkg set private=true
fi

# Verificar se o Docusaurus já está instalado
if [ ! -d "$DOCS_DIR/node_modules/@docusaurus" ]; then
    echo "📚 Instalando Docusaurus..."
    npm install --save @docusaurus/core@latest @docusaurus/preset-classic@latest @mdx-js/react@^1.6.22 clsx@^1.2.1 prism-react-renderer@^1.3.5 react@^17.0.2 react-dom@^17.0.2
    npm install --save-dev @docusaurus/module-type-aliases@latest
    
    # Adicionar scripts ao package.json
    npm pkg set scripts.docusaurus="docusaurus"
    npm pkg set scripts.start="docusaurus start"
    npm pkg set scripts.build="docusaurus build"
    npm pkg set scripts.swizzle="docusaurus swizzle"
    npm pkg set scripts.deploy="docusaurus deploy"
    npm pkg set scripts.clear="docusaurus clear"
    npm pkg set scripts.serve="docusaurus serve"
    npm pkg set scripts.write-translations="docusaurus write-translations"
    npm pkg set scripts.write-heading-ids="docusaurus write-heading-ids"
fi

# Verificar se a estrutura básica do Docusaurus já existe
if [ ! -f "$DOCS_DIR/docusaurus.config.js" ]; then
    echo "🔧 Configurando estrutura básica do Docusaurus..."
    
    # Criar diretório src se não existir
    if [ ! -d "$DOCS_DIR/src" ]; then
        mkdir -p "$DOCS_DIR/src/css"
        mkdir -p "$DOCS_DIR/src/pages"
        mkdir -p "$DOCS_DIR/static/img"
    fi
    
    # Criar arquivo CSS personalizado
    echo "/**
 * CSS personalizado para o Planify Docs
 */

:root {
  --ifm-color-primary: #1976d2;
  --ifm-color-primary-dark: #1565c0;
  --ifm-color-primary-darker: #0d47a1;
  --ifm-color-primary-darkest: #0a3880;
  --ifm-color-primary-light: #42a5f5;
  --ifm-color-primary-lighter: #64b5f6;
  --ifm-color-primary-lightest: #90caf9;
  --ifm-code-font-size: 95%;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.1);
}

[data-theme='dark'] {
  --ifm-color-primary: #42a5f5;
  --ifm-color-primary-dark: #1e88e5;
  --ifm-color-primary-darker: #1976d2;
  --ifm-color-primary-darkest: #1565c0;
  --ifm-color-primary-light: #64b5f6;
  --ifm-color-primary-lighter: #90caf9;
  --ifm-color-primary-lightest: #bbdefb;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.3);
}
" > "$DOCS_DIR/src/css/custom.css"
fi

# Iniciar o servidor de desenvolvimento
echo "🌐 Iniciando o servidor de desenvolvimento Docusaurus..."
echo "📝 Acesse a documentação em: http://localhost:3000"
echo "🛑 Para parar o servidor, pressione Ctrl+C"
echo ""
npm start -- --port 3000 --host 0.0.0.0
