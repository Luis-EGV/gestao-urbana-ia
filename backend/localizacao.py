import requests


def calcular_contexto_local(latitude, longitude, descricao=""):
    descricao = descricao.lower()

    # risco base
    score = 20

    # raio de busca em metros
    raio = 500

    query = f"""
    [out:json];

    (
      node(around:{raio},{latitude},{longitude})["amenity"="school"];
      way(around:{raio},{latitude},{longitude})["amenity"="school"];

      node(around:{raio},{latitude},{longitude})["amenity"="hospital"];
      way(around:{raio},{latitude},{longitude})["amenity"="hospital"];

      node(around:{raio},{latitude},{longitude})["amenity"="clinic"];
      way(around:{raio},{latitude},{longitude})["amenity"="clinic"];

      node(around:{raio},{latitude},{longitude})["amenity"="kindergarten"];
      way(around:{raio},{latitude},{longitude})["amenity"="kindergarten"];

      node(around:{raio},{latitude},{longitude})["highway"="bus_stop"];

      way(around:{raio},{latitude},{longitude})["highway"="primary"];
      way(around:{raio},{latitude},{longitude})["highway"="trunk"];
    );

    out tags center;
    """

    locais_encontrados = []

    try:
        resposta = requests.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": query},
            timeout=15
        )

        resposta.raise_for_status()

        dados = resposta.json()

        for elemento in dados.get("elements", []):
            tags = elemento.get("tags", {})

            amenity = tags.get("amenity")
            highway = tags.get("highway")

            if amenity == "school":
                locais_encontrados.append("escola")
                score += 25

            elif amenity == "hospital":
                locais_encontrados.append("hospital")
                score += 30

            elif amenity == "clinic":
                locais_encontrados.append("clinica")
                score += 20

            elif amenity == "kindergarten":
                locais_encontrados.append("creche")
                score += 25

            elif highway == "bus_stop":
                locais_encontrados.append("ponto_onibus")
                score += 10

            elif highway in ["primary", "trunk"]:
                locais_encontrados.append("via_importante")
                score += 20

    except Exception as erro:
        print(
            "Não foi possível consultar a localização:",
            erro
        )

    # Contexto informado pelo texto
    if "bloqueando" in descricao:
        score += 20

    if "risco de acidente" in descricao:
        score += 25

    if "avenida" in descricao:
        score += 15

    score = min(score, 100)

    return score