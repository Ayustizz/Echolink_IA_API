import gspread
import pandas as pd
import os
import json 


gc = None
try:
    # 1. Intentar leer de la variable de entorno (para Render)
    credentials_json = os.environ.get("GOOGLE_CREDENTIALS")
    if credentials_json:
        # Cargar las credenciales JSON desde la variable de entorno
        credentials_dict = json.loads(credentials_json)
        gc = gspread.service_account_from_dict(credentials_dict)
        print("Google Sheets: Cliente inicializado desde variable de entorno.")
    else:
        # 2. Fallback: Intentar leer el archivo local (para desarrollo)
        gc = gspread.service_account(filename="credencial.json")
        print("Google Sheets: Cliente inicializado desde archivo local.")
except Exception as e:
    print(f"Error CRÍTICO al inicializar el cliente de Google Sheets: {e}")

def leer_encuestas_google(hoja_id):
    """
    Lee un Google Sheet por su ID y devuelve un DataFrame de pandas.
    """
    if gc is None:
        print("ERROR: Cliente de Google Sheets no inicializado. Devuelve DataFrame vacío.")
        return pd.DataFrame()

    try:
        sh = gc.open_by_key(hoja_id)
        worksheet = sh.sheet1  
        data = worksheet.get_all_records()

        if not data:
            return pd.DataFrame()

        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error al intentar leer la hoja {hoja_id}: {e}")
        return pd.DataFrame()