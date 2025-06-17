# *Planify ~ Suíte Acesso e Segurança*
---
## Pré-condições gerais
1. Possuir o banco SQLite da aplicação limpo.
2. Executar o arquivo python `@/backend/seed_data.py` para gerar os dados de teste no banco de dados.
3. Acessar a rota `/api/schema/swagger-ui/#/`.

| Código   | Nome                               | Obrigatório? | Passou? |
| -------- | ---------------------------------- | :----------: | ------- |
| RF-1-001 | Criar usuário                      |      Y       | SIM     |
| RF-1-002 | Editar usuário                     |      Y       | SIM     |
| RF-1-003 | Desativar/Ativar Usuário           |      Y       | SIM     |
| RF-1-004 | Gerar Nova Senha Provisória        |      Y       |         |
| RF-1-005 | Definir Perfis de Acesso           |      Y       |         |
| RF-1-006 | Associar Usuários a Perfis         |      Y       |         |
| RF-1-007 | Trocar Senha                       |      Y       |         |
| RF-1-008 | Recuperar Senha (Lembrar Senha)    |      Y       |         |
| RF-1-009 | Definir Política de Senhas         |      Y       |         |
| RF-1-010 | Autenticar Usuário (Login)         |      Y       |         |
| RF-1-011 | Manter usuários                    |      Y       |         |
| RF-1-013 | Manter Perfil de Usuários          |      Y       |         |
| RF-1-017 | Lembrar Senha                      |      Y       |         |
| RF-1-012 | Expirar senha do usuário           |      N       |         |
| RF-1-015 | Impedir reuso de senha             |      N       |         |
| RF-1-016 | Impedir uso de senhas fracas       |      N       | sim     |
| RF-1-018 | Bloquear usuário por erro de senha |      N       |         |
| RF-1-019 | Manter Preferências do Usuário     |      N       |         |
| RF-1-020 | Consultar usuários e perfis        |      N       |         |
