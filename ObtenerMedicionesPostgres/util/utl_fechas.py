from datetime import datetime
import pytz


# Mapeo de nombres de zonas horarias comunes a los identificadores de pytz
timezone_mapping = {
    'Central Standard Time (Mexico)': 'America/Mexico_City',
    'US Mountain Standard Time': 'America/Denver',
    'US Eastern Standard Time': 'America/New_York',
    'US Pacific Standard Time': 'America/Los_Angeles',
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
        return fecha_cst.strftime('%Y-%m-%d %H:%M:%S.%f %z')
    except pytz.UnknownTimeZoneError:
        print(f"Zona horaria no reconocida: {timezone_id}")
        return None
