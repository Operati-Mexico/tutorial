import requests
import os
from typing import Optional

class OperatiAPIParticipanteClient:
    """
    Cliente de Python para interactuar con el Repositorio de Información de Operati (V2.8).

    Este cliente maneja la autenticación y proporciona métodos para consumir cada uno
    de los endpoints de la API, incluyendo la descarga de archivos.
    """

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        Inicializa el cliente.

        Puedes pasar el usuario y la contraseña directamente al crear la instancia,
        o el cliente intentará leerlos desde las variables de entorno.

        Args:
            username (str, optional): Tu nombre de usuario para la API.
            password (str, optional): Tu contraseña para la API.
        """
        self.base_url = os.getenv("OPERATI_BASE_URL", "https://webservices.operati.com.mx:18002/ri")
        
        self.username = username or os.getenv("OPERATI_USERNAME")
        self.password = password or os.getenv("OPERATI_PASSWORD")
        
        if not self.username or not self.password:
            raise ValueError("Debes proporcionar 'username' y 'password' o configurar las variables de entorno.")

        self.session = requests.Session()
        self._authenticate()

    def _authenticate(self):
        login_url = f"{self.base_url}/login/"
        credentials = {"username": self.username, "password": self.password}
        try:
            response = self.session.post(login_url, json=credentials)
            response.raise_for_status()
            token = response.text.strip('"')
            self.session.headers.update({"Authorization": f"Bearer {token}"})
            print("Autenticación exitosa.")
        except requests.exceptions.HTTPError as e:
            print(f"Error de autenticación: {e.response.status_code} {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión durante la autenticación: {e}")
            raise

    def _get_json_request(self, endpoint: str, params: Optional[dict] = None):
        """Método genérico para peticiones que devuelven JSON."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error en la petición a {url}: {e.response.status_code} - {e.response.text}")
            return None
        except requests.exceptions.JSONDecodeError:
            print(f"Error: La respuesta de {url} no es un JSON válido. Contenido: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión en la petición a {url}: {e}")
            return None

    def _download_file_request(self, endpoint: str, save_path: str, params: Optional[dict] = None):
        """Método genérico para peticiones que descargan un archivo."""
        url = f"{self.base_url}{endpoint}"
        try:
            with self.session.get(url, params=params, stream=True) as response:
                response.raise_for_status()
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"Archivo guardado exitosamente en: {save_path}")
            return save_path
        except requests.exceptions.HTTPError as e:
            print(f"Error al descargar de {url}: {e.response.status_code} - {e.response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión al descargar de {url}: {e}")
            return None

    # --- Estados de Cuenta Diario (ECD) ---

    def consultar_ecd_por_fuecd(self, fuecd: str):
        return self._get_json_request("/ecds/", params={"fuecd": fuecd})

    def consultar_ecd_por_cuenta_y_fecha(self, cuenta_de_orden: str, fecha: str):
        return self._get_json_request("/ecds/", params={"cuentadeorden": cuenta_de_orden, "fecha": fecha})

    def consultar_anexos_ecd(self, fecha_operacion_rango_ini: str, fecha_operacion_rango_fin: str, subcuenta: str, folio: str, reliquidacion: int = 0):
        params = {"fechaOperacionRangoIni": fecha_operacion_rango_ini, "fechaOperacionRangoFin": fecha_operacion_rango_fin, "subcuenta": subcuenta, "folio": folio, "reliquidacion": reliquidacion}
        return self._get_json_request("/ecds/GetAnexosFUF", params=params)

    def consultar_desglose_fuf(self, fecha_inicial: str, fecha_final: str, subcuentas: str):
        return self._get_json_request("/ecds/GetListadoFULs/", params={"fechaInicial": fecha_inicial, "fechaFinal": fecha_final, "subcuentas": subcuentas})

    def obtener_archivo_ecd_por_cuenta_y_fecha(self, cuenta_de_orden: str, fecha: str, formato: str, save_path: str):
        return self._download_file_request("/file/ecd/", save_path, params={"cuentadeorden": cuenta_de_orden, "fecha": fecha, "formato": formato})

    def obtener_archivo_ecd_por_fecha(self, fecha: str, save_path: str):
        ''' Retorna zip '''
        return self._download_file_request("/file/ecds/", save_path, params={"fecha": fecha})
    
    def obtener_archivo_anexos_ecd(self, cuenta_orden: str, fecha_ec_ini: str, fecha_ec_fin: str, save_path: str):
        ''' Retorna xlsx '''
        params = {"cuentaOrden": cuenta_orden, "fechaECIni": fecha_ec_ini, "fechaECFin": fecha_ec_fin}
        return self._download_file_request("/file/ecds/parseo/anexos/excel", save_path, params=params)

    # --- Mediciones ---

    def consultar_mediciones_fiscales(self, id_medidor: str, parametro: str, fecha: str, modalidad: str):
        params = {"idmedidor": id_medidor, "parametro": parametro, "fecha": fecha, "modalidad": modalidad}
        return self._get_json_request("/mediciones/", params=params)

    def obtener_archivo_mediciones_fiscales(self, id_medidor: str, parametro: str, fecha: str, modalidad: str, formato: str, save_path: str):
        '''retorna csv xlsx'''
        params = {"idmedidor": id_medidor, "parametro": parametro, "fecha": fecha, "modalidad": modalidad, "formato": formato}
        return self._download_file_request("/file/medicion", save_path, params=params)

    def obtener_archivos_mediciones_fiscales_por_fecha(self, fecha: str, save_path: str):
        return self._download_file_request("/file/mediciones", save_path, params={"fecha": fecha})

    # --- Documentos Fiscales ---

    def consultar_documento_fiscal_por_parametros(self, parametro: str, valor: str):
        return self._get_json_request("/documentosfiscales/GetDocumentoFiscal/", params={"parametro": parametro, "valor": valor})
        
    def consultar_documento_fiscal_por_fecha(self, fecha: str):
        return self._get_json_request("/documentosfiscales/", params={"fecha": fecha})

    def obtener_archivo_documento_fiscal_por_parametros(self, parametro: str, valor: str, save_path: str):
        return self._download_file_request("/file/documentofiscal", save_path, params={"parametro": parametro, "valor": valor})

    def obtener_archivos_documento_fiscal_por_fecha(self, fecha: str, save_path: str):
        return self._download_file_request("/file/documentosfiscales/", save_path, params={"fecha": fecha})

    # --- Escritorio 24/7 ---
    
    def consultar_tickets_por_fechas(self, fecha_inicial: str, fecha_final: str):
        return self._get_json_request("/Escritorio247/ticket/", params={"fechaInicial": fecha_inicial, "fechaFinal": fecha_final})

    # --- Responsabilidad Estimada Agregada (REA) ---
    
    def consultar_rea(self, fecha_inicial: str, fecha_final: str):
        # Nota: Este endpoint en Postman usa la misma URL que la consulta de tickets.
        return self._get_json_request("/ReaYGarantias/rea/", params={"fechaIni": fecha_inicial, "fechafin": fecha_final})

