from api_client_participante import OperatiAPIParticipanteClient
import os

try:
    cliente = OperatiAPIParticipanteClient(username="tu_usuario", password="tu_contraseña")

    print("\n--- Descargando archivo ECD en PDF ---")
    
    # Define dónde quieres guardar el archivo
    directorio_actual = os.getcwd()
    ruta_de_guardado = os.path.join(directorio_actual, "ecd_descargado.xml")

    # Llama al método de descarga
    ruta_del_archivo = cliente.obtener_archivo_anexos_ecd(        
        cuenta_orden="xxxx",
        fecha_ec_ini="2025-07-01",
        fecha_ec_fin="2025-07-01",
        save_path=ruta_de_guardado
    )

    if ruta_del_archivo:
        print(f"La descarga finalizó. Archivo disponible en: {ruta_del_archivo}")

except ValueError as e:
    print(f"Error de configuración: {e}")
except Exception as e:
    print(f"Ha ocurrido un error inesperado: {e}")