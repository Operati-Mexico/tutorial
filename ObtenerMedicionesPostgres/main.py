from datetime import datetime
from servicio.mediciones import MedicionesServicio
from util.constantes import TIPO_MEDICION,PARTICIPANTE,MODALIDAD,TIMEZONE


fecha_inicio_dt = datetime(2024, 7, 30)
fecha_fin_dt = datetime(2024, 7, 30)
participante = PARTICIPANTE.ACCIONA_C035
lista_mdidores = ["PIHPB0C073D90"]
tipo_medicion = TIPO_MEDICION.KWHE
modalidad = MODALIDAD.HORARIO
timezone = TIMEZONE.CENTROCARGA

serv = MedicionesServicio()
resultado = serv.obtener_mediciones_por_medidores(participante,tipo_medicion,lista_mdidores,fecha_inicio_dt,fecha_fin_dt,modalidad,timezone)
resultado.to_csv("./resultado.csv")


resultado = serv.obtener_mediciones_todos_medidores(participante,tipo_medicion,fecha_inicio_dt,fecha_fin_dt,modalidad,timezone)
resultado.to_csv("./resultado_todos.csv")





