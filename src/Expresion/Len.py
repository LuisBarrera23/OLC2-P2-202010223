
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import TipoDato,RetornoType

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Expresion.AccesoSimbolo import AccesoSimbolo
from src.Expresion.AccesoSimbolo import ArrayInstancia
from src.Expresion.AccesoArreglo import AccesoArreglo

from src.Symbol.Symbol import Simbolo


class Len(Expresion):
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
            if isinstance(arreglo,ArrayInstancia):
                temp1=s.obtenerTemporal()
                temp2=s.obtenerTemporal()
                temp3=s.obtenerTemporal()
                codigoSalida+="/* OPERACION LEN */\n"
                codigoSalida+=f"{temp1} = SP + {arreglo.direccionRelativa};\n"
                codigoSalida+= f"{temp2} = Stack[(int){temp1}];\n"
                codigoSalida+=f"{temp3} = Heap[(int){temp2}];\n"
                retorno.iniciarRetorno(codigoSalida,"",temp3,TipoDato.I64)
                return retorno
            else:
                raise Exception(s.addError(Error(f"Esta expresion no puede ser operada con len()",self.linea,self.columna)))
        elif isinstance(self.expresion,AccesoArreglo):
            self.expresion.len=True
            E=self.expresion.obtener3D(entorno)
            temp1=s.obtenerTemporal()
            codigoSalida+="/* OPERACION LEN */\n"
            codigoSalida+= E.codigo
            codigoSalida+=f"{temp1} = Heap[(int){E.temporal}];\n"
            retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.I64)
            return retorno
        return