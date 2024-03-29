from src.Abstract.RetornoType import RetornoType, TipoDato

from src.Abstract.Expresion import Expresion

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Symbol.ArrayInstancia import ArrayInstancia
from src.Symbol.VectorInstancia import VectorInstancia

class AccesoSimbolo(Expresion):

    def __init__(self,id,linea,columna):
        self.id=id
        self.linea=linea
        self.columna=columna

        self.etiquetaVerdadera=""
        self.etiquetaFalsa=""

    def obtener3D(self,entorno):
        s=Singleton.getInstance()
        if entorno.existeSimbolo(self.id):
            E=entorno.obtenerSimbolo(self.id)
            retorno=RetornoType()
            if isinstance(E,ArrayInstancia):
                retorno.iniciarRetorno("","","",TipoDato.ARREGLO)
                return retorno
            elif isinstance(E,VectorInstancia):
                retorno.iniciarRetorno("","","",TipoDato.VECTOR)
                return retorno
            temp1=s.obtenerTemporal()
            temp2=s.obtenerTemporal()
            codigoSalida=""
            
            codigoSalida += f"/* ACCESO SIMBOLO PRIMITIVO */\n"
            codigoSalida += f"{temp1} = SP + {E.direccionRelativa};\n"
            codigoSalida += f"{temp2} = Stack[(int){temp1}];\n"

            if E.tipo == TipoDato.BOOL and self.etiquetaVerdadera != "":
                codigoSalida += f"if ({temp2} == 1) goto {self.etiquetaVerdadera};\n"
                codigoSalida += f"goto {self.etiquetaFalsa};\n"
                retorno.etiquetaV=self.etiquetaVerdadera
                retorno.etiquetaF=self.etiquetaFalsa
            retorno.iniciarRetorno(codigoSalida,"",temp2,E.tipo)
            return retorno
        else:
            raise Exception(s.addError(Error(f"Variable {self.id} no existe",self.linea,self.columna)))