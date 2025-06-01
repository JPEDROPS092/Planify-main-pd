# Changelog de Padronização de Componentes UI

## [1.0.0] - 2025-05-31

### Componentes Padronizados

- Avatar
- Badge
- Button
- Card

### Melhorias Gerais

- Adicionada documentação detalhada em todos os componentes
- Criados arquivos README.md para cada componente com exemplos de uso
- Padronizados os estilos e variantes em todos os componentes
- Corrigidas as importações para evitar duplicação de componentes no registro do Nuxt
- Melhorada a acessibilidade em todos os componentes

### Avatar

- Criado arquivo index.ts com exportações explícitas
- Adicionadas variantes de tamanho (sm, base, lg)
- Adicionadas variantes de forma (circle, square)
- Melhorada a documentação dos componentes AvatarImage e AvatarFallback
- Adicionados comentários explicativos em cada componente

### Badge

- Criado arquivo index.ts com exportações explícitas
- Adicionadas variantes de estilo (default, secondary, outline, destructive, success)
- Melhorada a documentação com exemplos de uso
- Adicionados comentários explicativos

### Button

- Criado arquivo index.ts com exportações explícitas
- Adicionadas variantes de estilo (default, secondary, outline, ghost, link, destructive, success)
- Adicionadas variantes de tamanho (default, sm, lg, icon)
- Melhorada a documentação com exemplos de uso
- Adicionados comentários explicativos

### Card

- Criado arquivo index.ts com exportações explícitas
- Padronizados todos os subcomponentes (CardHeader, CardTitle, CardDescription, CardContent, CardFooter)
- Adicionado suporte para elementos HTML personalizados no CardTitle (h1, h2, h3, etc.)
- Melhorada a documentação com exemplos de uso
- Adicionados comentários explicativos em cada componente
