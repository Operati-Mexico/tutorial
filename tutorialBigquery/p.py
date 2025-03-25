from google.cloud import bigquery
import credentials
import pandas as pd
import datetime
import pandas_gbq
from google.cloud import bigquery
import numpy as np
import io
import os
import pyarrow as pa

def cargar_archivo_como_bytes(ruta_archivo):
        """
        Carga un archivo desde la ruta especificada y lo convierte en un arreglo de bytes.

        :param ruta_archivo: Ruta del archivo a leer.
        :return: Contenido del archivo en formato bytes, o None si el archivo no existe.
        """
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, "rb") as archivo:
                archivo_en_bytes = archivo.read()
            print("Archivo cargado y convertido a bytes exitosamente.")
            return archivo_en_bytes
        else:
            print("El archivo no existe en la ruta especificada.")
            return None

def replace_column_names(df, replacements):
    # Generar un diccionario de reemplazos
    column_replacements = {col: col.translate(str.maketrans(replacements)) for col in df.columns}

    # Reemplazar los nombres de columna
    df = df.rename(columns=column_replacements)

    return df

try:
    print("Descarga el archivo como objeto de BytesIO")        
    file_bytes = cargar_archivo_como_bytes('./Historico_ASV.csv')
    print("Convierte los bytes en una cadena utilizando io.StringIO")        
    file_string = file_bytes.decode('utf-8')
    file_io = io.StringIO(file_string)
    print("Lee el archivo utilizando pandas")
    df = pd.read_csv(file_io)  #modifica     
        
    # Define the correct date format
    date_format = "%d/%m/%Y %H:%M"
    df["Fecha"] = pd.to_datetime(df["Fecha"], format = date_format) 
    character_replacements = {
            ' ': '_',    
            '(': '',     
            ')': '',     
            '/': '_', 
            '-': '_',     
            '$': '_'     
        }
    df = replace_column_names(df, character_replacements)
    conversiones = {
    'Produccion_MWh': 'float64',
    'Producible_MWh': 'float64',
    'Consigna_MWh': 'float64',
    'MDAenviado_MWh': 'float64',
    'MDAcasado_MWh': 'float64',
    'RestMDA_MWh': 'float64',
    'AUGCenviado_MWh': 'float64',
    'AUGCcasado_MWh': 'float64',
    'RestAUGC_MWh': 'float64',
    'Limitacion_MWh': 'float64',
    'Vertido_MWh': 'float64',
    'GenLib_Recuperacion': 'int64',
    'MTR_Recuperacion': 'float64',
    'AUGC_Recuperacion': 'float64',
    'Factor_MDA': 'float64',
    'Factor_AUGC': 'float64'
    }
    df = df.astype(conversiones)

    print(df.head(10))
    print(df.dtypes)

    table_id = "acciona-info-privada.ACCIONA_ZONA_TRABAJO.produccion-mexico-centroamerica" # se modifica
    client = bigquery.Client.from_service_account_json(credentials.path_to_service_account_key_file)
    
    #Esta tabla es la que se subiría a la base de datos con la que se actualizar
    pandas_gbq.to_gbq(df, table_id, project_id=client.project, if_exists='append', credentials=client._credentials)

except Exception as e:
    print(f'Error al leer el archivo -> {str(e)}')
