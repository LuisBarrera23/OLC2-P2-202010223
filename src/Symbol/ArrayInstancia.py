from src.Symbol.Symbol import Simbolo

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error


class ArrayInstancia(Simbolo):

    def __init__(self,tipo, dimensiones, valores=[]):
        super().__init__()
        super().Simbolo_arreglo(tipo,dimensiones, valores)

    
    