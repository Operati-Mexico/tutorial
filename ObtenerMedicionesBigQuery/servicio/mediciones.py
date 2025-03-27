from decimal import Decimal, getcontext
from util.utl_fechas import convertir_fecha, obtener_rango_fechas, calcular_horas_del_dia
from datetime import datetime, timedelta
import pandas as pd
from util.constantes import TIPO_MEDICION,PARTICIPANTE,MODALIDAD,TIMEZONE
import pytz

from repositorio.participante import ParticipanteRepositorio
import pandas as pd

class MedicionesServicio:

    def __init__(self) -> None:
        self.repo = ParticipanteRepositorio()
        
    def _convertir_minutal_horario(self,resultado:pd.DataFrame):
        # Convertir la columna a formato datetime
        resultado['datetime_str_sliced'] = resultado['fecha'].str[:19]
        resultado['fecha'] = pd.to_datetime(resultado['datetime_str_sliced'])
        
        # Restar 5 minutos a la columna de fecha y hora
        resultado['fecha_restada'] = resultado['fecha'] - pd.Timedelta(minutes=5)
        # Redondear hacia abajo a la hora más cercana
        resultado['fecha_y_hora_redondeada'] = resultado['fecha_restada'].dt.floor('h')
        # Extraer solo la hora
        resultado['hora'] = resultado['fecha_y_hora_redondeada'].dt.hour        
        # Extraer solo la fecha
        resultado['fecha_solo'] = resultado['fecha_y_hora_redondeada'].dt.date
        # Agrupar por la columna modificada
        
        df_grouped = resultado.groupby(['clave_de_medicion','clave_de_medidor','fecha_solo', 'hora'])['valor'].sum().reset_index()
        
        # Renombrar la columna 'fecha' para mayor claridad
        df_grouped.rename(columns={'fecha_solo': 'fecha'}, inplace=True)
        return df_grouped
    
   
    def _convertir_minutal_horario_sumada(self,resultado:pd.DataFrame):
        resultado['hora'] = resultado['hora'] + 1
        resultado['valor'] = resultado['valor'].round(6)

        return resultado
    
    def _convertir_minutal_horario_conteo(self,resultado:pd.DataFrame):
        # Contador
        resultado['contador'] = range(1, len(resultado) + 1)
        # Renombrar la columna 'fecha' para mayor claridad
        resultado = resultado.drop(columns=['hora'])
        # Renombrar la columna 'fecha' para mayor claridad
        resultado.rename(columns={'contador': 'hora'}, inplace=True)
        resultado['valor'] = resultado['valor'].round(6)

        return resultado

    def _obtener_mediciones_para_medidores(self, tipo_medidion, lista_medidores, fecha_inicio_dt, fecha_fin_dt, tipo:MODALIDAD,timezone:TIMEZONE):
        cinco_minutos = timedelta(minutes=5)
        un_dia = timedelta(days=1)
        fecha_inicio_dt = fecha_inicio_dt + cinco_minutos
        fecha_fin_dt = fecha_fin_dt + un_dia

        df_combined = pd.DataFrame()
        for medidor in lista_medidores:            
            print(medidor)
            clave_de_medicion = medidor + tipo_medidion
            if timezone.value == TIMEZONE.CC.value:
                df_combined = self._obtener_medicio_por_timezone_cc(df_combined, medidor,fecha_inicio_dt,fecha_fin_dt,clave_de_medicion, tipo)
            
            if timezone.value == TIMEZONE.ESTADO_DE_CUENTA.value:
                df_combined = self._obtener_medicio_por_timezone_estado_cuenta(df_combined, medidor,fecha_inicio_dt,fecha_fin_dt,clave_de_medicion, tipo)

        return df_combined
    
    def _obtener_medicio_por_timezone_cc(self,df_combined, medidor,fecha_inicio_dt,fecha_fin_dt,clave_de_medicion, tipo):
        timezone_id = self.repo.obtener_timezone_id(medidor)
        if timezone_id:
            fecha_inicio = convertir_fecha(fecha_inicio_dt, timezone_id)
            fecha_fin = convertir_fecha(fecha_fin_dt, timezone_id)
           
            if fecha_inicio and fecha_fin:
                resultado = self.repo.obtener_mediciones(clave_de_medicion, fecha_inicio, fecha_fin)                            
                if(tipo == MODALIDAD.HORARIO):
                    resultado = self._convertir_minutal_horario(resultado)
                    resultado = self._convertir_minutal_horario_sumada(resultado)
                df_combined = pd.concat([df_combined, resultado], ignore_index=True)
        return df_combined
        
    
    def _obtener_medicio_por_timezone_estado_cuenta(self,df_combined, medidor,fecha_inicio_dt,fecha_fin_dt,clave_de_medicion, tipo):
        timezone_id = self.repo.obtener_timezone_id(medidor)        
        un_dia = timedelta(days=1)
        cinco_minutos = timedelta(minutes=5)
        if timezone_id:            
            rango =  obtener_rango_fechas(fecha_inicio_dt,fecha_fin_dt)
            for fecha in rango :                
                fecha2 = fecha+un_dia -cinco_minutos
                fecha_inicio = convertir_fecha(fecha, timezone_id)
                fecha_fin = convertir_fecha(fecha2, timezone_id)
                
                resultado = self.repo.obtener_mediciones(clave_de_medicion, fecha_inicio, fecha_fin)   
                if(tipo == MODALIDAD.HORARIO):
                    resultado = self._convertir_minutal_horario(resultado)                         
                    resultado = self._convertir_minutal_horario_conteo(resultado)                               
                
                if len(resultado) != 0:                                   
                    df_combined = pd.concat([df_combined, resultado], ignore_index=True)            
        return df_combined

    def obtener_mediciones_todos_medidores(self, participante:PARTICIPANTE, tipo_medicion:TIPO_MEDICION, fecha_inicio_dt, fecha_fin_dt,modalidad:MODALIDAD,timezone:TIMEZONE):
        self.repo.asignar_participante(participante.value)
        lista_medidores = self.repo.obtener_lista_medidores(fecha_inicio_dt, fecha_fin_dt)
        return self._obtener_mediciones_para_medidores(tipo_medicion.value, lista_medidores, fecha_inicio_dt, fecha_fin_dt,modalidad,timezone)

    def obtener_mediciones_por_medidores(self, participante:PARTICIPANTE, tipo_medidion:TIPO_MEDICION, lista_medidores, fecha_inicio_dt, fecha_fin_dt,modalidad:MODALIDAD,timezone:TIMEZONE):        
        self.repo.asignar_participante(participante.value)
        return self._obtener_mediciones_para_medidores(tipo_medidion.value, lista_medidores, fecha_inicio_dt, fecha_fin_dt,modalidad,timezone)
