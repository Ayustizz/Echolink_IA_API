from flask import Flask, render_template, request
from encuesta import analizar_encuestas_google
from cvs import procesar_cv, procesar_carpeta_cvs
import os

app = Flask(__name__)

# Carpeta para subir CVs
UPLOAD_FOLDER = "cvs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ID de la hoja de Google
HOJA_ID = "1zTXTBLeewcL-ENbh_W1zvbBaTZbnp9yT7hQFmp4xJdc"

# Página de inicio
@app.route('/')
def index():
    return render_template("index.html")

# Estadísticas de la encuesta
@app.route('/estadisticas')
def mostrar_estadisticas():
    resultados = analizar_encuestas_google(HOJA_ID)
    # PASAMOS zip al template
    return render_template("resultados.html", resultados=resultados, zip=zip)

# Subir CVs
@app.route('/subir_cv', methods=['GET', 'POST'])
def subir_cv():
    if request.method == 'POST':
        files = request.files.getlist('cv')  # aceptar múltiples archivos
        if files:
            for file in files:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
            top_resultados = procesar_carpeta_cvs(app.config['UPLOAD_FOLDER'])
            return render_template("Resultados_cv.html", resultados=top_resultados)
    return render_template("subir_cv.html")

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask en http://127.0.0.1:5000/")
    app.run(debug=True)
