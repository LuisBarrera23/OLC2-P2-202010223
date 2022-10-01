from src.Abstract.RetornoType import TipoDato
from src.Abstract.Instruccion import Instruccion
from src.Symbol.Symbol import Simbolo

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

class Asignacion(Instruccion):
    def __init__(self, id, expresion,linea,columna):
        self.id=id
        self.expresion=expresion
        self.linea=linea
        self.columna=columna
        
    def Ejecutar(self, entorno):
        codigoSalida=""
        existe=entorno.existeSimbolo(self.id)
        s=Singleton.getInstance()
        if existe is False:
            raise Exception(s.addError(Error(f"Variable {self.id} no existe",self.linea,self.columna)))
        else:
            valor=self.expresion.obtener3D(entorno)
            variable:Simbolo=entorno.obtenerSimbolo(self.id)

            if variable.editable is False:
                raise Exception(s.addError(Error(f"Variable {self.id} no es mutable",self.linea,self.columna)))

            if valor.tipo==variable.tipo or (valor.tipo==TipoDato.I64 and variable.tipo==TipoDato.USIZE):
                temp1=s.obtenerTemporal()
                codigoSalida += "/* ASIGNACION A UNA VARIABLE */\n"
                codigoSalida += valor.codigo + '\n'
                codigoSalida += f'{temp1} = SP + {variable.direccionRelativa}; \n'
                codigoSalida += f'Stack[(int) {temp1}] = {valor.temporal};\n'
                return codigoSalida
            else:
                raise Exception(s.addError(Error(f"Variable {self.id} no es del mismo tipo de dato que la expresion",self.linea,self.columna)))

