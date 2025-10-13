import gspread
from google.oauth2.service_account import Credentials

def analizar_encuestas_google(hoja_id):
    """
    Conecta con Google Sheets, lee las respuestas y calcula estadísticas básicas.
    """
    alcances = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credenciales = Credentials.from_service_account_file('credencial.json', scopes=alcances)
    cliente = gspread.authorize(credenciales)

    hoja = cliente.open_by_key(hoja_id).sheet1
    filas = hoja.get_all_records()

    if not filas:
        return {"mensaje": "No hay respuestas en la hoja."}

    satisfacciones = [int(f["Satisfacción"]) for f in filas if f.get("Satisfacción")]
    promedio_satisfaccion = sum(satisfacciones) / len(satisfacciones)

    return {
        "total_respuestas": len(filas),
        "promedio_satisfaccion": round(promedio_satisfaccion, 2),
        "primer_comentario": filas[0].get("Comentario", "Sin comentarios") if filas else "Sin datos"
    }
