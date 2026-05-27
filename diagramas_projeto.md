# Diagramas do Projeto - Feedback System

Este documento contém os diagramas representativos da arquitetura, dados e interações do sistema baseados na sintaxe **Mermaid**. Eles podem ser visualizados nativamente em plataformas como GitHub, Notion, Obsidian e por extensões do VS Code.

---

## 1. Diagrama de Caso de Uso

Este diagrama descreve as interações dos diferentes atores (Colaborador, Gestor e Administrador Master) com as principais funcionalidades do sistema.

```mermaid
flowchart LR
    %% Definição de Atores
    Colaborador["👤 Colaborador<br>(Acesso Público - Sem Login/Cadastro)"]
    Gestor["👥 Responsável / Gestor<br>(Requer Login)"]
    Master["👑 Administrador Master<br>(Requer Login)"]

    subgraph Sistema ["Feedback System"]
        UC1("Submeter Feedback<br>(Anônimo ou Canal Sigiloso via Protocolo)")
        UC2("Responder Pesquisa de Clima<br>(Anônimo por Setor)")
        UC3("Visualizar Comunicados")
        
        UC4("Visualizar Feedbacks do Setor")
        UC5("Responder Feedbacks do Setor")
        
        UC6("Gerenciar Usuários e Perfis")
        UC7("Criar e Gerenciar Pesquisas de Clima")
        UC8("Visualizar Dashboard & Relatórios (Análise IA)")
    end

    %% Associações do Colaborador
    Colaborador --> UC1
    Colaborador --> UC2
    Colaborador --> UC3

    %% Associações do Gestor de Setor
    Gestor --> UC3
    Gestor --> UC4
    Gestor --> UC5

    %% Associações do Administrador Master
    Master --> UC3
    Master --> UC4
    Master --> UC5
    Master --> UC6
    Master --> UC7
    Master --> UC8
```

---

## 2. Diagrama Entidade-Relacionamento (DER)

Representa o modelo físico do banco de dados relacional do sistema, incluindo os modelos do sistema de autenticação, perfis, feedbacks e pesquisas de clima.

> [!NOTE]
> O sistema não exige login ou cadastro para os colaboradores (que enviam feedbacks e respondem pesquisas de clima). A tabela **USUARIO_ADMIN** (que mapeia diretamente para `auth.User` do Django) armazena exclusivamente as credenciais de administradores (Master) e gestores de setores para acesso ao Dashboard administrativo.

```mermaid
erDiagram
    USUARIO_ADMIN ||--o| PERFIL : "tem (OneToOne)"
    USUARIO_ADMIN ||--o{ SETOR : "gerencia (responsavel)"
    SETOR ||--o{ PERFIL : "possui (membros)"
    SETOR ||--o{ FEEDBACK : "recebe"
    FEEDBACK ||--o| RESPOSTA : "possui (OneToOne)"
    
    PESQUISA_CLIMA ||--o{ PERGUNTA : "possui"
    PESQUISA_CLIMA ||--o{ RESPOSTA_CLIMA : "recebe"
    SETOR ||--o{ RESPOSTA_CLIMA : "responde"
    RESPOSTA_CLIMA ||--o{ RESPOSTA_PERGUNTA : "detalha"
    PERGUNTA ||--o{ RESPOSTA_PERGUNTA : "responde"

    USUARIO_ADMIN {
        int id PK
        string username
        string password
        boolean is_superuser
        boolean is_staff
    }

    PERFIL {
        int id PK
        int user_id FK
        int setor_id FK
        boolean is_master
    }

    SETOR {
        int id PK
        string nome
        int responsavel_id FK
    }

    FEEDBACK {
        int id PK
        int setor_id FK
        text mensagem
        datetime data_criacao
        boolean lido
        int curtidas
        string categoria
        int nota_enps
        string sentimento
        boolean is_sensivel
        string protocolo
    }

    RESPOSTA {
        int id PK
        int feedback_id FK
        text texto_resposta
        datetime data_resposta
    }

    COMUNICADO {
        int id PK
        string titulo
        text conteudo
        datetime data_criacao
        string tipo
        boolean ativo
    }

    PESQUISA_CLIMA {
        int id PK
        string titulo
        text descricao
        boolean ativa
        datetime data_inicio
    }

    PERGUNTA {
        int id PK
        int pesquisa_id FK
        string texto
        string tipo
        boolean obrigatoria
    }

    RESPOSTA_CLIMA {
        int id PK
        int pesquisa_id FK
        int setor_id FK
        int nota_enps
        text comentario_ia
        string sentimento
        datetime data_envio
    }

    RESPOSTA_PERGUNTA {
        int id PK
        int resposta_clima_id FK
        int pergunta_id FK
        text resposta_texto
        int resposta_nota
    }
```

---

## 3. Diagrama de Classes UML

Demonstra a estrutura orientada a objetos das classes de modelo (Django Models) do projeto, com seus atributos, métodos e relações estruturais.

```mermaid
classDiagram
    class DjangoUser {
        +int id
        +string username
        +string password
        +boolean is_superuser
        +boolean is_staff
    }

    class Perfil {
        +int id
        +DjangoUser user
        +Setor setor
        +boolean is_master
        +__str__()
    }

    class Setor {
        +int id
        +string nome
        +DjangoUser responsavel
        +__str__()
    }

    class Feedback {
        +int id
        +Setor setor
        +string mensagem
        +datetime data_criacao
        +boolean lido
        +int curtidas
        +string categoria
        +int nota_enps
        +string sentimento
        +boolean is_sensivel
        +string protocolo
        +__str__()
    }

    class Resposta {
        +int id
        +Feedback feedback
        +string texto_resposta
        +datetime data_resposta
    }

    class Comunicado {
        +int id
        +string titulo
        +string conteudo
        +datetime data_criacao
        +string tipo
        +boolean ativo
        +__str__()
    }

    class PesquisaClima {
        +int id
        +string titulo
        +string descricao
        +boolean ativa
        +datetime data_inicio
        +__str__()
    }

    class Pergunta {
        +int id
        +PesquisaClima pesquisa
        +string texto
        +string tipo
        +boolean obrigatoria
        +__str__()
    }

    class RespostaClima {
        +int id
        +PesquisaClima pesquisa
        +Setor setor
        +int nota_enps
        +string comentario_ia
        +string sentimento
        +datetime data_envio
        +__str__()
    }

    class RespostaPergunta {
        +int id
        +RespostaClima resposta_clima
        +Pergunta pergunta
        +string resposta_texto
        +int resposta_nota
        +__str__()
    }

    DjangoUser "1" -- "1" Perfil : tem
    DjangoUser "1" -- "0..*" Setor : gerencia
    Setor "1" -- "0..*" Perfil : possui
    Setor "1" -- "0..*" Feedback : recebe
    Feedback "1" -- "1" Resposta : possui
    PesquisaClima "1" -- "0..*" Pergunta : possui
    PesquisaClima "1" -- "0..*" RespostaClima : recebe
    Setor "0..1" -- "0..*" RespostaClima : responde
    RespostaClima "1" -- "0..*" RespostaPergunta : detalha
    Pergunta "1" -- "0..*" RespostaPergunta : responde
```
