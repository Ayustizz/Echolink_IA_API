import pdfplumber
import os

def procesar_cv(ruta_cv):
    """Lee un CV PDF y devuelve un resumen simple."""
    texto = ""
    with pdfplumber.open(ruta_cv) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() or ""

    # Ejemplo básico: buscar palabras clave
    palabras_clave = ["Python", "Flask", "IA", "Machine Learning", "Django", "SQL"]
    conteo = {palabra: texto.lower().count(palabra.lower()) for palabra in palabras_clave}
    puntaje = sum(conteo.values()) * 10

    return {
        "archivo": os.path.basename(ruta_cv),
        "puntaje": puntaje,
        "palabras_clave": conteo
    }

def procesar_carpeta_cvs(carpeta):
    """Procesa todos los CVs PDF en la carpeta indicada."""
    resultados = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".pdf"):
            ruta = os.path.join(carpeta, archivo)
            resultados.append(procesar_cv(ruta))
    return resultados
