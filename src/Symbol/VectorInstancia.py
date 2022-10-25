from src.Symbol.Symbol import Simbolo



class VectorInstancia(Simbolo):

    def __init__(self,tipo, dimensiones, valores=[]):
        super().__init__()
        super().Simbolo_arreglo(tipo,dimensiones, valores)