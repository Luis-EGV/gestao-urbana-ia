# Banco de Dados

Esta pasta contém os arquivos necessários para configurar o PostgreSQL utilizado pelo Sistema de Gestão Urbana.

## Requisito

Instale:

- PostgreSQL
- pgAdmin

## 1. Criar o banco

Abra o pgAdmin.

Acesse:

```text
Servers
→ PostgreSQL
→ Databases
```

Clique com o botão direito em:

```text
Databases
```

Selecione:

```text
Create
→ Database
```

Nome:

```text
gestao_urbana
```

Salve.

## 2. Criar as tabelas

Selecione:

```text
gestao_urbana
```

Abra:

```text
Query Tool
```

Abra o arquivo:

```text
database.sql
```

Copie o conteúdo para o Query Tool e execute.

## 3. Resultado esperado

Deverá existir:

```text
gestao_urbana
└── Schemas
    └── public
        └── Tables
            └── denuncias
```

## 4. Próxima etapa

Depois de configurar o banco, siga para:

```text
backend/README.md
```

para configurar a conexão entre FastAPI e PostgreSQL.
