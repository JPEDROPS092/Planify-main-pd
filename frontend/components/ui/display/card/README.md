# Componentes Card

Este conjunto de componentes é usado para criar cartões de conteúdo com diferentes seções no Planify.

## Componentes

- `Card`: Componente principal que define o contêiner do card
- `CardHeader`: Componente para o cabeçalho do card
- `CardTitle`: Componente para o título do card
- `CardDescription`: Componente para a descrição do card
- `CardContent`: Componente para o conteúdo principal do card
- `CardFooter`: Componente para o rodapé do card

## Exemplos de Uso

### Card Básico

```vue
<Card>
  <CardContent>
    Conteúdo do card
  </CardContent>
</Card>
```

### Card Completo

```vue
<Card>
  <CardHeader>
    <CardTitle>Título do Card</CardTitle>
    <CardDescription>Descrição detalhada do card</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Este é o conteúdo principal do card.</p>
  </CardContent>
  <CardFooter>
    <Button variant="outline">Cancelar</Button>
    <Button>Salvar</Button>
  </CardFooter>
</Card>
```

### Card com Título Personalizado

```vue
<Card>
  <CardHeader>
    <CardTitle as="h2" class="text-xl text-primary">Título Personalizado</CardTitle>
    <CardDescription>Descrição do card</CardDescription>
  </CardHeader>
  <CardContent>
    Conteúdo do card
  </CardContent>
</Card>
```

### Card com Classes Personalizadas

```vue
<Card class="max-w-md mx-auto shadow-lg">
  <CardHeader class="bg-secondary/10">
    <CardTitle>Título do Card</CardTitle>
  </CardHeader>
  <CardContent>
    Conteúdo do card
  </CardContent>
  <CardFooter class="flex justify-end gap-2">
    <Button>Ação</Button>
  </CardFooter>
</Card>
```

## Acessibilidade

- Use hierarquia adequada de títulos (h1, h2, h3) para manter a estrutura semântica
- Mantenha contraste adequado entre texto e fundo
- Considere adicionar `aria-labelledby` ao Card, referenciando o ID do CardTitle para melhorar a navegação por leitores de tela
