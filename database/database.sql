CREATE TABLE IF NOT EXISTS denuncias (
    id SERIAL PRIMARY KEY,

    protocolo VARCHAR(30) UNIQUE NOT NULL,

    descricao TEXT NOT NULL,

    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,

    data_captura TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    data_envio TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    classe_yolo VARCHAR(50),
    confianca_yolo NUMERIC(6,4),

    risco_imagem NUMERIC(6,2),
    risco_texto NUMERIC(6,2),
    risco_contexto NUMERIC(6,2),

    ipu NUMERIC(6,2),

    nivel VARCHAR(20),

    status VARCHAR(30) DEFAULT 'Recebida',

    imagem_url TEXT
);