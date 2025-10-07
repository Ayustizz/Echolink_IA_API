from transformers import pipeline

# Crear clasificador con modelo preentrenado BETO
clasificador = pipeline("sentiment-analysis", model="finiteautomata/beto-sentiment-analysis")

print("\n✅ Modelo BETO cargado correctamente")
print("Ejemplo de prueba:")
print(clasificador("Me encanta trabajar aquí"))   # positivo
print(clasificador("No soporto a mi jefe"))       # negativo
print(clasificador("El ambiente está bien"))      # neutro
