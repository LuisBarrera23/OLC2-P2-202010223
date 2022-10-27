from src.Abstract.RetornoType import RetornoType, TipoDato
from src.Abstract.Instruccion import Instruccion
from src.Abstract.Expresion import Expresion

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Symbol.EntornoTabla import EntornoTabla

from src.Instruccion.Break import Break

class Loop(Instruccion,Expresion):
    def __init__(self, bloque, linea, columna):
        self.bloque=bloque
        self.linea=linea
        self.columna=columna

    def Ejecutar(self, entorno):
        codigo=self.obtener3D(entorno)
        return codigo.codigo


    def obtener3D(self,entorno) -> RetornoType:
        s=Singleton.getInstance()
        
        etqCiclo=s.obtenerEtiqueta()
        etqSalida=s.obtenerEtiqueta()
        temp=s.obtenerTemporal()
        s.temporalLoop=temp
        codigoSalida=""
        codigoSalida+="/* LOOP */\n"

        nuevoEntorno=EntornoTabla(entorno)
        nuevoEntorno.tamaño=entorno.tamaño

        codigoSalida+=f"{etqCiclo}:\n"
        codigoSalida+=self.EjecutarBloque(nuevoEntorno,self.bloque)
        codigoSalida += f"goto {etqCiclo};\n"
        codigoSalida+=f"{etqSalida}:\n"


        codigoSalida=codigoSalida.replace("REEMPLAZOBREAK",etqSalida)
        retorno=RetornoType()
        retorno.iniciarRetorno(codigoSalida,"",temp,s.tipoTemporal)
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