// tailwind.config.js - Configuração do Tailwind CSS para o projeto
// Documentação: https://tailwindcss.com/docs/configuration

/** @type {import('tailwindcss').Config} */
module.exports = {
  // Ativa o modo escuro via classe CSS (ex: <body class="dark">)
  darkMode: 'class',
  // Define os caminhos dos arquivos onde o Tailwind irá buscar classes utilizadas
  content: [
    './components/**/*.{js,vue,ts}', // Componentes Vue, JS e TS
    './layouts/**/*.vue',            // Layouts Vue
    './pages/**/*.vue',              // Páginas Vue
    './plugins/**/*.{js,ts}',        // Plugins JS e TS
    './app.vue',                     // Arquivo principal
    './error.vue',                   // Página de erro
  ],
  theme: {
    // Configuração do container centralizado
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    // Extensões de tema personalizadas
    extend: {
      // Cores customizadas baseadas em variáveis CSS
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        chart: {
          1: 'hsl(var(--chart-1))',
          2: 'hsl(var(--chart-2))',
          3: 'hsl(var(--chart-3))',
          4: 'hsl(var(--chart-4))',
          5: 'hsl(var(--chart-5))',
        },
      },
      // Bordas arredondadas baseadas em variáveis CSS
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      // Animações customizadas
      keyframes: {
        'accordion-down': {
          from: { height: 0 },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: 0 },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
      },
    },
  },
  // Plugin para animações (opcional, pode ser removido se não for usado)
  plugins: [
    require('tailwindcss-animate'),
    require('@tailwindcss/typography'),
    // Outros plugins podem ser adicionados aqui
  ],
};
// DICA: Se não estiver usando variáveis CSS para cores ou animações customizadas, simplifique removendo as extensões em 'extend'.
// Mantenha apenas o necessário para evitar conflitos e facilitar a manutenção.
