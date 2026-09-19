# Backend — FastAPI

Esta pasta contém a API e as regras do Sistema de Gestão Urbana.

Antes de configurar o backend, configure:

```text
database/README.md
```

## 1. Entrar na pasta

```powershell
cd backend
```

## 2. Instalar dependências

```powershell
py -m pip install -r requirements.txt
```

## 3. Configurar o `.env`

Crie:

```text
.env
```

Use `.env.example` como referência:

```env
DATABASE_URL=postgresql+psycopg2://postgres:SUA_SENHA@localhost:5432/gestao_urbana
```

Nunca envie sua senha para o GitHub.

## 4. Testar PostgreSQL

```powershell
py -c "from banco import engine; conn = engine.connect(); print('Conexão com PostgreSQL funcionando!'); conn.close()"
```

Resultado esperado:

```text
Conexão com PostgreSQL funcionando!
```

## 5. Iniciar FastAPI

```powershell
py -m uvicorn api:app --reload
```

Resultado:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Mantenha esse terminal aberto enquanto estiver utilizando o sistema.

## 6. Próxima etapa

Depois que o backend estiver funcionando, siga:

```text
painel-gestor/README.md
```
