# Cliente Python para la API del Repositorio de Información Pública de Mercado y Participante

Este proyecto proporciona un cliente de Python para interactuar de manera sencilla con la API del **Repositorio de Información de Mercado y Participante de Operati**.

El cliente gestiona la autenticación de forma automática y ofrece métodos claros y directos para cada uno de los *endpoints* disponibles en la API.

---

## Requisitos

- Python 3.6 o superior.
- La librería `requests` de Python.

---

## ⚙️ Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto:

### 1. Instalar la librería `requests`

Si no la tienes instalada, abre tu terminal o línea de comandos y ejecuta:

```bash
pip install requests
```

### 2. Guardar el archivo del cliente

Guarda el código del cliente en un archivo llamado `api_client.py` en tu directorio de trabajo.

### 3. Configurar las credenciales (¡Importante!)

Por seguridad, el cliente está diseñado para leer tus credenciales y la URL de la API desde **variables de entorno**. **No debes escribir tus credenciales directamente en el código.**

Configura las siguientes variables de entorno en tu sistema:

- `OPERATI_USERNAME`: Tu nombre de usuario para la API.
- `OPERATI_PASSWORD`: Tu contraseña para la API.
- `OPERATI_BASE_URL` (Opcional): Por defecto, apunta a `https://now.operati.com.mx:18002/ri`. Solo necesitas configurar esta variable si la URL base cambia.

Para una configuración permanente, consulta la documentación de tu sistema operativo.

---

## 🚀 Cómo Usar el Cliente

Una vez configurado, usar el cliente es muy sencillo.

1.  **Importa** la clase `OperatiAPI##`.
2.  **Crea una instancia** de la clase. La autenticación se realizará automáticamente.
3.  **Llama a los métodos** que necesites para obtener los datos.

### Ejemplo de Uso InfoMercado

A continuación, un ejemplo de cómo obtener los **Precios Marginales Locales (PML)** y el **Tipo de Cambio**.

```python
# ejemplo_uso_info_mercado.py

from api_client_info_mercado import OperatiAPIInfoMercadoClient

# Asegúrate de haber configurado las variables de entorno antes de ejecutar
try:
    # 1. Crear una instancia del cliente (la autenticación ocurre aquí)
    cliente = OperatiAPIInfoMercadoClient(
    username="tu_usuario", 
    password="tu_contraseña"
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


```

### Ejemplo de Uso Info Participante

```python
# ejemplo_uso_info_participante.py

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
```


Este ejemplo descarga un archivo ECD en formato PDF.

```python
from api_client_participante import OperatiAPIParticipanteClient
import os

try:
    cliente = OperatiAPIParticipanteClient(username="tu_usuario", password="tu_contraseña")

    print("\n--- Descargando archivo ECD en PDF ---")
    
    # Define dónde quieres guardar el archivo
    directorio_actual = os.getcwd()
    ruta_de_guardado = os.path.join(directorio_actual, "ecd_descargado.pdf")

    # Llama al método de descarga
    ruta_del_archivo = cliente.obtener_archivo_ecd_por_cuenta_y_fecha(
        cuenta_de_orden="X000YYY",
        fecha="2025-01-01",
        formato="PDF",
        save_path=ruta_de_guardado
    )

    if ruta_del_archivo:
        print(f"La descarga finalizó. Archivo disponible en: {ruta_del_archivo}")

except ValueError as e:
    print(f"Error de configuración: {e}")
except Exception as e:
    print(f"Ha ocurrido un error inesperado: {e}")
```

---