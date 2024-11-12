from enum import Enum

class TIMEZONE(Enum):
    CC = "CENTR_DE_CARGA",
    ESTADO_DE_CUENTA = "ESTADO_DE_CUENTA"

class MODALIDAD(Enum):
    HORARIO = "H",
    MINUTAL = "M"

class TIPO_MEDICION(Enum):
    KWHE = "KWHE"
    KWHR = "KWHR"
    KVAR = "KVAR"

class PARAMETROS_CONEXION (Enum):    
    DATAB_BASE = "ACCIONA_G094"
    DATASET_ID = "acciona-info-privada"
    PATH_TO_SERVICE_ACCOUNT_KEY_FILE = "C:\\Proyectos\\Operati\\cuentas_servicios\\account-app-01.json"

class PARTICIPANTE (Enum):
    ACCIONA_G094 = "ACCIONA_G094"
    ACCIONA_G032 = "ACCIONA_G032"
    ACCIONA_C035 = "ACCIONA_C035"
    ACCIONA_G069 = "ACCIONA_G069"
        