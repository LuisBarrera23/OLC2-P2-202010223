
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import TipoDato,RetornoType

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Expresion.AccesoSimbolo import AccesoSimbolo
from src.Expresion.AccesoSimbolo import ArrayInstancia
from src.Expresion.AccesoArreglo import AccesoArreglo


class Clone(Expresion):
    def __init__(self,expresion,linea,columna) -> None:
        self.expresion:Expresion=expresion
        self.linea=linea
        self.columna=columna
        
    def obtener3D(self, entorno) -> RetornoType:
        s=Singleton.getInstance()
        retorno=RetornoType()

        try:
            retorno=self.expresion.obtener3D(entorno)
            #print(E.tipo)
            return retorno
        except:
            print("error al clonar")
        return retorno