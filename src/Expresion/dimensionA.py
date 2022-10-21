from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import RetornoType,TipoDato

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

class Dimension(Expresion):
    def __init__(self,dimensiones, tipo, linea, columna):
        self.dimensiones=dimensiones
        self.tipo=tipo
        self.linea=linea
        self.columna=columna

    def obtener3D(self, entorno) -> RetornoType:
        pass