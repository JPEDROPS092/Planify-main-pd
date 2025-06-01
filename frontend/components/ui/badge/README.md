# Componente Badge

Este componente é usado para exibir etiquetas, status ou pequenas informações destacadas no Planify.

## Variantes

O componente Badge suporta as seguintes variantes:

### Estilos (variant)

- `default`: Estilo padrão com fundo primário (azul)
- `secondary`: Estilo secundário com fundo mais claro
- `outline`: Estilo com apenas borda
- `destructive`: Estilo para ações destrutivas ou alertas (vermelho)
- `success`: Estilo para indicar sucesso ou conclusão (verde)

## Exemplos de Uso

### Badge Padrão

```vue
<Badge>Novo</Badge>
```

### Badge com Variantes

```vue
<Badge variant="success">Concluído</Badge>
<Badge variant="destructive">Cancelado</Badge>
<Badge variant="outline">Em andamento</Badge>
<Badge variant="secondary">Pendente</Badge>
```

### Badge com Classes Personalizadas

```vue
<Badge class="px-4 py-1">Personalizado</Badge>
```

## Acessibilidade

- Use cores com contraste adequado para garantir legibilidade
- Evite usar apenas cor para transmitir informações importantes
- Considere adicionar ícones junto com o texto para melhorar a compreensão visual
