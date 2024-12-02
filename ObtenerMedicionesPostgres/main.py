from datetime import datetime
from servicio.mediciones import MedicionesServicio
from util.constantes import TIPO_MEDICION,PARTICIPANTE,MODALIDAD,TIMEZONE


fecha_inicio_dt = datetime(2024, 10, 1)
fecha_fin_dt = datetime(2024, 11, 20)
participante = PARTICIPANTE.ACCIONA_C035
lista_mdidores = ["580921054323X"]
tipo_medicion = TIPO_MEDICION.KWHE
modalidad = MODALIDAD.HORARIO
timezone = TIMEZONE.ESTADO_DE_CUENTA
serv = MedicionesServicio()
resultado = serv.obtener_mediciones_por_medidores(participante,tipo_medicion,lista_mdidores,fecha_inicio_dt,fecha_fin_dt,modalidad,timezone)
resultado.to_csv("./resultado.csv")


resultado = serv.obtener_mediciones_todos_medidores(participante,tipo_medicion,fecha_inicio_dt,fecha_fin_dt,modalidad,timezone)
resultado.to_csv("./resultado_todos.csv")





