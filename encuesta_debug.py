from google_utils import leer_encuestas_google

# 👉 Reemplaza por el ID real de tu Google Sheet
HOJA_ID = "1zTXTBLeewcL-ENbh_W1zvbBaTZbnp9yT7hQFmp4xJdc"

def debug_encuesta():
    df = leer_encuestas_google(HOJA_ID)
    if df.empty:
        print("⚠️ No se pudo leer nada desde la hoja de Google.")
        return

    print("\n📊 Columnas detectadas en la hoja:")
    print(df.columns.tolist())

    print("\n🔎 Primeras filas de la hoja:")
    print(df.head())

if __name__ == "__main__":
    debug_encuesta()
