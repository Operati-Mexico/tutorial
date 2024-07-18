from enum import Enum

class TIPO_MEDICION(Enum):
    KWHE = "KWHE"
    KWHR = "KWHR"
    KVAR = "KVAR"

class PARAMETROS_CONEXION (Enum):
    HOST = ""
    DATAB_BASE = ""
    USER = ""
    PASSWORD = ""
        