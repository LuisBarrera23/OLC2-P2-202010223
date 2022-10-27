from src.Abstract.Instruccion import Instruccion
from src.Abstract.RetornoType import TipoDato,RetornoType

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Instruccion.Break import Break
from src.Instruccion.Continue import Continue
from src.Instruccion.Return import Return

from src.Symbol.EntornoTabla import EntornoTabla

class While(Instruccion):
    def __init__(self, condicion, bloque, linea, columna):
        self.condicion=condicion
        self.bloque=bloque
        self.linea=linea
        self.columna=columna

    def Ejecutar(self, entorno):
        s=Singleton.getInstance()
        self.condicion.etiquetaVerdadera=s.obtenerEtiqueta()
        self.condicion.etiquetaFalsa=s.obtenerEtiqueta()
        E1:RetornoType=self.condicion.obtener3D(entorno)
        if E1.tipo!=TipoDato.BOOL:
            raise Exception(s.addError(Error(f"Instruccion while necesita una expresion booleana",self.linea,self.columna)))
        etqCiclo=s.obtenerEtiqueta()
        codigoSalida=""
        codigoSalida+="/* WHILE */\n"
        codigoSalida+=f"{etqCiclo}:\n"
        codigoSalida+=E1.codigo
        codigoSalida+=f"{E1.etiquetaV}:\n"
        codigoSalida+=self.EjecutarBloque(entorno,self.bloque)
        codigoSalida += f"goto {etqCiclo};\n"
        codigoSalida+=f"{E1.etiquetaF}:\n"
        codigoSalida=codigoSalida.replace("REEMPLAZOBREAK",E1.etiquetaF)
        codigoSalida=codigoSalida.replace("REEMPLAZOCONTINUE",etqCiclo)
        return codigoSalida

    def EjecutarBloque(self,entorno,lista):
        codigoSalida = ""
        for i in lista :
            try:
                codigoSalida += i.Ejecutar(entorno)
                pass
            except:
                print("error.........................")
            #codigoSalida += i.Ejecutar(entorno) 
        return codigoSalida
