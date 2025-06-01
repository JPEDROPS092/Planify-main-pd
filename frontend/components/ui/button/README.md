# Componente Button

Este componente é usado para ações interativas como submissão de formulários, navegação, ou qualquer interação que requeira um botão no Planify.

## Variantes

O componente Button suporta as seguintes variantes:

### Estilos (variant)

- `default`: Estilo padrão com fundo primário
- `secondary`: Estilo secundário com fundo mais claro
- `outline`: Estilo com apenas borda
- `ghost`: Estilo transparente que mostra fundo apenas no hover
- `link`: Estilo de link com sublinhado no hover
- `destructive`: Estilo para ações destrutivas ou perigosas
- `success`: Estilo para indicar sucesso ou confirmação

### Tamanhos (size)

- `default`: Tamanho padrão
- `sm`: Pequeno
- `lg`: Grande
- `icon`: Quadrado, ideal para botões com apenas ícones

## Exemplos de Uso

### Botão Padrão

```vue
<Button>Enviar</Button>
```

### Botão com Variantes

```vue
<Button variant="outline" size="sm">Cancelar</Button>
<Button variant="destructive">Excluir</Button>
<Button variant="ghost">Menu</Button>
<Button variant="link">Saiba mais</Button>
<Button variant="success" size="lg">Confirmar</Button>
```

### Botão como Link

```vue
<Button as="a" href="/dashboard">Dashboard</Button>
```

### Botão com Ícone

```vue
<Button variant="outline" size="icon">
  <IconComponent />
</Button>
```

## Acessibilidade

- Use textos descritivos que indicam claramente a ação do botão
- Adicione aria-label para botões que contêm apenas ícones
- Mantenha um tamanho mínimo de 44x44px para áreas tocáveis em dispositivos móveis
- Certifique-se de que o contraste entre o texto e o fundo do botão atenda às diretrizes WCAG
