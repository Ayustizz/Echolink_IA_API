import pandas as pd
from transformers import pipeline

# Cargar modelo
clasificador = pipeline("sentiment-analysis", model="finiteautomata/beto-sentiment-analysis")

# Leer tus encuestas locales
df = pd.read_csv("encuestas_empleados.csv", encoding="utf-8")

# Mostrar columnas
print("\n📌 Columnas detectadas:", df.columns.tolist())

# Elegir columna de respuestas (ajusta el nombre si es distinto)
columna = "respuesta" if "respuesta" in df.columns else df.columns[0]

# Tomar las primeras 10 respuestas
respuestas = df[columna].dropna().tolist()[:10]

print("\n📝 Ejemplos a clasificar:")
for r in respuestas:
    print("-", r)

# Clasificar
resultados = clasificador(respuestas)

print("\n🎯 Resultados:")
for r, pred in zip(respuestas, resultados):
    print(f"{r} --> {pred['label']} ({pred['score']:.2f})")
