from datetime import datetime, timedelta
import pytz


# Mapeo de nombres de zonas horarias comunes a los identificadores de pytz
timezone_mapping = {
    'Central Standard Time (Mexico)': 'America/Mexico_City',
    'US Mountain Standard Time': 'America/Hermosillo',    
    'Mountain Standard Time (Mexico)': 'America/Hermosillo',
    'America/Matamoros': 'America/Matamoros',
    # Agrega más mapeos según sea necesario
}


# Lógica personalizada para transformar las horas
def get_custom_hour(dt):
    hour = dt.hour
    if hour == 0:
        return 1
    elif hour == 12:
        return 13
    elif hour > 12:
        return hour + 1
    else:
        return hour + 1

def calcular_horas_del_dia(fecha: str, timezone_id: str ) -> int:
    """
    Calcula cuántas horas tiene un día específico basado en la zona horaria.
    
    :param fecha: Fecha en formato "YYYY-MM-DD HH:MM:SS±HH:MM"
    :param zona_horaria: Zona horaria como string, por defecto 'America/Mexico_City'
    :return: Número de horas del día (23, 24 o 25)
    """

    zona_horaria = timezone_mapping.get(timezone_id, timezone_id)

    print(fecha)
    print(zona_horaria)
    # Convertir la fecha de string a objeto de fecha
    dt = datetime.fromisoformat(fecha)

    # Inicializar la zona horaria
    tz = pytz.timezone(zona_horaria)
    dt_local = dt.astimezone(tz)  # Ajustar a la zona horaria local

    # Obtener el inicio y el final del día en la zona horaria local
    inicio_dia = tz.localize(datetime(dt_local.year, dt_local.month, dt_local.day, 0, 0, 0))
    fin_dia = inicio_dia + timedelta(days=1)

    # Restar los timestamps para obtener la duración real del día
    diferencia = (fin_dia - inicio_dia).total_seconds() / 3600

    # Devolver la cantidad de horas
    return int(diferencia)



def convertir_fecha(fecha_dt, timezone_id):
    try:
        # Mapear el identificador de zona horaria al formato de pytz
        timezone_pytz = timezone_mapping.get(timezone_id, timezone_id)
        tz = pytz.timezone(timezone_pytz)
        # Localizar la fecha en la zona horaria
        fecha_cst = tz.localize(fecha_dt)
        # Convertir la fecha a string en el formato adecuado
        formatted_fecha = fecha_cst.strftime("%Y-%m-%d %H:%M:%S")
        offset = fecha_cst.strftime("%z")
        # Agregamos un 0 al final de los microsegundos para que tenga 7 dígitos
        formatted_fecha = formatted_fecha 
        formatted_fecha_with_offset = f"{formatted_fecha}{offset[:3]}:{offset[3:]}"  # Reemplazar el desplazamiento por el formato -06:00
        return formatted_fecha_with_offset

    except pytz.UnknownTimeZoneError:
        print(f"Zona horaria no reconocida: {timezone_id}")
        return None

def obtener_rango_fechas(start_date: datetime, end_date: datetime):
    """
    Genera un rango de fechas entre dos fechas dadas.

    :param start_date: Fecha de inicio en tipo datetime.
    :param end_date: Fecha de finalización en tipo datetime.
    :return: Lista de fechas en el rango.
    """
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)

    return date_range
