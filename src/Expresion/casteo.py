from lib2to3.pgen2.token import STRING
from tkinter import E
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import TipoDato,RetornoType

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

class Casteo(Expresion):
    def __init__(self,expresion,linea,columna,tipo=None) -> None:
        self.expresion:Expresion=expresion
        self.tipo=tipo
        self.linea=linea
        self.columna=columna
        
    def obtener3D(self, entorno) -> RetornoType:
        s=Singleton.getInstance()
        E1=self.expresion.obtener3D(entorno)
        if(self.tipo==None):
            if(E1.tipo==TipoDato.STR or E1.tipo==TipoDato.STRING):
                E1.tipo=TipoDato.STRING
                return E1
            else:
                raise Exception(s.addError(Error(f"Se necesita un cadena para ejecutar to_string o to_owned",self.linea,self.columna)))
        else:
            if(E1.tipo==TipoDato.I64 or E1.tipo==TipoDato.F64):
                if(self.tipo==TipoDato.I64):
                    E1.tipo=TipoDato.I64
                    return E1
                elif(self.tipo==TipoDato.F64):
                    E1.tipo=TipoDato.F64
                    return E1
        return E1