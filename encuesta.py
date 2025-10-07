from google_utils import leer_encuestas_google
from transformers import pipeline
from collections import Counter

def analizar_encuestas_google(hoja_id):
    # Leer las respuestas desde Google Sheets
    df = leer_encuestas_google(hoja_id)
    if df.empty:
        return {'preguntas': [], 'resultados': []}

    # Filtrar columnas útiles
    columnas_validas = [
        c for c in df.columns
        if "marca temporal" not in c.lower() and not c.lower().startswith("columna")
    ]
    if not columnas_validas:
        return {'preguntas': [], 'resultados': []}

    # Crear modelo de análisis de sentimientos
    clasificador = pipeline("sentiment-analysis", model="finiteautomata/beto-sentiment-analysis")

    preguntas = []
    resultados = []

    for col in columnas_validas:
        respuestas = df[col].dropna().astype(str).tolist()
        if not respuestas:
            continue

        analisis = clasificador(respuestas)
        mapeo = {"POS": "positivo", "NEG": "negativo", "NEU": "neutro",
                 "positive": "positivo", "negative": "negativo", "neutral": "neutro"}
        etiquetas = [mapeo.get(a["label"], a["label"]) for a in analisis]
        conteo = Counter(etiquetas)

        preguntas.append(col)
        resultados.append(conteo)

    return {'preguntas': preguntas, 'resultados': resultados}
