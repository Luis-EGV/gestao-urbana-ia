from banco import engine
from sqlalchemy import text
from datetime import datetime
import uuid


def gerar_protocolo():

    ano = datetime.now().year
    codigo = uuid.uuid4().hex[:8].upper()
    return f"URB-{ano}-{codigo}"


def salvar_denuncia(
    protocolo,
    descricao,
    latitude,
    longitude,
    data_captura,
    classe_yolo,
    confianca_yolo,
    risco_imagem,
    risco_texto,
    risco_contexto,
    ipu,
    nivel,
    imagem_url
):

    comando = text("""
        INSERT INTO denuncias (
            protocolo,
            descricao,
            latitude,
            longitude,
            data_captura,
            classe_yolo,
            confianca_yolo,
            risco_imagem,
            risco_texto,
            risco_contexto,
            ipu,
            nivel,
            status,
            imagem_url
        )
        VALUES (
            :protocolo,
            :descricao,
            :latitude,
            :longitude,
            :data_captura,
            :classe_yolo,
            :confianca_yolo,
            :risco_imagem,
            :risco_texto,
            :risco_contexto,
            :ipu,
            :nivel,
            'Recebida',
            :imagem_url
        )
    """)

    with engine.begin() as conexao:

        conexao.execute(
            comando,
            {
                "protocolo": protocolo,
                "descricao": descricao,
                "latitude": latitude,
                "longitude": longitude,
                "data_captura": data_captura,
                "classe_yolo": classe_yolo,
                "confianca_yolo": confianca_yolo,
                "risco_imagem": risco_imagem,
                "risco_texto": risco_texto,
                "risco_contexto": risco_contexto,
                "ipu": ipu,
                "nivel": nivel,
                "imagem_url": imagem_url
            }
        )
        
def listar_denuncias():

    comando = text("""
        SELECT
            id,
            protocolo,
            descricao,
            latitude,
            longitude,
            data_captura,
            data_envio,
            classe_yolo,
            confianca_yolo,
            risco_imagem,
            risco_texto,
            risco_contexto,
            ipu,
            nivel,
            status,
            imagem_url
        FROM denuncias
        ORDER BY ipu DESC, data_envio ASC
    """)

    with engine.connect() as conexao:

        resultado = conexao.execute(comando)

        denuncias = []

        for linha in resultado.mappings():

            denuncias.append({
                "id": linha["id"],
                "protocolo": linha["protocolo"],
                "descricao": linha["descricao"],
                "latitude": linha["latitude"],
                "longitude": linha["longitude"],
                "data_captura": (
                    linha["data_captura"].isoformat()
                    if linha["data_captura"]
                    else None
                ),
                "data_envio": (
                    linha["data_envio"].isoformat()
                    if linha["data_envio"]
                    else None
                ),
                "classe_yolo": linha["classe_yolo"],
                "confianca_yolo": (
                    float(linha["confianca_yolo"])
                    if linha["confianca_yolo"] is not None
                    else None
                ),
                "risco_imagem": (
                    float(linha["risco_imagem"])
                    if linha["risco_imagem"] is not None
                    else None
                ),
                "risco_texto": (
                    float(linha["risco_texto"])
                    if linha["risco_texto"] is not None
                    else None
                ),
                "risco_contexto": (
                    float(linha["risco_contexto"])
                    if linha["risco_contexto"] is not None
                    else None
                ),
                "ipu": (
                    float(linha["ipu"])
                    if linha["ipu"] is not None
                    else None
                ),
                "nivel": linha["nivel"],
                "status": linha["status"],
                "imagem_url": linha["imagem_url"]
            })

        return denuncias
    
def buscar_denuncia_por_protocolo(protocolo):

    comando = text("""
        SELECT
            id,
            protocolo,
            descricao,
            latitude,
            longitude,
            data_captura,
            data_envio,
            classe_yolo,
            confianca_yolo,
            risco_imagem,
            risco_texto,
            risco_contexto,
            ipu,
            nivel,
            status,
            imagem_url
        FROM denuncias
        WHERE protocolo = :protocolo
    """)

    with engine.connect() as conexao:

        resultado = conexao.execute(
            comando,
            {
                "protocolo": protocolo
            }
        )

        linha = resultado.mappings().first()

        if linha is None:
            return None

        return {
            "id": linha["id"],
            "protocolo": linha["protocolo"],
            "descricao": linha["descricao"],
            "latitude": linha["latitude"],
            "longitude": linha["longitude"],

            "data_captura": (
                linha["data_captura"].isoformat()
                if linha["data_captura"]
                else None
            ),

            "data_envio": (
                linha["data_envio"].isoformat()
                if linha["data_envio"]
                else None
            ),

            "classe_yolo": linha["classe_yolo"],

            "confianca_yolo": (
                float(linha["confianca_yolo"])
                if linha["confianca_yolo"] is not None
                else None
            ),

            "risco_imagem": (
                float(linha["risco_imagem"])
                if linha["risco_imagem"] is not None
                else None
            ),

            "risco_texto": (
                float(linha["risco_texto"])
                if linha["risco_texto"] is not None
                else None
            ),

            "risco_contexto": (
                float(linha["risco_contexto"])
                if linha["risco_contexto"] is not None
                else None
            ),

            "ipu": (
                float(linha["ipu"])
                if linha["ipu"] is not None
                else None
            ),

            "nivel": linha["nivel"],
            "status": linha["status"],
            "imagem_url": linha["imagem_url"]
        }

def atualizar_status_denuncia(protocolo, novo_status):

    status_permitidos = [
        "Recebida",
        "Em análise",
        "Em atendimento",
        "Resolvida"
    ]

    if novo_status not in status_permitidos:
        raise ValueError("Status inválido")

    comando = text("""
        UPDATE denuncias
        SET status = :novo_status
        WHERE protocolo = :protocolo
        RETURNING protocolo, status
    """)

    with engine.begin() as conexao:

        resultado = conexao.execute(
            comando,
            {
                "novo_status": novo_status,
                "protocolo": protocolo
            }
        )

        linha = resultado.mappings().first()

        if linha is None:
            return None

        return {
            "protocolo": linha["protocolo"],
            "status": linha["status"]
        }    

def filtrar_denuncias(status=None, nivel=None):

    comando_sql = """
        SELECT
            id,
            protocolo,
            descricao,
            latitude,
            longitude,
            data_captura,
            data_envio,
            classe_yolo,
            confianca_yolo,
            risco_imagem,
            risco_texto,
            risco_contexto,
            ipu,
            nivel,
            status,
            imagem_url
        FROM denuncias
        WHERE 1=1
    """

    parametros = {}

    if status:
        comando_sql += " AND status = :status"
        parametros["status"] = status

    if nivel:
        comando_sql += " AND nivel = :nivel"
        parametros["nivel"] = nivel

    comando_sql += " ORDER BY ipu DESC, data_envio ASC"

    comando = text(comando_sql)

    with engine.connect() as conexao:

        resultado = conexao.execute(
            comando,
            parametros
        )

        denuncias = []

        for linha in resultado.mappings():

            denuncias.append({
                "id": linha["id"],
                "protocolo": linha["protocolo"],
                "descricao": linha["descricao"],
                "latitude": linha["latitude"],
                "longitude": linha["longitude"],
                "data_captura": (
                    linha["data_captura"].isoformat()
                    if linha["data_captura"]
                    else None
                ),
                "data_envio": (
                    linha["data_envio"].isoformat()
                    if linha["data_envio"]
                    else None
                ),
                "classe_yolo": linha["classe_yolo"],
                "confianca_yolo": (
                    float(linha["confianca_yolo"])
                    if linha["confianca_yolo"] is not None
                    else None
                ),
                "ipu": (
                    float(linha["ipu"])
                    if linha["ipu"] is not None
                    else None
                ),
                "nivel": linha["nivel"],
                "status": linha["status"],
                "imagem_url": linha["imagem_url"]
            })

        return denuncias
    
def filtrar_denuncias(
    status=None,
    nivel=None
):

    filtros = []
    parametros = {}

    if status:
        filtros.append(
            "status = :status"
        )
        parametros["status"] = status

    if nivel:
        filtros.append(
            "nivel = :nivel"
        )
        parametros["nivel"] = nivel

    consulta = """
        SELECT
            id,
            protocolo,
            descricao,
            latitude,
            longitude,
            data_captura,
            data_envio,
            classe_yolo,
            confianca_yolo,
            risco_imagem,
            risco_texto,
            risco_contexto,
            ipu,
            nivel,
            status,
            imagem_url
        FROM denuncias
    """

    if filtros:
        consulta += (
            " WHERE "
            + " AND ".join(filtros)
        )

    # Mais prioritárias primeiro
    consulta += " ORDER BY ipu DESC"

    comando = text(consulta)

    with engine.connect() as conexao:

        resultado = conexao.execute(
            comando,
            parametros
        )

        denuncias = []

        for linha in resultado.mappings():

            denuncia = dict(linha)

            # Converte tipos do PostgreSQL
            # para tipos aceitos pelo JSON
            for campo, valor in denuncia.items():

                if isinstance(valor, datetime):
                    denuncia[campo] = (
                        valor.isoformat()
                    )

                elif hasattr(valor, "as_tuple"):
                    denuncia[campo] = float(
                        valor
                    )

            denuncias.append(
                denuncia
            )

        return denuncias