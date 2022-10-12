from src.Abstract.RetornoType import TipoDato,RetornoType
from src.Abstract.Instruccion import Instruccion
from src.Symbol.Symbol import Simbolo
from src.Symbol.EntornoTabla import EntornoTabla
from src.Instruccion.Return import Return
from src.Instruccion.Break import Break
from src.Instruccion.Continue import Continue

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

class If_i(Instruccion):
    def __init__(self, condicion, Bloqueverdadero, listaElseIf, BloqueElse,linea, columna):
        self.condicion=condicion
        self.Bloqueverdadero=Bloqueverdadero
        self.listaElseIf=listaElseIf
        self.BloqueElse=BloqueElse
        self.linea=linea
        self.columna=columna
        
    def Ejecutar(self, entorno):
        s=Singleton.getInstance()
        codigoSalida=""
        etqSalida=s.obtenerEtiqueta()
        self.condicion.etiquetaVerdadera=s.obtenerEtiqueta()
        self.condicion.etiquetaFalsa=s.obtenerEtiqueta()
        condicion=self.condicion.obtener3D(entorno)
        
        codigoSalida += "/* INSTRUCCION IF */\n"
        codigoSalida += condicion.codigo
        codigoSalida += f"{condicion.etiquetaV}: \n"
        nuevoEntorno=EntornoTabla(entorno)
        nuevoEntorno.tamaño=entorno.tamaño
        codigoSalida += self.EjecutarBloque(nuevoEntorno,self.Bloqueverdadero)
        codigoSalida += f"goto {etqSalida};\n"
        codigoSalida += f"{condicion.etiquetaF}:\n"

        for e in self.listaElseIf:
            e.condicion.etiquetaVerdadera=s.obtenerEtiqueta()
            e.condicion.etiquetaFalsa=s.obtenerEtiqueta()
            exp:RetornoType=e.condicion.obtener3D(entorno)
            codigoSalida += "\n/* INSTRUCCION ELSE IF*/\n"
            codigoSalida += exp.codigo
            codigoSalida += f"{exp.etiquetaV}:\n"
            nuevoEntorno=EntornoTabla(entorno)
            nuevoEntorno.tamaño=entorno.tamaño
            codigoSalida += self.EjecutarBloque(nuevoEntorno, e.Bloqueverdadero)
            codigoSalida += f"goto {etqSalida};\n"
            codigoSalida += f"{exp.etiquetaF}:\n"
        nuevoEntorno=EntornoTabla(entorno)
        nuevoEntorno.tamaño=entorno.tamaño
        codigoSalida+=self.EjecutarBloque(nuevoEntorno,self.BloqueElse)
        codigoSalida += f"{etqSalida}:\n"
        return codigoSalida


    def EjecutarBloque(self,entorno,lista):
        codigoSalida = ""
        for i in lista :
            codigoSalida += i.Ejecutar(entorno)
        return codigoSalida