import pdfplumber, re, unicodedata, os
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"
EMB_MODEL = SentenceTransformer(MODEL_NAME)

DESCRIPCION_PUESTO = """
Buscamos programador Python con experiencia en javascript.
"""

SKILLS = ["python","django","sql","javascript","react","git","comunicativo","puntual","responsable"]

def extraer_texto_cv(ruta_pdf):
    texto = ""
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            for pagina in pdf.pages:
                t = pagina.extract_text()
                if t:
                    texto += t + "\n"
    except Exception as e:
        print(f"Error al leer {ruta_pdf}: {e}")
    return texto if texto.strip() else " "

def preprocess_text(s):
    s = s or ""
    s = s.lower()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join([c for c in s if not unicodedata.combining(c)])
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    return s

def extraer_skills(texto):
    t = preprocess_text(texto)
    return [skill for skill in SKILLS if skill in t]

def procesar_cv(filepath):
    texto_cv = extraer_texto_cv(filepath)
    texto_cv_proc = preprocess_text(texto_cv)
    desc_proc = preprocess_text(DESCRIPCION_PUESTO)
    emb_cv = EMB_MODEL.encode(texto_cv_proc, convert_to_tensor=True)
    emb_desc = EMB_MODEL.encode(desc_proc, convert_to_tensor=True)
    simil = util.cos_sim(emb_cv, emb_desc).item()
    skills = extraer_skills(texto_cv)
    return {'archivo': os.path.basename(filepath), 'similitud': round(float(simil)*100,2), 'skills': skills}

def procesar_carpeta_cvs(carpeta):
    resultados = []
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(".pdf"):
            ruta = os.path.join(carpeta, archivo)
            resultado = procesar_cv(ruta)
            resultados.append(resultado)

    # Ordenar por similitud (mayor a menor)
    resultados_ordenados = sorted(resultados, key=lambda x: x['similitud'], reverse=True)

    # Devolver solo los 10 mejores (puedes cambiarlo)
    return resultados_ordenados[:10]
