# Painel do Gestor

Painel web utilizado pelos gestores para visualizar e acompanhar as ocorrências urbanas.

Tecnologias:

- React
- Vite
- JavaScript
- CSS

## Antes de iniciar

O FastAPI deve estar funcionando em:

```text
http://127.0.0.1:8000
```

Consulte:

```text
backend/README.md
```

## 1. Entrar na pasta

Abra um segundo terminal:

```powershell
cd painel-gestor
```

## 2. Instalar dependências

Na primeira execução:

```powershell
npm install
```

## 3. Iniciar o painel

```powershell
npm run dev
```

O Vite mostrará um endereço semelhante a:

```text
http://localhost:5173
```

Abra esse endereço no navegador.

## Servidores durante a apresentação

Mantenha dois terminais abertos.

### Terminal 1

```powershell
cd backend
py -m uvicorn api:app --reload
```

### Terminal 2

```powershell
cd painel-gestor
npm run dev
```

Depois abra:

```text
http://localhost:5173
```

O painel buscará as ocorrências através da API FastAPI.
