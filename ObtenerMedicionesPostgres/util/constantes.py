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
    HOST = "35.239.245.216"
    DATAB_BASE = "ACCIONA_G094"
    USER = "postgresroot"
    PASSWORD = "xOLrRmjwPI#*.D2T8zKx0K6n"

class PARTICIPANTE (Enum):
    ACCIONA_G094 = "ACCIONA_G094"
    ACCIONA_G032 = "ACCIONA_G032"
    ACCIONA_C035 = "ACCIONA_C035"
    ACCIONA_G069 = "ACCIONA_G069"
        