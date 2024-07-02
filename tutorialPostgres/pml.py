import psycopg2
import pandas as pd

# Parámetros de conexión a la base de datos
parametros_conexion = {
    "host": "ip",
    "database": "InformacionPublica",
    "user": "***",
    "password": "***"
}
try:
  # Conectarse a la base de datos
    conexion = psycopg2.connect(**parametros_conexion)

    # Definir la consulta SQL
    consulta_sql = """
        SELECT 
            tipo_de_mercado, clave_de_nodo, zona_horaria_entidad, 
            fecha_origen_utc, fecha_entidad_utc, fecha, hora, 
            pml_total, pml_congestion, pml_energia, pml_perdidas, 
            tipo_cambio, pml_total_usd, pml_congestion_usd, 
            pml_energia_usd, pml_perdidas_usd 
        FROM 
            public.preciosmarginaleslocales 
        WHERE 
            tipo_de_mercado = 'MDA' 
            AND clave_de_nodo = '04MNV-230' 
            AND fecha between '2023-05-01 00:00:00' and '2023-07-01 00:00:00'
    """
    
    # Cargar datos desde PostgreSQL a un DataFrame de Pandas
    df = pd.read_sql_query(consulta_sql, conexion)

    # Mostrar el DataFrame
    print(df)

except (Exception, psycopg2.Error) as error:
    print("Error al conectar a la base de datos PostgreSQL:", error)
finally:
    # Cerrar la conexión a la base de datos
    if 'conexion' in locals():
        conexion.close()
