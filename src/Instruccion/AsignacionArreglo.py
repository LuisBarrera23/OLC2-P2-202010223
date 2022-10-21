from src.Abstract.Instruccion import Instruccion
from src.Abstract.RetornoType import TipoDato

from src.Symbol.ArrayInstancia import ArrayInstancia

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Expresion.AccesoArreglo import AccesoArreglo

class AsignacionArreglo(Instruccion):
    def __init__(self,id,listaExpresiones, expresion, linea,columna):
        self.id=id
        self.listaExpresiones=listaExpresiones
        self.expresion=expresion
        self.linea=linea
        self.columna=columna

    def Ejecutar(self, entorno):
        s=Singleton.getInstance()
        E=self.expresion.obtener3D(entorno);
        if entorno.existeSimbolo(self.id) is not True:
            raise Exception(s.addError(Error(f"Arreglo {self.id} no existe",self.linea,self.columna)))

        arreglo = entorno.obtenerSimbolo(self.id)
        if isinstance(arreglo, ArrayInstancia) is not True:
            raise Exception(s.addError(Error(f"No es referencia de un arreglo",self.linea,self.columna)))

        if E.tipo!=arreglo.tipo:
            raise Exception(s.addError(Error(f"Los elementos del arreglo no son del mismo tipo",self.linea,self.columna)))
        
        Acceso=AccesoArreglo(self.id,self.listaExpresiones,self.linea,self.columna)
        Acceso.asignacion=True
        ubicacion=Acceso.obtener3D(entorno)
        codigoSalida=""
        codigoSalida+="/* ASIGNACION DE VALOR A ARREGLO */\n"
        codigoSalida+=E.codigo
        codigoSalida+=ubicacion.codigo
        codigoSalida+=f"Heap[(int){ubicacion.temporal}] = {E.temporal};//cambio de valor\n"

        return codigoSalida
        
        