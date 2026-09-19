from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
from calcular_risco import calcular_ipu
from localizacao import calcular_contexto_local
from salvar_denuncia import (salvar_denuncia,gerar_protocolo,listar_denuncias,buscar_denuncia_por_protocolo,atualizar_status_denuncia,filtrar_denuncias)
from datetime import datetime
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

import shutil
import uuid


app = FastAPI(
    title="API Gestão Urbana",
    description="API para análise de denúncias urbanas com YOLO + IPU",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODELO YOLO

BASE_DIR = Path(__file__).resolve().parent.parent
CAMINHO_MODELO = BASE_DIR / "modelo" / "best.pt"

model = YOLO(str(CAMINHO_MODELO))

# PASTAS

PASTA_UPLOADS = BASE_DIR / "uploads"
PASTA_UPLOADS.mkdir(parents=True, exist_ok=True)

PASTA_IMAGENS = BASE_DIR / "imagens_denuncias"
PASTA_IMAGENS.mkdir(parents=True, exist_ok=True)

app.mount(
    "/imagens",
    StaticFiles(directory=str(PASTA_IMAGENS)),
    name="imagens"
)

# ROTA INICIAL

@app.get("/")
def inicio():
    return {
        "mensagem":
            "API de Gestão Urbana funcionando"
    }

# LISTAR TODAS AS DENÚNCIAS

@app.get("/denuncias")
def obter_denuncias():

    try:
        denuncias = listar_denuncias()
        return {
            "total": len(denuncias),
            "denuncias": denuncias
        }

    except Exception as erro:
        return JSONResponse(
            status_code=500,
            content={
                "erro": str(erro)
            }
        )

# FILA DO GESTOR

@app.get("/gestor/denuncias")
def fila_gestor(
    status: str = None,
    nivel: str = None
):

    try:
        denuncias = filtrar_denuncias(
            status=status,
            nivel=nivel
        )
        return {
            "total": len(denuncias),
            "filtros": {
                "status": status,
                "nivel": nivel
            },
            "denuncias": denuncias
        }

    except Exception as erro:

        return JSONResponse(
            status_code=500,
            content={
                "erro": str(erro)
            }
        )

# BUSCAR DENÚNCIA PELO PROTOCOLO

@app.get("/denuncias/{protocolo}")
def obter_denuncia(
    protocolo: str
):

    try:
        denuncia = buscar_denuncia_por_protocolo(
            protocolo
        )

        if denuncia is None:
            return JSONResponse(
                status_code=404,
                content={
                    "erro":
                        "Denúncia não encontrada"
                }
            )
        return denuncia

    except Exception as erro:
        return JSONResponse(
            status_code=500,
            content={
                "erro": str(erro)
            }
        )

# ALTERAR STATUS

@app.put(
    "/denuncias/{protocolo}/status"
)
def alterar_status(
    protocolo: str,
    novo_status: str
):

    try:

        resultado = atualizar_status_denuncia(
            protocolo,
            novo_status
        )

        if resultado is None:
            return JSONResponse(
                status_code=404,
                content={
                    "erro":
                        "Denúncia não encontrada"
                }
            )

        return {
            "mensagem":
                "Status atualizado com sucesso",
            "protocolo":
                resultado["protocolo"],
            "status":
                resultado["status"]
        }

    except ValueError as erro:
        return JSONResponse(
            status_code=400,
            content={
                "erro": str(erro)
            }
        )

    except Exception as erro:
        return JSONResponse(
            status_code=500,
            content={
                "erro": str(erro)
            }
        )

# ANALISAR / CRIAR DENÚNCIA

@app.post("/analisar-denuncia")
async def analisar_denuncia(

    imagem: UploadFile = File(...),
    descricao: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    data_captura: str = Form(...)

):

    caminho_imagem = None

    try:

        # SALVAR IMAGEM TEMPORARIAMENTE

        extensao = Path(
            imagem.filename
        ).suffix

        nome_arquivo = (
            f"{uuid.uuid4()}{extensao}"
        )

        caminho_imagem = (
            PASTA_UPLOADS / nome_arquivo
        )

        with open(
            caminho_imagem,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                imagem.file,
                buffer
            )

        # YOLO

        resultados = model.predict(
            source=str(caminho_imagem),
            conf=0.25,
            verbose=False
        )

        melhor_classe = None
        melhor_confianca = 0

        deteccoes = []

        for resultado in resultados:

            for box in resultado.boxes:

                classe_id = int(
                    box.cls[0]
                )

                confianca = float(
                    box.conf[0]
                )

                classe = model.names[
                    classe_id
                ]

                deteccoes.append({
                    "classe": classe,
                    "confianca": round(
                        confianca,
                        4
                    )
                })

                if (
                    confianca
                    > melhor_confianca
                ):
                    melhor_confianca = (
                        confianca
                    )
                    melhor_classe = classe

        # CONTEXTO DA LOCALIZAÇÃO

        risco_contexto = (
            calcular_contexto_local(
                latitude,
                longitude,
                descricao
            )
        )

        # IPU

        resultado_ipu = calcular_ipu(

            classe_yolo=
                melhor_classe,

            confianca_yolo=
                melhor_confianca,

            texto=
                descricao,

            risco_contexto=
                risco_contexto
        )

        # GERAR PROTOCOLO

        protocolo = gerar_protocolo()

        # SALVAR IMAGEM PERMANENTEMENTE

        extensao_final = (
            caminho_imagem.suffix
        )

        nome_final = (
            f"{protocolo}"
            f"{extensao_final}"
        )

        caminho_final = (
            PASTA_IMAGENS
            / nome_final
        )

        shutil.move(
            str(caminho_imagem),
            str(caminho_final)
        )

        imagem_url = (
            f"/imagens/{nome_final}"
        )

        # CONVERTER DATA

        data_captura_convertida = (
            datetime.fromisoformat(
                data_captura
            )
        )

        # SALVAR NO POSTGRESQL

        salvar_denuncia(
            protocolo=
                protocolo,
            descricao=
                descricao,
            latitude=
                latitude,
            longitude=
                longitude,
            data_captura=
                data_captura_convertida,
            classe_yolo=
                resultado_ipu[
                    "classe_yolo"
                ],
            confianca_yolo=
                resultado_ipu[
                    "confianca_yolo"
                ],
            risco_imagem=
                resultado_ipu[
                    "risco_yolo"
                ],
            risco_texto=
                resultado_ipu[
                    "risco_texto"
                ],
            risco_contexto=
                resultado_ipu[
                    "risco_contexto"
                ],
            ipu=
                resultado_ipu[
                    "ipu"
                ],
            nivel=
                resultado_ipu[
                    "nivel"
                ],
            imagem_url=
                imagem_url
        )

        # RESPOSTA

        return JSONResponse(
            content={
                "protocolo":
                    protocolo,
                "status":
                    "Recebida",
                "descricao":
                    descricao,
                "data_captura":
                    data_captura,
                "imagem_url":
                    imagem_url,
                "localizacao": {
                    "latitude":
                        latitude,
                    "longitude":
                        longitude
                },
                "yolo": {
                    "classe_principal":
                        melhor_classe,
                    "confianca_principal":
                        round(
                            melhor_confianca,
                            4
                        ),
                    "deteccoes":
                        deteccoes
                },

                "analise_risco": {

                    "classe_considerada":
                        resultado_ipu[
                            "classe_yolo"
                        ],
                    "confianca_considerada":
                        resultado_ipu[
                            "confianca_yolo"
                        ],
                    "risco_imagem":
                        resultado_ipu[
                            "risco_yolo"
                        ],
                    "risco_texto":
                        resultado_ipu[
                            "risco_texto"
                        ],
                    "risco_contexto":
                        resultado_ipu[
                            "risco_contexto"
                        ],
                    "ipu":
                        resultado_ipu[
                            "ipu"
                        ],
                    "nivel":
                        resultado_ipu[
                            "nivel"
                        ]
                }
            }
        )


    except Exception as erro:
        return JSONResponse(
            status_code=500,
            content={
                "erro": str(erro)
            }
        )

    finally:
        if (
            caminho_imagem
            and caminho_imagem.exists()
        ):
            caminho_imagem.unlink()