# *Planify ~ Plano de Testes*

### **Histórico / Autor(es)**

| Versão | Data       | Autor(es)              | Descrição  |
| ------ | ---------- | ---------------------- | ---------- |
| 1.0    | 04/06/2025 | - Luiz Felipe Oliveira | Elaboração |

---
## **1 - Introdução**
Neste documento estarão apresentados os requisitos testáveis definidos no **documento de visão**, junto de seu caso de teste correspondente, organizando os testes por **suítes**.
## **2 - Requisitos testáveis**
Abaixo estão listados os nomes dos requisitos funcionais para rápida consulta. Podem ser conferidos em mais detalhes no **documento de visão**.
## **2.1 - Acesso e segurança**

| Código   | Nome                               | Obrigatório? |
| -------- | ---------------------------------- | :----------: |
| RF-1-001 | Criar usuário                      |      Y       |
| RF-1-002 | Editar usuário                     |      Y       |
| RF-1-003 | Desativar/Ativar Usuário           |      Y       |
| RF-1-004 | Gerar Nova Senha Provisória        |      Y       |
| RF-1-005 | Definir Perfis de Acesso           |      Y       |
| RF-1-006 | Associar Usuários a Perfis         |      Y       |
| RF-1-007 | Trocar Senha                       |      Y       |
| RF-1-008 | Recuperar Senha (Lembrar Senha)    |      Y       |
| RF-1-009 | Definir Política de Senhas         |      Y       |
| RF-1-010 | Autenticar Usuário (Login)         |      Y       |
| RF-1-011 | Manter usuários                    |      Y       |
| RF-1-013 | Manter Perfil de Usuários          |      Y       |
| RF-1-017 | Lembrar Senha                      |      Y       |
| RF-1-012 | Expirar senha do usuário           |      N       |
| RF-1-015 | Impedir reuso de senha             |      N       |
| RF-1-016 | Impedir uso de senhas fracas       |      N       |
| RF-1-018 | Bloquear usuário por erro de senha |      N       |
| RF-1-019 | Manter Preferências do Usuário     |      N       |
| RF-1-020 | Consultar usuários e perfis        |      N       |
|          |                                    |              |
## **2.2 - Cadastro de projetos**
| Código   | Nome                           | Obrigatório? |
| -------- | ------------------------------ | :----------: |
| RF-2-001 | Cadastrar Novo Projeto         |      Y       |
| RF-2-002 | Editar Projeto                 |      Y       |
| RF-2-003 | Adicionar Membros ao Projeto   |      Y       |
| RF-2-004 | Remover Membros do Projeto     |      Y       |
| RF-2-005 | Alterar Status do Projeto      |      Y       |
| RF-2-006 | Visualizar Detalhes do Projeto |      Y       |
| RF-2-007 | Listar Projetos                |      Y       |
| RF-2-008 | Arquivar Projeto               |      N       |
|          |                                |              |

## **2.3 - Gestão de tarefa**
| Código   | Nome                           | Obrigatório? |
| -------- | ------------------------------ | :----------: |
| RF-3-001 | Manter Tarefa                  |      Y       |
| RF-3-002 | Atribuir Responsáveis à Tarefa |      Y       |
| RF-3-003 | Gerenciar Status de Tarefa     |      Y       |
| RF-3-004 | Associar Tarefa à Sprints      |      Y       |
| RF-3-005 | FIltrar tarefas                |      Y       |
|          |                                |              |

## **2.4 - Gestão de equipes**
| Código   | Nome                                  | Obrigatório? |
| -------- | ------------------------------------- | :----------: |
| RF-4-001 | Manter Equipe                         |      Y       |
| RF-4-002 | Atribuir Papeis aos Membros da Equipe |      Y       |
| RF-4-003 | Gerenciar Membros De  Equipe          |      Y       |
| RF-4-004 | Visualizar lista de membros           |      Y       |
|          |                                       |              |

## **2.5 - Gestão de recursos**
| Código   | Nome                        | Obrigatório? |
| -------- | --------------------------- | :----------: |
| RF-5-001 | Alocar Recursos Financeiros |      Y       |
|          |                             |              |

## **2.6 - Comunicação e colaboração**
| Código   | Nome                             | Obrigatório? |
| -------- | -------------------------------- | :----------: |
| RF-6-001 | Chat Integrado por Projeto       |      Y       |
| RF-6-002 | Notificar Informações de Tarefas | *Importante* |
|          |                                  |              |

## **2.7 - Calendário de projetos**
| Código   | Nome              | Obrigatório? |
| -------- | ----------------- | :----------: |
| RF-7-001 | Exibir calendário |      Y       |
|          |                   |              |

## **2.8 - Gestão de riscos**
| Código   | Nome                     | Obrigatório? |
| -------- | ------------------------ | :----------: |
| RF-8-001 | Cadastrar Riscos         |      Y       |
| RF-8-002 | Visualizar Riscos        |      Y       |
| RF-8-003 | Desativar/Ativar Usuário |      Y       |
|          |                          |              |

## **2.9 - Gestão de custos**
| Código   | Nome                      | Obrigatório? |
| -------- | ------------------------- | :----------: |
| RF-9-001 | Registrar custos          |      Y       |
| RF-9-002 | Gerar relatório de custos |      Y       |
|          |                           |              |

## **2.10 - Gestão de documentação**
| Código    | Nome                           | Obrigatório? |
| --------- | ------------------------------ | :----------: |
| RF-10-001 | Anexar documentos              |      Y       |
| RF-10-002 | Associar documentos às tarefas |      Y       |
|           |                                |              |

## **3 - Suítes de teste**
## **3.1 - Acesso e segurança**

## **4 - Mudanças futuras**

- [ ] Adicionar testes para requisitos não funcionais
- [ ] 

