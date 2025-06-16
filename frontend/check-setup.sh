#!/bin/bash

# =============================================================================
# PLANIFY - SCRIPT DE VERIFICAÇÃO DE CONFIGURAÇÃO
# =============================================================================

echo "🔍 Verificando configurações do Planify..."

# Verificar se o Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Instale o Node.js 18+ para continuar."
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js encontrado: $NODE_VERSION"

# Verificar se o npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ npm não encontrado."
    exit 1
fi

NPM_VERSION=$(npm --version)
echo "✅ npm encontrado: $NPM_VERSION"

# Verificar se as dependências estão instaladas
if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules não encontrado. Executando npm install..."
    npm install
else
    echo "✅ Dependências encontradas"
fi

# Verificar arquivo de configuração
if [ -f "nuxt.config.ts" ]; then
    echo "✅ nuxt.config.ts encontrado"
else
    echo "❌ nuxt.config.ts não encontrado"
    exit 1
fi

# Verificar plugins
PLUGINS_DIR="plugins"
if [ -d "$PLUGINS_DIR" ]; then
    echo "✅ Diretório de plugins encontrado"
    
    if [ -f "$PLUGINS_DIR/api.ts" ]; then
        echo "  ✅ Plugin API configurado"
    else
        echo "  ❌ Plugin API não encontrado"
    fi
    
    if [ -f "$PLUGINS_DIR/auth.ts" ]; then
        echo "  ✅ Plugin Auth configurado"
    else
        echo "  ❌ Plugin Auth não encontrado"
    fi
    
    if [ -f "$PLUGINS_DIR/icons.ts" ]; then
        echo "  ✅ Plugin Icons configurado"
    else
        echo "  ❌ Plugin Icons não encontrado"
    fi
else
    echo "❌ Diretório de plugins não encontrado"
fi

# Verificar arquivo de ambiente
if [ -f ".env" ]; then
    echo "✅ Arquivo .env encontrado"
elif [ -f ".env.example" ]; then
    echo "⚠️  .env não encontrado, mas .env.example existe"
    echo "   Execute: cp .env.example .env"
else
    echo "❌ Nenhum arquivo de ambiente encontrado"
fi

# Verificar TypeScript
if command -v tsc &> /dev/null; then
    echo "✅ TypeScript encontrado"
else
    echo "⚠️  TypeScript não encontrado globalmente (ok, está em devDependencies)"
fi

echo ""
echo "🎯 Resumo das configurações otimizadas:"
echo "   • Auto-imports para services, stores e composables"
echo "   • Aliases organizados (@components, @services, @types, etc.)"
echo "   • Plugins carregados em ordem otimizada"
echo "   • Componentes com prefixos (Ui, Shared, Business)"
echo "   • Runtime config expandido"
echo "   • SEO otimizado"
echo ""

echo "🚀 Para iniciar o desenvolvimento:"
echo "   npm run dev"
echo ""

echo "📦 Para fazer build de produção:"
echo "   npm run build"
echo ""

echo "✨ Configuração concluída com sucesso!"
