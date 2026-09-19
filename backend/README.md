
# Backend — Sistema de Gestão Urbana

Este documento explica passo a passo como configurar e iniciar o backend do Sistema de Gestão Urbana.

O backend foi desenvolvido utilizando **Python + FastAPI**, com **PostgreSQL** para armazenamento das ocorrências e **YOLOv8** para análise das imagens.

---

# 1. Requisitos

Antes de iniciar o backend, é necessário possuir:

- Python
- PostgreSQL
- pip
- Modelo YOLO treinado

As bibliotecas Python necessárias estão disponíveis no arquivo:

```text
requirements.txt
```

---

# 2. Abrir o terminal

Abra o **Windows PowerShell**.

Entre na pasta do backend:

```powershell
cd C:\GestaoUrbana\gestao-urbana\backend
```

O terminal deverá ficar semelhante a:

```text
PS C:\GestaoUrbana\gestao-urbana\backend>
```

---

# 3. Instalar as dependências

Na primeira execução do projeto, instale as bibliotecas necessárias:

```powershell
py -m pip install -r requirements.txt
```

Esse comando instalará as principais dependências do backend, incluindo:

- FastAPI
- Uvicorn
- SQLAlchemy
- psycopg2
- python-dotenv
- Ultralytics / YOLOv8
- python-multipart

Essa instalação normalmente precisa ser realizada apenas na primeira configuração do projeto.

---

# 4. Configurar o PostgreSQL

O projeto utiliza o banco de dados:

```text
gestao_urbana
```

O PostgreSQL deve estar instalado e o servidor do banco deve estar em execução.

O backend utiliza uma variável de ambiente para armazenar a conexão com o banco.

Dentro da pasta:

```text
backend
```

crie um arquivo:

```text
.env
```

Utilize o arquivo:

```text
.env.example
```

como referência.

Exemplo:

```env
DATABASE_URL=postgresql+psycopg2://postgres:SUA_SENHA@localhost:5432/gestao_urbana
```

Substitua:

```text
SUA_SENHA
```

pela senha configurada no PostgreSQL.

> IMPORTANTE: o arquivo `.env` contém informações privadas e não deve ser enviado para o GitHub.

---

# 5. Testar a conexão com o banco

Antes de iniciar a API, é possível verificar se o Python consegue se conectar ao PostgreSQL.

Execute:

```powershell
py -c "from banco import engine; conn = engine.connect(); print('Conexão com PostgreSQL funcionando!'); conn.close()"
```

Se estiver configurado corretamente, será exibido:

```text
Conexão com PostgreSQL funcionando!
```

---

# 6. Modelo de Inteligência Artificial

O sistema utiliza um modelo YOLOv8 treinado para identificar ocorrências urbanas.

Atualmente, durante o desenvolvimento local, o caminho do modelo é configurado no arquivo:

```text
api.py
```

Exemplo:

```python
model = YOLO(
    "C:/Yolo/runs/ocorrencias_urbanas_v2-2/weights/best.pt"
)
```

Portanto, para executar a análise de imagens, o arquivo:

```text
best.pt
```

deve existir no caminho configurado no `api.py`.

O modelo treinado não está armazenado neste repositório por ser um arquivo gerado durante o treinamento da IA.

---

# 7. Iniciar o servidor FastAPI

Com o PostgreSQL disponível e as dependências instaladas, execute:

```powershell
py -m uvicorn api:app --reload
```

Se tudo estiver funcionando, aparecerá uma mensagem semelhante a:

```text
Uvicorn running on http://127.0.0.1:8000
```

Isso significa que o backend está funcionando.

Não feche esse PowerShell enquanto estiver utilizando o sistema.

---

# 8. Testar a API

Abra o navegador e acesse:

```text
http://127.0.0.1:8000
```

A API deverá responder informando que o sistema está funcionando.

---

# 9. Abrir o Swagger

O FastAPI gera automaticamente uma interface para visualizar e testar os endpoints.

Com o servidor funcionando, acesse:

```text
http://127.0.0.1:8000/docs
```

Nessa página é possível testar os endpoints da API.

Entre os endpoints implementados estão:

```text
GET  /
GET  /denuncias
GET  /denuncias/{protocolo}
GET  /gestor/denuncias
PUT  /denuncias/{protocolo}/status
POST /analisar-denuncia
```

---

# 10. Iniciar o painel do gestor

O painel React utiliza outro servidor.

Por isso, mantenha o PowerShell do backend aberto e abra um **segundo PowerShell**.

Entre na pasta:

```powershell
cd C:\GestaoUrbana\gestao-urbana\painel-gestor
```

Na primeira execução, instale as dependências:

```powershell
npm install
```

Depois execute:

```powershell
npm run dev
```

O Vite deverá informar um endereço semelhante a:

```text
http://localhost:5173
```

Abra esse endereço no navegador.

---

# 11. Servidores necessários

Para utilizar o sistema completo durante o desenvolvimento, mantenha:

```text
┌─────────────────────────────────────┐
│ PostgreSQL                          │
│ Banco: gestao_urbana                │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│ FastAPI                             │
│ http://127.0.0.1:8000               │
│                                     │
│ PowerShell:                         │
│ py -m uvicorn api:app --reload      │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│ React / Vite                        │
│ http://localhost:5173               │
│                                     │
│ Segundo PowerShell:                 │
│ npm run dev                         │
└─────────────────────────────────────┘
```

---

# 12. Resumo para iniciar o projeto

Depois que o ambiente já estiver configurado, o processo diário fica simples.

## Terminal 1 — Backend

```powershell
cd C:\GestaoUrbana\gestao-urbana\backend
py -m uvicorn api:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Terminal 2 — Painel do gestor

```powershell
cd C:\GestaoUrbana\gestao-urbana\painel-gestor
npm run dev
```

Painel:

```text
http://localhost:5173
```

---

# 13. Encerrar os servidores

Para parar o FastAPI ou o Vite, entre no respectivo PowerShell e pressione:

```text
Ctrl + C
```

---

# Fluxo do sistema

```text
Painel React
     │
     ▼
FastAPI
     │
     ├──── YOLOv8
     │
     ├──── Análise textual
     │
     ├──── Análise de contexto
     │
     └──── Cálculo do IPU
     │
     ▼
PostgreSQL
```

O FastAPI atua como intermediário entre o painel/aplicativo, a Inteligência Artificial e o banco de dados.
