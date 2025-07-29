from api_client_info_mercado import OperatiAPIInfoMercadoClient

# Asegúrate de haber configurado las variables de entorno antes de ejecutar
try:
    # 1. Crear una instancia del cliente (la autenticación ocurre aquí)
    cliente = OperatiAPIInfoMercadoClient(
    username="jesus.gutierrez", 
    password="08090385e*"
    )

    # 2. Ejemplo 1: Consultar Precios Marginales Locales (PML)
    print("\n--- Consultando PML ---")
    datos_pml = cliente.get_pml(
        tipo_de_pml="Distribuido",
        tipo_de_mercado="MDA",
        sistema="SIN",
        clave_de_nodo="VDM NORTE",
        fecha_inicial="2024-01-01",
        fecha_final="2024-01-03"
    )

    if datos_pml:
        # Imprime los primeros 5 resultados para no saturar la consola
        print(f"Se encontraron {len(datos_pml)} registros de PML.")
        for registro in datos_pml[:5]:
            print(registro)

except ValueError as e:
    print(f"Error de configuración: {e}")
except Exception as e:
    print(f"Ha ocurrido un error inesperado: {e}")