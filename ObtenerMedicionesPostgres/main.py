from datetime import datetime
from servicio.mediciones import MedicionesServicio
from util.constantes import TIPO_MEDICION,PARTICIPANTE,MODALIDAD


fecha_inicio_dt = datetime(2024, 1, 24)
fecha_fin_dt = datetime(2024, 1, 25)
participante = PARTICIPANTE.ACCIONA_G094.value
lista_mdidores = ["MNVP1PB0C093020"]
tipo_medicion = TIPO_MEDICION.KWHE
modalidad = MODALIDAD.HORARIO

serv = MedicionesServicio()
resultado = serv.obtener_mediciones_por_medidores(participante,tipo_medicion,lista_mdidores,fecha_inicio_dt,fecha_fin_dt,modalidad)
resultado.to_csv("./resultado.csv")


resultado = serv.obtener_mediciones_todos_medidores(participante,tipo_medicion,fecha_inicio_dt,fecha_fin_dt,modalidad)
resultado.to_csv("./resultado_todos.csv")





