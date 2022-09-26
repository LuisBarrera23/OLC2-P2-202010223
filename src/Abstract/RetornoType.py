from enum import IntEnum

class TipoDato(IntEnum):
    I64 = 0,
    F64 = 1,
    BOOL = 2,
    CHAR = 3,
    STRING = 4,
    STR = 5,
    USIZE = 6,
    ARREGLO = 7,
    ERROR = 8,

class RetornoType:
    def __init__(self,tipo=TipoDato.ERROR):
        self.codigo = ""
        self.etiqueta = ""
        self.temporal = ""
        self.tipo = tipo
        self.etiquetaV = ""
        self.etiquetaF = ""

    def iniciarRetorno(self,codigo, etiqueta, temporal, tipo):
        self.codigo=codigo
        self.etiqueta=etiqueta
        self.temporal=temporal
        self.tipo=tipo