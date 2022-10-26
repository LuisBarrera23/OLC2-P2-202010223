
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import RetornoType,TipoDato
from src.Symbol.ArrayInstancia import ArrayInstancia
from src.Symbol.VectorInstancia import VectorInstancia
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

        referencia:Simbolo = entorno.obtenerSimbolo(self.idArreglo)
        if isinstance(referencia,ArrayInstancia):
            c=copy.copy(referencia)
            temp=s.obtenerTemporal()
            temp2=s.obtenerTemporal()
            codigoSalida=""
            codigoSalida+=f"{temp} = SP + {referencia.direccionRelativa};\n"
            codigoSalida+=f"{temp2} = Stack[(int){temp}];\n"
            
            retorno=RetornoType()
            retorno.iniciarRetornoArray(codigoSalida,temp2,TipoDato.ARREGLO,c)
            return retorno
        elif isinstance(referencia,VectorInstancia):
            c=copy.copy(referencia)
            temp=s.obtenerTemporal()
            temp2=s.obtenerTemporal()
            temp3=s.obtenerTemporal()
            codigoSalida=""
            codigoSalida+=f"{temp3} = SP;\n"
            codigoSalida+=f"{temp} = SP + {referencia.direccionRelativa};\n"
            codigoSalida+=f"{temp2} = Stack[(int){temp}];\n"
            c.nombreAnterior=referencia.identificador
            c.punteroReferencia=temp3
            retorno=RetornoType()
            retorno.iniciarRetornoVector(codigoSalida,temp2,TipoDato.VECTOR,c)
            return retorno