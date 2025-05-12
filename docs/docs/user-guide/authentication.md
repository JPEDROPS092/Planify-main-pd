---
sidebar_position: 2
---

# Autenticação e Perfil de Usuário

O sistema de autenticação do Planify garante a segurança e o controle de acesso às funcionalidades da plataforma. Esta seção explica como gerenciar sua conta, autenticação e perfil de usuário.

## Criação de Conta

### Registro de Novo Usuário

Para criar uma nova conta no Planify:

1. Acesse a página inicial do Planify
2. Clique no botão "Criar Conta"
3. Preencha o formulário de registro:
   - Nome completo
   - Email (será seu nome de usuário)
   - Senha (deve atender aos requisitos de segurança)
   - Confirmação de senha
4. Leia e aceite os termos de uso
5. Clique em "Registrar"

<!-- <!-- ![Tela de Registro](/img/docs/register-screen.png) --> -->

:::note Nota
Dependendo da configuração do sistema, novos registros podem requerer aprovação de um administrador.
:::

### Confirmação de Email

Após o registro, você receberá um email de confirmação:

1. Verifique sua caixa de entrada (e pasta de spam, se necessário)
2. Clique no link de confirmação no email
3. Você será redirecionado para a página de login com uma mensagem de confirmação

## Login e Autenticação

### Fazendo Login

Para acessar sua conta:

1. Acesse a página inicial do Planify
2. Digite seu email e senha
3. (Opcional) Marque "Lembrar-me" para manter a sessão ativa
4. Clique em "Entrar"

<!-- <!-- ![Tela de Login](/img/docs/login-screen.png) --> -->

### Recuperação de Senha

Se você esquecer sua senha:

1. Na tela de login, clique em "Esqueceu a senha?"
2. Digite o email associado à sua conta
3. Clique em "Enviar link de recuperação"
4. Verifique seu email e clique no link recebido
5. Defina uma nova senha seguindo os requisitos de segurança

### Política de Senhas

O Planify implementa uma política de senhas robusta para garantir a segurança das contas:

- Mínimo de 8 caracteres
- Pelo menos uma letra maiúscula
- Pelo menos uma letra minúscula
- Pelo menos um número
- Pelo menos um caractere especial (ex: !@#$%^&*)
- Não pode ser similar ao seu nome ou email
- Não pode ser uma senha comum (ex: "123456", "password")

### Bloqueio de Conta

Por segurança, sua conta será temporariamente bloqueada após múltiplas tentativas de login malsucedidas:

- Após 5 tentativas incorretas, a conta será bloqueada por 30 minutos
- Você receberá um email notificando sobre o bloqueio
- Para desbloquear imediatamente, use o processo de recuperação de senha

## Gerenciamento de Perfil

### Visualizando seu Perfil

Para acessar seu perfil:

1. Clique no seu nome/avatar no canto superior direito
2. Selecione "Meu Perfil" no menu suspenso

<!-- <!-- ![Perfil de Usuário](/img/docs/user-profile.png) --> -->

### Editando Informações do Perfil

Na página de perfil, você pode editar:

1. **Informações Básicas**:
   - Nome completo
   - Título/Cargo
   - Biografia
   - Informações de contato

2. **Foto de Perfil**:
   - Clique na imagem atual ou no ícone de câmera
   - Faça upload de uma nova imagem
   - Ajuste o recorte conforme necessário
   - Clique em "Salvar"

3. **Preferências**:
   - Idioma da interface
   - Fuso horário
   - Formato de data/hora
   - Tema (claro/escuro)

### Alterando sua Senha

Para alterar sua senha:

1. Acesse seu perfil
2. Clique na aba "Segurança"
3. Digite sua senha atual
4. Digite e confirme a nova senha
5. Clique em "Atualizar Senha"

:::caution Atenção
Após alterar sua senha, você receberá um email de confirmação. Se você não realizou esta alteração, entre em contato com o administrador imediatamente.
:::

### Configurando Notificações

Personalize quais notificações deseja receber:

1. Acesse seu perfil
2. Clique na aba "Notificações"
3. Configure as preferências para cada tipo de notificação:
   - **Email**: Receba notificações por email
   - **In-app**: Receba notificações dentro do sistema
   - **Push**: Receba notificações no navegador (se suportado)
4. Clique em "Salvar Preferências"

## Autenticação de Dois Fatores (2FA)

Para maior segurança, você pode ativar a autenticação de dois fatores:

### Ativando 2FA

1. Acesse seu perfil
2. Clique na aba "Segurança"
3. Na seção "Autenticação de Dois Fatores", clique em "Ativar"
4. Escolha o método de autenticação:
   - Aplicativo Autenticador (recomendado)
   - SMS
5. Siga as instruções na tela para configurar

### Usando 2FA

Quando o 2FA estiver ativo:

1. Faça login com seu email e senha
2. Você será solicitado a fornecer o código de verificação
3. Abra seu aplicativo autenticador ou verifique o SMS
4. Digite o código de 6 dígitos
5. Clique em "Verificar"

### Códigos de Backup

Ao ativar o 2FA, você receberá códigos de backup:

1. Guarde esses códigos em um local seguro
2. Use um código de backup caso não tenha acesso ao seu dispositivo
3. Cada código pode ser usado apenas uma vez
4. Você pode gerar novos códigos a qualquer momento

## Sessões Ativas

### Gerenciando Sessões

Visualize e gerencie suas sessões ativas:

1. Acesse seu perfil
2. Clique na aba "Segurança"
3. Na seção "Sessões Ativas", veja todos os dispositivos conectados
4. Para encerrar uma sessão, clique em "Encerrar" ao lado dela
5. Para encerrar todas as sessões, exceto a atual, clique em "Encerrar Todas"

### Expiração de Sessão

Por segurança, sua sessão expirará após um período de inatividade:

- Em navegadores desktop: 2 horas de inatividade
- Em dispositivos móveis: 1 hora de inatividade
- Se "Lembrar-me" estiver marcado: 2 semanas (independente de atividade)

## Próximos Passos

Agora que você entende como gerenciar sua conta e perfil, continue para o [Dashboard](/docs/user-guide/dashboard) para aprender sobre a interface principal do sistema.
