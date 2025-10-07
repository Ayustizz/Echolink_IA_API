import gspread
import pandas as pd

# Cliente global con credenciales del service account
gc = gspread.service_account(filename="credencial.json")

def leer_encuestas_google(hoja_id):
    """
    Lee un Google Sheet por su ID y devuelve un DataFrame de pandas.

    Parámetros:
    - hoja_id (str): ID del documento (lo que aparece en la URL entre /d/ y /edit).

    Devuelve:
    - pd.DataFrame con los registros de la hoja 1.
    """
    sh = gc.open_by_key(hoja_id)
    worksheet = sh.sheet1  # primera pestaña
    data = worksheet.get_all_records()

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data)
