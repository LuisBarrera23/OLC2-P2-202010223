
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import RetornoType,TipoDato
from src.Symbol.ArrayInstancia import ArrayInstancia
from src.Symbol.Symbol import Simbolo

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error
import copy

class Referencia(Expresion):
    def __init__(self, idArreglo, linea, columna):
        self.idArreglo = idArreglo
        self.linea=linea
        self.columna=columna

    def obtener3D(self, entorno) -> RetornoType:
        s=Singleton.getInstance()
        if entorno.existeSimbolo(self.idArreglo) is not True:
            raise Exception(s.addError(Error(f"Arreglo {self.id} no existe",self.linea,self.columna)))

        arreglo:Simbolo = entorno.obtenerSimbolo(self.idArreglo)
        c=copy.copy(arreglo)
        temp=s.obtenerTemporal()
        temp2=s.obtenerTemporal()
        codigoSalida=""
        codigoSalida+=f"{temp} = SP + {arreglo.direccionRelativa};\n"
        codigoSalida+=f"{temp2} = Stack[(int){temp}];\n"
        
        retorno=RetornoType()
        retorno.iniciarRetornoArray(codigoSalida,temp2,TipoDato.ARREGLO,c)
        return retorno