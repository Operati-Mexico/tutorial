import psycopg2
import pandas as pd
from datetime import datetime
import pytz
from util.constantes import PARAMETROS_CONEXION
from google.cloud import bigquery


class ParticipanteRepositorio():
    
    def __init__(self) -> None:                            
        self.bqclient = bigquery.Client.from_service_account_json(PARAMETROS_CONEXION.PATH_TO_SERVICE_ACCOUNT_KEY_FILE.value)   
        self.parametros_conexion = {            
            "dataset_id": PARAMETROS_CONEXION.DATASET_ID.value,
            "database": PARAMETROS_CONEXION.DATAB_BASE.value,
        }    

    def asignar_participante(self, participante) -> None :
        self.parametros_conexion["database"] = participante

    def obtener_timezone_id(self, clave_de_medidor) -> str :
        try:
            # Crear el cliente de BigQuery
            cliente_bq = self.bqclient 

            # Definir la consulta SQL con parámetros
            consulta_sql = """
            SELECT TimezoneID
            FROM `"""+self.parametros_conexion["dataset_id"]+"""."""+self.parametros_conexion["database"] +""".ClavesDeMedidor`
            WHERE ClavedeMedidor = @clave_de_medidor
            """

            # Configurar los parámetros de la consulta
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("clave_de_medidor", "STRING", clave_de_medidor)
                ]
            )

            # Ejecutar la consulta
            resultado = cliente_bq.query(consulta_sql, job_config=job_config).result()

            # Obtener el valor del resultado
            for fila in resultado:
                return fila["TimezoneID"]

            # Si no se encuentran resultados, devolver None
            print("No se encontraron resultados para la ClavedeMedidor proporcionada.")
            return None

        except Exception as error:
            print("Error al conectar a BigQuery:", error)
            return None
    
    def obtener_timezone_id_cc(self, clave_de_medidor) -> str:
        try:
            # Crear el cliente de BigQuery
            cliente_bq = self.bqclient 

            # Definir la consulta SQL con parámetros
            consulta_sql = """
            SELECT TimezoneID_CC
            FROM `"""+self.parametros_conexion["dataset_id"]+"""."""+self.parametros_conexion["database"] +""".ClavesDeMedidor`
            WHERE ClavedeMedidor = @clave_de_medidor
            """

            # Configurar los parámetros de la consulta
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("clave_de_medidor", "STRING", clave_de_medidor)
                ]
            )

            # Ejecutar la consulta
            resultado = cliente_bq.query(consulta_sql, job_config=job_config).result()

            # Obtener el valor del resultado
            for fila in resultado:
                return fila["TimezoneID_CC"]

            # Si no se encuentran resultados, devolver None
            print("No se encontraron resultados para la clave_de_medidor proporcionada.")
            return None

        except Exception as error:
            print("Error al conectar a BigQuery:", error)
            return None
        
    def obtener_mediciones(self, clave_de_medicion, fecha_inicio, fecha_fin) -> pd.DataFrame:
        try:
            # Crear el cliente de BigQuery
            cliente_bq = self.bqclient 

            # Definir la consulta SQL con parámetros
            consulta_sql = """
            SELECT ClavedeMedidor as clave_de_medidor, ClavedeMedicion as clave_de_medicion, 
                Tipo as tipo, Fecha as fecha, Valor as valor
            FROM `"""+self.parametros_conexion["dataset_id"]+"""."""+self.parametros_conexion["database"] +""".Mediciones`
            WHERE ClavedeMedicion = @clave_de_medicion
            AND FechaTimeStamp >= @fecha_inicio
            AND FechaTimeStamp <= @fecha_fin
            ORDER BY id ASC
            """

            # Configurar los parámetros de la consulta
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("clave_de_medicion", "STRING", clave_de_medicion),
                    bigquery.ScalarQueryParameter("fecha_inicio", "TIMESTAMP", fecha_inicio),
                    bigquery.ScalarQueryParameter("fecha_fin", "TIMESTAMP", fecha_fin),
                ]
            )

            # Ejecutar la consulta y obtener los resultados
            resultado = cliente_bq.query(consulta_sql, job_config=job_config).result()

            # Convertir los resultados a un DataFrame de pandas
            df = resultado.to_dataframe()

            return df

        except Exception as error:
            print("Error al conectar a BigQuery:", error)
            return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error
    
    def obtener_lista_medidores(self, clave_de_medidor=None) -> list:
        try:
            # Crear el cliente de BigQuery
            cliente_bq = self.bqclient 

            # Definir la consulta SQL con parámetros
            if clave_de_medidor:
                consulta_sql = """
                SELECT ClavedeMedidor
                FROM `"""+self.parametros_conexion["dataset_id"]+"""."""+self.parametros_conexion["database"] +""".ClavesDeMedidor`
                WHERE ClavedeMedidor = @clave_de_medidor
                """
                # Configurar el parámetro de la consulta
                job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter("ClavedeMedidor", "STRING", clave_de_medidor)
                    ]
                )
            else:
                consulta_sql = """
                SELECT ClavedeMedidor
                FROM `"""+self.parametros_conexion["dataset_id"]+"""."""+self.parametros_conexion["database"] +""".ClavesDeMedidor`
                """
                job_config = None  # No hay parámetros si no se proporciona una clave_de_medidor

            # Ejecutar la consulta
            resultado = cliente_bq.query(consulta_sql, job_config=job_config).result()

            # Convertir los resultados a una lista de claves de medidor
            lista_medidores = [fila["ClavedeMedidor"] for fila in resultado]

            return lista_medidores

        except Exception as error:
            print("Error al conectar a BigQuery:", error)
            return None