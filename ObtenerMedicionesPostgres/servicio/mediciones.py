from util.utl_fechas import convertir_fecha
from datetime import timedelta
import pandas as pd
from util.constantes import TIPO_MEDICION,PARTICIPANTE,MODALIDAD

from repositorio.participante import ParticipanteRepositorio
import pandas as pd

class MedicionesServicio:

    def __init__(self) -> None:
        self.repo = ParticipanteRepositorio()
        
    def _convertir_minutal_horario(self,resultado:pd.DataFrame):
        # Convertir la columna a formato datetime
        resultado['fecha'] = pd.to_datetime(resultado['fecha'])
        # Restar 5 minutos a la columna de fecha y hora
        resultado['fecha_restada'] = resultado['fecha'] - pd.Timedelta(minutes=5)
        # Redondear hacia abajo a la hora más cercana
        resultado['fecha_y_hora_redondeada'] = resultado['fecha_restada'].dt.floor('h')
        # Extraer solo la hora
        resultado['hora'] = resultado['fecha_y_hora_redondeada'].dt.hour + 1
        # Extraer solo la fecha
        resultado['fecha_solo'] = resultado['fecha_y_hora_redondeada'].dt.date
        # Agrupar por la columna modificada
        # Agrupar por 'clave_de_medidor', 'fecha', y 'tipo' y sumar los valores
        df_grouped = resultado.groupby(['clave_de_medicion','clave_de_medidor','fecha_solo', 'hora','tipo'])['valor'].sum().reset_index()
        # Renombrar la columna 'fecha' para mayor claridad
        df_grouped.rename(columns={'fecha_solo': 'fecha'}, inplace=True)
        return df_grouped

    def _obtener_mediciones_para_medidores(self, tipo_medidion, lista_medidores, fecha_inicio_dt, fecha_fin_dt, tipo:MODALIDAD):
        cinco_minutos = timedelta(minutes=5)
        un_dia = timedelta(days=1)
        fecha_inicio_dt = fecha_inicio_dt + cinco_minutos
        fecha_fin_dt = fecha_fin_dt + un_dia

        df_combined = pd.DataFrame()
        for medidor in lista_medidores:
            clave_de_medicion = medidor + tipo_medidion
            timezone_id = self.repo.obtener_timezone_id(medidor)
            if timezone_id:
                fecha_inicio = convertir_fecha(fecha_inicio_dt, timezone_id)
                fecha_fin = convertir_fecha(fecha_fin_dt, timezone_id)
                if fecha_inicio and fecha_fin:
                    resultado = self.repo.obtener_mediciones(clave_de_medicion, fecha_inicio, fecha_fin)                            
                    if(tipo == MODALIDAD.HORARIO):
                        resultado = self._convertir_minutal_horario(resultado)
                    df_combined = pd.concat([df_combined, resultado], ignore_index=True)
        return df_combined

    def obtener_mediciones_todos_medidores(self, participante, tipo_medicion:TIPO_MEDICION, fecha_inicio_dt, fecha_fin_dt,modalidad:MODALIDAD):
        self.repo.asignar_participante(participante)
        lista_medidores = self.repo.obtener_lista_medidores()
        return self._obtener_mediciones_para_medidores(tipo_medicion.value, lista_medidores, fecha_inicio_dt, fecha_fin_dt,modalidad)

    def obtener_mediciones_por_medidores(self, participante, tipo_medidion:TIPO_MEDICION, lista_medidores, fecha_inicio_dt, fecha_fin_dt,modalidad:MODALIDAD):        
        self.repo.asignar_participante(participante)
        return self._obtener_mediciones_para_medidores(tipo_medidion.value, lista_medidores, fecha_inicio_dt, fecha_fin_dt,modalidad)
