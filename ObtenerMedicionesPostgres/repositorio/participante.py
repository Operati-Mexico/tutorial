import psycopg2
import pandas as pd
from datetime import datetime
import pytz
from util.constantes import PARAMETROS_CONEXION


class ParticipanteRepositorio():

    def __init__(self) -> None:
        self.parametros_conexion = {
            "host": PARAMETROS_CONEXION.HOST.value,
            "database": PARAMETROS_CONEXION.DATAB_BASE.value,
            "user": PARAMETROS_CONEXION.USER.value,
            "password": PARAMETROS_CONEXION.PASSWORD.value
        }

    def asignar_participante(self, participante) -> None :
        self.parametros_conexion["database"] = participante

    def obtener_timezone_id(self, clave_de_medidor) -> str :
        try:
            # Conectarse a la base de datos
            with psycopg2.connect(**self.parametros_conexion) as conexion:
                with conexion.cursor() as cursor:
                    # Definir la consulta SQL con parámetros
                    consulta_sql = "SELECT timezone_id FROM public.clavesdemedidor WHERE clave_de_medidor = %s"
                    # Ejecutar la consulta
                    cursor.execute(consulta_sql, (clave_de_medidor,))
                    # Obtener el valor
                    timezone = cursor.fetchone()
                    if timezone:
                        return timezone[0]
                    else:
                        print("No se encontraron resultados para la clave_de_medidor proporcionada.")
                        return None
        except (Exception, psycopg2.Error) as error:
            print("Error al conectar a la base de datos PostgreSQL:", error)
            return None
        
    def obtener_mediciones(self, clave_de_medicion, fecha_inicio, fecha_fin) -> pd.DataFrame:
        try:
            # Conectarse a la base de datos
            with psycopg2.connect(**self.parametros_conexion) as conexion:
                # Definir la consulta SQL con parámetros
                consulta_sql = """
                SELECT clave_de_medicion, clave_de_medidor, fecha AT TIME ZONE zona fecha,tipo, valor
                        FROM mediciones
                        WHERE clave_de_medicion = %s
                        AND fecha >= %s
                        AND fecha <= %s
                        ORDER BY id DESC
                """
                # Cargar datos desde PostgreSQL a un DataFrame de Pandas
                return pd.read_sql_query(consulta_sql, conexion, params=(clave_de_medicion, fecha_inicio, fecha_fin))                
        except (Exception, psycopg2.Error) as error:
            print("Error al conectar a la base de datos PostgreSQL:", error)

    def obtener_lista_medidores(self, clave_de_medidor=None) -> list:
        try:
            # Conectarse a la base de datos
            with psycopg2.connect(**self.parametros_conexion) as conexion:
                with conexion.cursor() as cursor:
                    # Definir la consulta SQL con parámetros
                    if clave_de_medidor:
                        consulta_sql = "SELECT clave_de_medidor FROM public.clavesdemedidor WHERE clave_de_medidor = %s"
                        # Ejecutar la consulta con el parámetro proporcionado
                        cursor.execute(consulta_sql, (clave_de_medidor,))
                    else:
                        consulta_sql = "SELECT clave_de_medidor FROM public.clavesdemedidor"
                        # Ejecutar la consulta sin parámetros
                        cursor.execute(consulta_sql)
                    
                    # Obtener todos los resultados
                    medidores = cursor.fetchall()
                    
                    # Extraer los resultados como una lista de claves de medidor
                    lista_medidores = [medidor[0] for medidor in medidores]
                    
                    return lista_medidores
        except (Exception, psycopg2.Error) as error:
            print("Error al conectar a la base de datos PostgreSQL:", error)
            return None


