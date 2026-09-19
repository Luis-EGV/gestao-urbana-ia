# Sistema de Gestão Urbana com Inteligência Artificial

Sistema desenvolvido para auxiliar no registro, análise, priorização e gerenciamento de ocorrências urbanas.

O projeto utiliza Inteligência Artificial para analisar imagens e informações enviadas pelos cidadãos, gerando um Índice de Prioridade Urbana (IPU) para auxiliar os gestores na identificação das ocorrências que necessitam de maior atenção.

## Tecnologias utilizadas

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

### Inteligência Artificial
- YOLOv8
- Análise de imagem
- Análise textual
- Análise de contexto
- Índice de Prioridade Urbana (IPU)

### Frontend
- React
- Vite
- JavaScript
- HTML
- CSS

## Funcionamento do sistema

O fluxo principal do sistema é:

1. O cidadão registra uma ocorrência urbana.
2. Uma foto da ocorrência é enviada.
3. A localização é obtida através de GPS.
4. O cidadão fornece uma descrição do problema.
5. A API recebe os dados da ocorrência.
6. O YOLO analisa a imagem.
7. O sistema analisa a descrição e o contexto da ocorrência.
8. O Índice de Prioridade Urbana (IPU) é calculado.
9. A ocorrência é armazenada no PostgreSQL.
10. O gestor visualiza as ocorrências através do painel web.

## Índice de Prioridade Urbana

O IPU é utilizado para auxiliar na priorização das ocorrências.

O cálculo considera informações como:

- análise da imagem;
- confiança da detecção;
- descrição da ocorrência;
- contexto da localização.

As ocorrências podem ser classificadas em níveis como:

- Mediano
- Perigoso
- Risco

As ocorrências com maior IPU aparecem primeiro na fila do gestor.

## Funcionalidades implementadas

- API REST utilizando FastAPI
- Integração com PostgreSQL
- Análise de imagens utilizando YOLOv8
- Análise da descrição da ocorrência
- Análise de contexto
- Cálculo automático do IPU
- Geração automática de protocolo
- Armazenamento das denúncias
- Consulta de denúncias
- Filtros por status e nível
- Atualização do status das ocorrências
- Painel web para gestores
- Integração React com FastAPI
- Fila de ocorrências ordenada pelo IPU
- Visualização dos detalhes das ocorrências

## Estrutura do projeto

```text
gestao-urbana/
│
├── backend/
│   ├── api.py
│   ├── banco.py
│   ├── calcular_risco.py
│   ├── localizacao.py
│   ├── salvar_denuncia.py
│   ├── requirements.txt
│   └── .env.example
│
├── painel-gestor/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md