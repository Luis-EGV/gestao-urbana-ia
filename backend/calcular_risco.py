def risco_texto(texto):
    texto = texto.lower()

    score = 0

    regras = {
        "árvore caída": 70,
        "arvore caída": 70,
        "árvore caiu": 70,
        "galho caiu": 45,
        "bloqueando a rua": 30,
        "bloqueou a avenida": 35,

        "esgoto": 35,
        "vazamento": 35,
        "ralo transbordando": 45,
        "água suja": 30,
        "mau cheiro": 20,

        "buraco": 30,
        "buraco grande": 50,
        "risco de acidente": 45,

        "alagamento": 50,
        "rua alagada": 55,
        "carro preso": 40,

        "lixo acumulado": 25,
        "muito lixo": 30,

        "poste apagado": 35,
        "sem iluminação": 35,
        "fio exposto": 60,
        "risco de choque": 70,

        "hospital": 30,
        "escola": 25,
        "creche": 25,
        "avenida": 15
    }

    for termo, peso in regras.items():
        if termo in texto:
            score += peso

    return min(score, 100)


def risco_yolo(classe, confianca):
    pesos = {
        "buraco": 60,
        "galho_caido": 70,
        "alagamento": 80,
        "lixo_acumulado": 40,
        "esgoto": 60,
        "poste_semluz": 45
    }

    if classe is None:
        return 0

    peso = pesos.get(classe, 30)

    return min(peso * confianca, 100)


def ajustar_consistencia(classe, confianca, texto):
    texto = texto.lower()

    if classe == "esgoto":
        palavras_esgoto = [
            "esgoto",
            "vazamento",
            "ralo",
            "água suja",
            "mau cheiro",
            "transbordando"
        ]

        confirmou = any(
            palavra in texto
            for palavra in palavras_esgoto
        )

        if not confirmou:
            confianca *= 0.4

    # compensar possível falha do YOLO.
    if any(termo in texto for termo in [
        "árvore caída",
        "arvore caída",
        "árvore caiu",
        "arvore caiu",
        "tronco na pista"
    ]):
        if classe is None:
            classe = "galho_caido"
            confianca = 0.60

    return classe, confianca

# risco base
def calcular_risco_contexto(texto, latitude=None, longitude=None):
    texto = texto.lower()

    score = 20  

    locais_sensiveis = {
        "hospital": 30,
        "upa": 30,
        "escola": 25,
        "creche": 25,
        "posto de saúde": 25,
        "avenida": 20,
        "rodovia": 25,
        "ponte": 25,
        "ponto de ônibus": 15,
        "terminal": 20,
        "praça": 10
    }

    fatores_perigo = {
        "bloqueando": 20,
        "bloqueou": 20,
        "acidente": 25,
        "risco de acidente": 30,
        "criança": 15,
        "idoso": 10,
        "muito movimento": 15,
        "trânsito intenso": 20
    }

    for termo, peso in locais_sensiveis.items():
        if termo in texto:
            score += peso

    for termo, peso in fatores_perigo.items():
        if termo in texto:
            score += peso

    # Depois verificar proximidade real de locais sensíveis.

    return min(score, 100)

def calcular_ipu(classe_yolo, confianca_yolo, texto, risco_contexto):

    classe_yolo, confianca_yolo = ajustar_consistencia(
        classe_yolo,
        confianca_yolo,
        texto
    )

    score_yolo = risco_yolo(
        classe_yolo,
        confianca_yolo
    )

    score_texto = risco_texto(texto)

    ipu = (
        score_yolo * 0.35 +
        score_texto * 0.40 +
        risco_contexto * 0.25
    )

    ipu = round(min(ipu, 100), 2)

    if ipu < 40:
        nivel = "Mediano"
    elif ipu < 65:
        nivel = "Perigoso"
    else:
        nivel = "Risco"

    return {
        "classe_yolo": classe_yolo,
        "confianca_yolo": round(confianca_yolo, 2),
        "risco_yolo": round(score_yolo, 2),
        "risco_texto": score_texto,
        "risco_contexto": risco_contexto,
        "ipu": ipu,
        "nivel": nivel
    }