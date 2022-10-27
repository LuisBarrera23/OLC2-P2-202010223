from src.Abstract.RetornoType import RetornoType, TipoDato
from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Abstract.Expresion import Expresion
from src.Symbol.EntornoTabla import EntornoTabla

class If_e(Expresion):
    def __init__(self, condicion, Bloqueverdadero,expresion1, listaElseIf, BloqueElse,expresion2,linea, columna):
        self.condicion=condicion
        self.Bloqueverdadero=Bloqueverdadero
        self.expresion1=expresion1
        self.listaElseIf=listaElseIf
        self.BloqueElse=BloqueElse
        self.expresion2=expresion2
        self.linea=linea
        self.columna=columna

    def obtener3D(self, entorno):
        s=Singleton.getInstance()
        codigoSalida=""
        etqSalida=s.obtenerEtiqueta()
        temp=s.obtenerTemporal()
        self.condicion.etiquetaVerdadera=s.obtenerEtiqueta()
        self.condicion.etiquetaFalsa=s.obtenerEtiqueta()
        condicion=self.condicion.obtener3D(entorno)
        
        codigoSalida += "/* INSTRUCCION IF */\n"
        codigoSalida += condicion.codigo
        codigoSalida += f"{condicion.etiquetaV}: \n"


        nuevoEntorno=EntornoTabla(entorno)
        nuevoEntorno.tamaño=entorno.tamaño
        codigoSalida += self.EjecutarBloque(nuevoEntorno,self.Bloqueverdadero)
        E=self.expresion1.obtener3D(nuevoEntorno)
        codigoSalida+=E.codigo
        codigoSalida+=f"{temp} = {E.temporal};\n"


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
            E=e.expresion1.obtener3D(nuevoEntorno)
            codigoSalida+=E.codigo
            codigoSalida+=f"{temp} = {E.temporal};\n"


            codigoSalida += f"goto {etqSalida};\n"
            codigoSalida += f"{exp.etiquetaF}:\n"


        nuevoEntorno=EntornoTabla(entorno)
        nuevoEntorno.tamaño=entorno.tamaño
        codigoSalida+=self.EjecutarBloque(nuevoEntorno,self.BloqueElse)
        E=self.expresion2.obtener3D(nuevoEntorno)
        codigoSalida+=E.codigo
        codigoSalida+=f"{temp} = {E.temporal};\n"

        codigoSalida += f"{etqSalida}:\n"
        retorno=RetornoType()
        retorno.iniciarRetorno(codigoSalida,"",temp,E.tipo)
        return retorno


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