# api_client.py

import requests
import os

class OperatiAPIInfoMercadoClient:
    """
    Cliente de Python para interactuar con el Repositorio de Información 
    Pública de Mercado de Operati.

    Este cliente maneja la autenticación y proporciona métodos para consumir
    cada uno de los endpoints de la API.
    """

    def __init__(self, username=None, password=None):
        """
        Inicializa el cliente de la API.

        Puedes pasar el usuario y la contraseña directamente al crear la instancia.
        Si no se proporcionan, el cliente intentará leerlos desde las variables de entorno.

        Args:
            username (str, optional): Tu nombre de usuario para la API.
            password (str, optional): Tu contraseña para la API.
        """
        self.base_url = os.getenv("OPERATI_BASE_URL", "https://now.operati.com.mx:18002/ri")
        
        # Prioriza los argumentos pasados a la clase sobre las variables de entorno.
        self.username = username or os.getenv("OPERATI_USERNAME")
        self.password = password or os.getenv("OPERATI_PASSWORD")
        
        if not self.username or not self.password:
            raise ValueError("Debes proporcionar 'username' y 'password' al crear la clase, o configurar las variables de entorno.")

        self.session = requests.Session()
        self._authenticate()

    def _authenticate(self):
        """
        Realiza la autenticación contra la API para obtener un token JWT.
        El token se añade automáticamente a las cabeceras de las futuras peticiones.
        """
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

    def _get_request(self, endpoint: str, params: dict = None):
        """
        Método genérico para realizar peticiones GET.
        """
        url = f"{self.base_url}{endpoint}"
        try:            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error en la petición a {url}: {e.response.status_code} - {e.response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión en la petición a {url}: {e}")
            return None

    # --- Precios Marginales Locales ---
    
    def get_pml(self, tipo_de_pml: str, tipo_de_mercado: str, sistema: str, clave_de_nodo: str, fecha_inicial: str, fecha_final: str):
        params = {"tipoDePML": tipo_de_pml, "tipoDeMercado": tipo_de_mercado, "sistema": sistema, "claveDeNodo": clave_de_nodo, "fechaInicial": fecha_inicial, "fechaFinal": fecha_final}
        return self._get_request("/infopublica/pml", params=params)

    def get_pml_agrupado(self, tipo_mercado: str, tipo_pml: str, tipo_funcion: str, elemento: str, fecha_inicial: str, fecha_final: str):
        params = {"tipoMercado": tipo_mercado, "tipoPML": tipo_pml, "tipoFuncion": tipo_funcion, "elemento": elemento, "fechaInicial": fecha_inicial, "fechaFinal": fecha_final}
        return self._get_request("/infopublica/pml_agrupado/", params=params)

    # --- Ofertas de Compra y Venta ---
    
    def get_ofertas_termicas(self, fecha: str, sistema: str, tipo_mercado: str):
        params = {"fecha": fecha, "sistema": sistema, "tipoMercado": tipo_mercado}
        return self._get_request("/infopublica/OcvTermicas", params=params)

    def get_ofertas_no_despachables(self, fecha: str, sistema: str, tipo_mercado: str):
        params = {"fecha": fecha, "sistema": sistema, "tipoMercado": tipo_mercado}
        return self._get_request("/infopublica/OcvNoDespachables", params=params)
        
    def get_ofertas_hidro(self, fecha: str, sistema: str, tipo_mercado: str):
        params = {"fecha": fecha, "sistema": sistema, "tipoMercado": tipo_mercado}
        return self._get_request("/infopublica/OcvHidro", params=params)
        
    def get_ofertas_gi_generacion(self, fecha: str, sistema: str, tipo_mercado: str):
        params = {"fecha": fecha, "sistema": sistema, "tipoMercado": tipo_mercado}
        return self._get_request("/infopublica/OcvGiGeneracion", params=params)
        
    def get_ofertas_gi_consumo(self, fecha: str, sistema: str, tipo_mercado: str):
        params = {"fecha": fecha, "sistema": sistema, "tipoMercado": tipo_mercado}
        return self._get_request("/infopublica/OcvGiConsumo", params=params)
        
    def get_ofertas_exportacion(self, fecha: str, sistema: str, tipo_mercado: str):
        params = {"fecha": fecha, "sistema": sistema, "tipoMercado": tipo_mercado}
        return self._get_request("/infopublica/OcvExportacion", params=params)
        
    def get_ofertas_importacion(self, fecha: str, sistema: str, tipo_mercado: str):
        params = {"fecha": fecha, "sistema": sistema, "tipoMercado": tipo_mercado}
        return self._get_request("/infopublica/OcvImportacion", params=params)
        
    def get_ofertas_despachables(self, fecha: str, sistema: str, tipo_mercado: str):
        params = {"fecha": fecha, "sistema": sistema, "tipoMercado": tipo_mercado}
        return self._get_request("/infopublica/OcvDespachables", params=params)
        
    def get_ofertas_compra(self, fecha: str, sistema: str, tipo_mercado: str):
        params = {"fecha": fecha, "sistema": sistema, "tipoMercado": tipo_mercado}
        return self._get_request("/infopublica/OcvCompra", params=params)

    # --- Estimación de la Demanda Real ---
    
    def get_edrr_demanda_por_retiros(self, fecha_operacion_inicial: str, fecha_operacion_final: str, liquidacion: int, sistema: str, zona_carga: str):
        params = {"fechaOperacionInicial": fecha_operacion_inicial, "fechaOperacionFinal": fecha_operacion_final, "liquidacion": liquidacion, "sistema": sistema, "zonaCarga": zona_carga}
        return self._get_request("/infopublica/infoMercado/tblEdrRetiro", params=params)

    def get_edrb_demanda_por_balance(self, fecha_operacion_inicial: str, fecha_operacion_final: str, liquidacion: int, sistema: str, area: str):
        params = {"fechaOperacionInicial": fecha_operacion_inicial, "fechaOperacionFinal": fecha_operacion_final, "liquidacion": liquidacion, "sistema": sistema, "area": area}
        return self._get_request("/infopublica/infoMercado/tblEdrBalance", params=params)

    # --- Estimación de Pérdidas Reales ---
    
    def get_eprd_perdidas_distribucion(self, fecha: str, liquidacion: int, sistema: str, zona_de_carga: str):
        params = {"fecha": fecha, "liquidacion": liquidacion, "sistema": sistema, "zonaDeCarga": zona_de_carga}
        return self._get_request("/infopublica/EprtDistribucion", params=params)

    def get_eprt_perdidas_transmision(self, fecha: str, liquidacion: int, sistema: str):
        params = {"fecha": fecha, "liquidacion": liquidacion, "sistema": sistema}
        return self._get_request("/infopublica/EprtTransmision", params=params)

    # --- Capacidad de Transferencia ---
    
    def get_ctei_capacidad_transferencia(self, fecha_operacion_inicial: str, fecha_operacion_final: str, sistema: str, enlace: str):
        params = {"fechaOperacionInicial": fecha_operacion_inicial, "fechaOperacionFinal": fecha_operacion_final, "sistema": sistema, "enlace": enlace}
        return self._get_request("/infopublica/infoMercado/tblCtei", params=params)

    # --- Energía Generada por Tipo de Tecnología ---
    
    def get_egtt_energia_generada_tecnologia(self, fecha_operacion_inicial: str, fecha_operacion_final: str):
        params = {"fechaOperacionInicial": fecha_operacion_inicial, "fechaOperacionFinal": fecha_operacion_final}
        return self._get_request("/infopublica/infoMercado/tblEgtt", params=params)

    # --- Cantidades Asignadas ---
    
    def get_ca_energia(self, sistema: str, zona_de_carga: str, fecha_inicial: str, fecha_final: str):
        params = {"sistema": sistema, "zonaDeCarga": zona_de_carga, "fechainicial": fecha_inicial, "fechafinal": fecha_final}
        return self._get_request("/infopublica/ca_energia/", params=params)

    def get_ca_importacion_exportacion(self, sistema: str, fecha_inicial: str, fecha_final: str, clave_de_nodo: str):
        params = {"sistema": sistema, "fechainicial": fecha_inicial, "fechafinal": fecha_final, "claveDeNodo": clave_de_nodo}
        return self._get_request("/infopublica/ca_impex/", params=params)

    def get_ca_servicios_conexos(self, sistema: str, fecha_inicial: str, fecha_final: str, tipo_de_mercado: str):
        params = {"sistema": sistema, "fechainicial": fecha_inicial, "fechafinal": fecha_final, "tipodemercado": tipo_de_mercado}
        return self._get_request("/infopublica/ca_conexos/", params=params)

    # --- Precio Servicios Conexos ---
    
    def get_precio_servicios_conexos(self, tipo_de_mercado: str, sistema: str, fecha_inicial: str, fecha_final: str):
        params = {"tipodemercado": tipo_de_mercado, "sistema": sistema, "fechainicial": fecha_inicial, "fechafinal": fecha_final}
        return self._get_request("/infopublica/precio_conexos/", params=params)

    # --- Nodos ---
    
    def get_catalogo_nodos(self, tipo_de_lista: str):
        params = {"tipoDeLista": tipo_de_lista}
        return self._get_request("/infopublica/listadenodos/", params=params)

    # --- Indicadores Financieros ---
    
    def get_uspp_indicador_financiero(self, fecha_inicial: str, fecha_final: str, serie: str):
        params = {"fechaInicial": fecha_inicial, "fechaFinal": fecha_final, "serie": serie}
        return self._get_request("/infopublica/uspp/", params=params)

    def get_ppi_us(self, fecha_inicial: str, fecha_final: str, serie: str, preliminar: bool = False):
        params = {"fechaInicial": fecha_inicial, "fechaFinal": fecha_final, "serie": serie, "preliminar": str(preliminar).lower()}
        return self._get_request("/infopublica/ppi-us/", params=params)

    def get_cpi_us(self, fecha_inicial: str, fecha_final: str, serie: str):
        params = {"fechaInicial": fecha_inicial, "fechaFinal": fecha_final, "serie": serie}
        return self._get_request("/infopublica/cpi-us/", params=params)

    def get_inpp_sin_petroleo(self, concepto: str, fecha_inicial: str, fecha_final: str):
        params = {"concepto": concepto, "fechaInicial": fecha_inicial, "fechaFinal": fecha_final}
        return self._get_request("/infopublica/inpp/", params=params)

    def get_tipo_de_cambio(self, fecha_inicial: str, fecha_final: str, serie: str):
        params = {"fechaInicial": fecha_inicial, "fechaFinal": fecha_final, "serie": serie}
        return self._get_request("/infopublica/tipo_cambio", params=params)
        
    # --- Pronóstico de Demanda ---
    
    def get_pronostico_demanda_cenace(self, fecha_ini: str, fecha_fin: str, sistema: str, regiones: str):
        params = {"fechaIni": fecha_ini, "fechaFin": fecha_fin, "sistema": sistema, "regiones": regiones}
        return self._get_request("/infopublica/pronostico-demanda-cenace", params=params)
        
    # --- Estado Operativo SEN ---
    
    def get_estado_operativo_sen(self, fecha_folio_ini: str, fecha_folio_fin: str):
        params = {"fechaFolioIni": fecha_folio_ini, "fechaFolioFin": fecha_folio_fin}
        return self._get_request("/infopublica/estado-operativo-sen/fecha-folio", params=params)
        
    # --- 100 Horas Críticas ---
    
    def get_cien_horas_criticas(self, sistema: str, anio: int):
        params = {"sistema": sistema, "anio": anio}
        return self._get_request("/infopublica/cien-horas", params=params)
        
    # --- Margen Reserva Operativa ---
    
    def get_margen_reserva_operativa(self, fecha_inicial: str, fecha_final: str):
        params = {"fechaInicial": fecha_inicial, "fechaFinal": fecha_final}
        return self._get_request("/infopublica/margen-reserva-operativa/fecha-demanda-maxima", params=params)