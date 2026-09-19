# Modelo de Inteligência Artificial

Esta pasta contém o modelo YOLO utilizado pelo Sistema de Gestão Urbana.

## Arquivo

```text
best.pt
```

Esse arquivo representa o modelo YOLOv8 treinado para análise das ocorrências urbanas.

## Importante

Não é necessário treinar novamente o modelo para executar a demonstração.

O FastAPI carrega automaticamente:

```text
modelo/best.pt
```

## Fluxo

```text
Imagem da ocorrência
        ↓
     YOLOv8
        ↓
    best.pt
        ↓
Classe identificada
        ↓
Confiança da detecção
        ↓
Cálculo de risco
```

O resultado da análise é utilizado junto com a descrição e o contexto da ocorrência para calcular o Índice de Prioridade Urbana (IPU).

## Treinamento

O arquivo disponibilizado é o modelo final utilizado na demonstração.

Os datasets e arquivos intermediários de treinamento não estão incluídos no repositório.
