from api_client_participante import OperatiAPIParticipanteClient

try:
    # Crear una instancia del cliente
    cliente = OperatiAPIParticipanteClient(username="tu_usuario", password="tu_contraseña")

    # Llamar a un método para obtener datos
    print("\n--- Consultando ECD por FUECD ---")
    ecd_data = cliente.consultar_ecd_por_fuecd(fuecd="20250208X000YYY")

    if ecd_data:
        print("Datos recibidos:")
        print(ecd_data)

except ValueError as e:
    print(f"Error de configuración: {e}")
except Exception as e:
    print(f"Ha ocurrido un error inesperado: {e}")