# ============================================================
#  📦 API IA_Echolinks v3 (segura con API Key)
#  - Analiza encuestas desde Google Sheets
#  - Analiza CVs nuevos sin mezclar con anteriores
#  - Guarda resultados históricos
#  - Protegida con x-api-key
# ============================================================

from flask import Flask, request, jsonify
from encuesta import analizar_encuestas_google
from cvs import procesar_carpeta_cvs
import os
import pandas as pd

# ------------------------------------------------------------
# 1️⃣ Configuración base
# ------------------------------------------------------------
app = Flask(__name__)

# ID de la hoja de Google Sheets (reemplaza por la tuya si cambia)
HOJA_ID = "1zTXTBLeewcL-ENbh_W1zvbBaTZbnp9yT7hQFmp4xJdc"

# Carpeta temporal donde se guardan los CVs subidos
CARPETA_CVS = "cvs"
os.makedirs(CARPETA_CVS, exist_ok=True)
app.config["UPLOAD_FOLDER"] = CARPETA_CVS

# Clave secreta de la API (puede configurarse en Render o usar valor por defecto)
API_KEY = os.environ.get("API_KEY", "clave-secreta")


# ------------------------------------------------------------
# 2️⃣ Middleware de autenticación
# ------------------------------------------------------------
def requiere_api_key(func):
    """Verifica que la solicitud incluya la clave correcta en los encabezados."""
    def wrapper(*args, **kwargs):
        clave = request.headers.get("x-api-key")
        if clave != API_KEY:
            return jsonify({"estado": "error", "mensaje": "Acceso no autorizado"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# ------------------------------------------------------------
# 3️⃣ Endpoint de prueba
# ------------------------------------------------------------
@app.route('/api/saludo', methods=['GET'])
def saludo():
    """Verifica que la API esté en funcionamiento."""
    return jsonify({"mensaje": "✅ API IA_Echolinks funcionando correctamente"}), 200


# ------------------------------------------------------------
# 4️⃣ Endpoint para obtener estadísticas de encuestas
# ------------------------------------------------------------
@app.route('/api/estadisticas', methods=['GET'])
@requiere_api_key
def obtener_estadisticas():
    """Conecta con Google Sheets y obtiene resultados reales."""
    try:
        resultados = analizar_encuestas_google(HOJA_ID)
        return jsonify({
            "estado": "exito",
            "fuente": "Google Sheets",
            "resultados": resultados
        }), 200
    except Exception as e:
        return jsonify({
            "estado": "error",
            "mensaje": f"Ocurrió un error al analizar las encuestas: {str(e)}"
        }), 500


# ------------------------------------------------------------
# 5️⃣ Endpoint para subir CVs nuevos y analizarlos
# ------------------------------------------------------------
@app.route('/api/subir_cv', methods=['POST'])
@requiere_api_key
def subir_cv():
    """
    Recibe uno o varios CVs PDF.
    Analiza solo los nuevos, los guarda en resultados_cvs.csv
    y devuelve únicamente los resultados de los CVs recién subidos.
    """
    try:
        if 'cv' not in request.files:
            return jsonify({"estado": "error", "mensaje": "No se enviaron archivos"}), 400

        archivos = request.files.getlist('cv')
        if not archivos:
            return jsonify({"estado": "error", "mensaje": "No se recibió ningún archivo"}), 400

        # 1️⃣ Limpiamos la carpeta para evitar combinar con anteriores
        for f in os.listdir(CARPETA_CVS):
            os.remove(os.path.join(CARPETA_CVS, f))

        # 2️⃣ Guardamos los nuevos CVs
        for archivo in archivos:
            ruta = os.path.join(app.config["UPLOAD_FOLDER"], archivo.filename)
            archivo.save(ruta)

        # 3️⃣ Procesamos los CVs nuevos
        resultados_nuevos = procesar_carpeta_cvs(CARPETA_CVS)

        # 4️⃣ Guardamos resultados en un CSV histórico
        historial_path = "resultados_cvs.csv"
        df_nuevos = pd.DataFrame(resultados_nuevos)

        if os.path.exists(historial_path):
            df_historial = pd.read_csv(historial_path)
            df_combinado = pd.concat([df_historial, df_nuevos], ignore_index=True)
        else:
            df_combinado = df_nuevos

        df_combinado.to_csv(historial_path, index=False)

        # 5️⃣ Devolvemos solo los resultados nuevos
        return jsonify({
            "estado": "exito",
            "mensaje": f"{len(archivos)} CV(s) analizado(s) correctamente.",
            "resultados_nuevos": resultados_nuevos
        }), 200

    except Exception as e:
        return jsonify({
            "estado": "error",
            "mensaje": f"Error al procesar los CVs: {str(e)}"
        }), 500


# ------------------------------------------------------------
# 6️⃣ Ejecutar el servidor
# ------------------------------------------------------------
if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    print(f"🚀 Servidor iniciado en el puerto {puerto}")
    app.run(host="0.0.0.0", port=puerto)
