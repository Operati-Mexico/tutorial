from datetime import datetime, timedelta
import pytz


# Mapeo de nombres de zonas horarias comunes a los identificadores de pytz
timezone_mapping = {
    'Central Standard Time (Mexico)': 'America/Mexico_City',
    'US Mountain Standard Time': 'America/Hermosillo',    
    'America/Matamoros': 'America/Matamoros',
    # Agrega más mapeos según sea necesario
}


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
