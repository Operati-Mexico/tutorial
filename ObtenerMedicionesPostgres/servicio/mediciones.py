from util.utl_fechas import convertir_fecha
from datetime import datetime, timedelta

from repositorio.participante import ParticipanteRepositorio
import pandas as pd

class MedicionesServicio:

    def __init__(self) -> None:
        self.repo = ParticipanteRepositorio()

    def _obtener_mediciones_para_medidores(self, tipo_medidion, lista_medidores, fecha_inicio_dt, fecha_fin_dt):
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
                    df_combined = pd.concat([df_combined, resultado], ignore_index=True)
        return df_combined

    def obtener_mediciones_todos_medidores(self, participante, tipo_medicion, fecha_inicio_dt, fecha_fin_dt):
        self.repo.asignar_participante(participante)
        lista_medidores = self.repo.obtener_lista_medidores()
        return self._obtener_mediciones_para_medidores(tipo_medicion, lista_medidores, fecha_inicio_dt, fecha_fin_dt)

    def obtener_mediciones_por_medidores(self, participante, tipo_medidion, lista_medidores, fecha_inicio_dt, fecha_fin_dt):        
        self.repo.asignar_participante(participante)
        return self._obtener_mediciones_para_medidores(tipo_medidion, lista_medidores, fecha_inicio_dt, fecha_fin_dt)
