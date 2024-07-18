from datetime import datetime
from servicio.mediciones import MedicionesServicio
from util.constantes import TIPO_MEDICION


fecha_inicio_dt = datetime(2024, 1, 24)
fecha_fin_dt = datetime(2024, 1, 26)
participante = "ACCIONA_G094"
lista_mdidores = ["MNVP1PB0C093020"]

serv = MedicionesServicio()
resultado = serv.obtener_mediciones_por_medidores(participante,TIPO_MEDICION.KWHE.value,lista_mdidores,fecha_inicio_dt,fecha_fin_dt)
resultado.to_csv("./resultado.csv")


resultado = serv.obtener_mediciones_todos_medidores(participante,TIPO_MEDICION.KWHE.value,fecha_inicio_dt,fecha_fin_dt)
resultado.to_csv("./resultado_todos.csv")





