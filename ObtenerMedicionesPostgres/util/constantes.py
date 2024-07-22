from enum import Enum

class MODALIDAD(Enum):
    HORARIO = "H",
    MINUTAL = "M"

class TIPO_MEDICION(Enum):
    KWHE = "KWHE"
    KWHR = "KWHR"
    KVAR = "KVAR"

class PARAMETROS_CONEXION (Enum):
    HOST = ""
    DATAB_BASE = "ACCIONA_G094"
    USER = ""
    PASSWORD = ""

class PARTICIPANTE (Enum):
    ACCIONA_G094 = "ACCIONA_G094"
    ACCIONA_G032 = "ACCIONA_G032"
    ACCIONA_C035 = "ACCIONA_C035"
    ACCIONA_G069 = "ACCIONA_G069"
        