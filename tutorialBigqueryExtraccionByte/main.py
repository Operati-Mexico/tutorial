from google.cloud import bigquery
import credentials

# Crea el cliente de BigQuery
bqclient = bigquery.Client.from_service_account_json(credentials.path_to_service_account_key_file)

# Define la consulta para obtener los archivos
query = """
    SELECT id_archivo, nobrem_archivo, dato
    FROM info-publica-mem.Mercado.Archivos where id_archivo = 'e817cd3f-e0db-4491-a4de-fe2de2c7cdfa'
"""

# Ejecuta la consulta
query_job = bqclient.query(query)

# Itera sobre los resultados y guarda los archivos PDF
for row in query_job:
    id_archivo = row.id_archivo
    nombre_archivo = row.nobrem_archivo
    datos = row.dato

    # Asegúrate de que `datos` no sea None
    if datos:
        # Guardar los datos en un archivo PDF
        with open(nombre_archivo, 'wb') as pdf_file:
            pdf_file.write(datos)

        print(f"Archivo guardado: {nombre_archivo}")
