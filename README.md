# Sistema de Gestão Urbana com Inteligência Artificial

Sistema para registro, análise, priorização e gerenciamento de ocorrências urbanas.

O projeto utiliza Inteligência Artificial para analisar as informações enviadas pelos cidadãos e calcular um **Índice de Prioridade Urbana (IPU)**, auxiliando o gestor na organização das ocorrências.

## Tecnologias

### Backend
- Python
- FastAPI
- SQLAlchemy

### Inteligência Artificial
- YOLOv8
- Modelo treinado `best.pt`
- Análise textual
- Análise de contexto
- Índice de Prioridade Urbana (IPU)

### Banco de dados
- PostgreSQL

### Painel
- React
- Vite
- JavaScript
- HTML
- CSS

---

# Estrutura

```text
gestao-urbana-ia/
│
├── backend/
│   └── API FastAPI e regras do sistema
│
├── database/
│   └── Script para criação do banco
│
├── modelo/
│   └── Modelo YOLO treinado
│
└── painel-gestor/
    └── Painel web React
```

Cada pasta possui seu próprio `README.md` com instruções específicas.

---

# Como executar o projeto

Para configurar um computador novo, siga esta ordem:

## 1. Baixar o projeto

No Git:

```bash
git clone https://github.com/Luis-EGV/gestao-urbana-ia.git
```

Entre na pasta:

```bash
cd gestao-urbana-ia
```

Também é possível utilizar **Code > Download ZIP** pelo GitHub.

---

## 2. Configurar o PostgreSQL

Primeiro configure o banco de dados.

Entre na pasta:

```text
database/
```

Leia:

```text
database/README.md
```

O banco utilizado pelo projeto é:

```text
gestao_urbana
```

O arquivo:

```text
database/database.sql
```

contém a estrutura necessária para criação da tabela de denúncias.

---

## 3. Configurar o backend

Depois configure:

```text
backend/
```

Leia:

```text
backend/README.md
```

Será necessário:

1. instalar Python;
2. instalar as dependências;
3. criar o arquivo `.env`;
4. configurar a conexão com PostgreSQL;
5. iniciar o FastAPI.

Servidor do backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 4. Modelo YOLO

O modelo treinado utilizado pelo sistema está disponível em:

```text
modelo/best.pt
```

Não é necessário treinar novamente o YOLO para executar a demonstração.

Mais informações:

```text
modelo/README.md
```

---

## 5. Iniciar o painel do gestor

Entre em:

```text
painel-gestor/
```

Leia:

```text
painel-gestor/README.md
```

O painel utiliza React + Vite.

Servidor local:

```text
http://localhost:5173
```

---

# Ordem para apresentação

Depois que o computador estiver configurado, para iniciar o sistema novamente basta:

### 1 — verificar se PostgreSQL está funcionando

Banco:

```text
gestao_urbana
```

### 2 — abrir o backend

Terminal 1:

```bash
cd backend
py -m uvicorn api:app --reload
```

### 3 — abrir o painel

Terminal 2:

```bash
cd painel-gestor
npm run dev
```

### 4 — abrir no navegador

Painel:

```text
http://localhost:5173
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# Arquitetura

```text
CIDADÃO
   │
   │ Foto + descrição + localização
   ▼
FASTAPI
   │
   ├── YOLOv8
   │      └── best.pt
   │
   ├── Análise textual
   │
   ├── Análise de contexto
   │
   └── Cálculo do IPU
   │
   ▼
POSTGRESQL
   │
   ▼
PAINEL DO GESTOR
   │
   ▼
Fila de ocorrências por prioridade
```

---

# Funcionalidades implementadas

- API REST com FastAPI
- Banco PostgreSQL
- Modelo YOLOv8 treinado
- Análise de imagens
- Análise textual
- Análise de contexto
- Cálculo do IPU
- Geração de protocolo
- Armazenamento de ocorrências
- Consulta de denúncias
- Filtro por status
- Filtro por nível
- Alteração de status
- Painel web React
- Fila de prioridade por IPU
- Visualização dos detalhes das ocorrências

---

# Status

Projeto em desenvolvimento.

Novas funcionalidades serão adicionadas ao aplicativo do cidadão e ao painel administrativo.
