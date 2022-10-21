from src.Symbol.Symbol import Simbolo

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error


class ArrayInstancia(Simbolo):

    def __init__(self,tipo, dimensiones, valores=[]):
        super().__init__()
        super().Simbolo_arreglo(tipo,dimensiones, valores)

    def obtener3D(self, listaDimensiones, index, valores):
        s=Singleton.getInstance()
    
    def Cambiar(self, listaDimensiones, index, valores, nuevo):
        s=Singleton.getInstance()
        DimensionActual:int = listaDimensiones.pop(0)
        tamanoDimension:int = self.dimensiones[index]

        if len(listaDimensiones) > 0:
            if DimensionActual > (tamanoDimension-1):
                raise Exception(s.addError(Error(f"Se ingreso una posicion no existente",0,0)))
            else:
                subArreglo = valores[DimensionActual]
                return self.Cambiar(listaDimensiones, index+1, subArreglo,nuevo)
        else:
            if DimensionActual > (tamanoDimension-1):
                raise Exception(s.addError(Error(f"Se ingreso una posicion no existente",0,0)))
            else:
                valores[DimensionActual]=nuevo
                return 