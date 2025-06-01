# Componente Avatar

Este conjunto de componentes é usado para exibir avatares de usuários ou entidades no Planify.

## Componentes

- `Avatar`: Componente principal que define o contêiner do avatar
- `AvatarImage`: Componente para exibir a imagem do avatar
- `AvatarFallback`: Componente para exibir quando a imagem não está disponível

## Variantes

O componente Avatar suporta as seguintes variantes:

### Tamanhos (size)

- `sm`: Pequeno (padrão) - 40px x 40px
- `base`: Médio - 64px x 64px
- `lg`: Grande - 128px x 128px

### Formas (shape)

- `circle`: Circular (padrão)
- `square`: Quadrado com bordas arredondadas

## Exemplos de Uso

### Avatar Básico com Fallback

```vue
<Avatar>
  <AvatarImage src="/path/to/image.jpg" alt="Avatar do usuário" />
  <AvatarFallback>JP</AvatarFallback>
</Avatar>
```

### Avatar com Tamanho e Forma Personalizados

```vue
<Avatar size="lg" shape="square">
  <AvatarImage src="/path/to/image.jpg" alt="Avatar do usuário" />
  <AvatarFallback>JP</AvatarFallback>
</Avatar>
```

### Avatar com Classes Personalizadas

```vue
<Avatar class="border-2 border-primary">
  <AvatarImage src="/path/to/image.jpg" alt="Avatar do usuário" />
  <AvatarFallback>JP</AvatarFallback>
</Avatar>
```

## Acessibilidade

- Sempre forneça um atributo `alt` descritivo para o componente `AvatarImage`
- O componente `AvatarFallback` deve conter texto ou conteúdo que identifique o usuário
- O contraste entre o texto do fallback e o fundo deve seguir as diretrizes WCAG
