
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import TipoDato,RetornoType

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Expresion.AccesoSimbolo import AccesoSimbolo
from src.Symbol.VectorInstancia import VectorInstancia

from src.Symbol.Symbol import Simbolo


class Capacity(Expresion):
    def __init__(self,expresion,linea,columna) -> None:
        self.expresion:Expresion=expresion
        self.linea=linea
        self.columna=columna
        
    def obtener3D(self, entorno) -> RetornoType:
        s=Singleton.getInstance()
        codigoSalida=""
        retorno=RetornoType()

        if isinstance(self.expresion,AccesoSimbolo):
            if entorno.existeSimbolo(self.expresion.id)==False:
                raise Exception(s.addError(Error(f"No existe variable con este ID",self.linea,self.columna)))
            arreglo:Simbolo=entorno.obtenerSimbolo(self.expresion.id)
            if isinstance(arreglo,VectorInstancia):
                temp1=s.obtenerTemporal()
                temp2=s.obtenerTemporal()
                temp3=s.obtenerTemporal()
                temp4=s.obtenerTemporal()
                codigoSalida+="/* OPERACION CAPACITY */\n"
                codigoSalida+=f"{temp1} = SP + {arreglo.direccionRelativa};\n"
                codigoSalida+= f"{temp2} = Stack[(int){temp1}];\n"
                codigoSalida+= f"{temp3} = {temp2} + 1;\n"
                codigoSalida+=f"{temp4} = Heap[(int){temp3}];\n"
                retorno.iniciarRetorno(codigoSalida,"",temp4,TipoDato.I64)
                return retorno
            else:
                raise Exception(s.addError(Error(f"Esta expresion no puede ser operada con len()",self.linea,self.columna)))