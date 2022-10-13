from src.Abstract.Instruccion import Instruccion
from src.Abstract.RetornoType import RetornoType

from src.PatronSingleton.Singleton import Singleton
class Break(Instruccion):

    def __init__(self,expresion,linea,columna):
        self.expresion=expresion
        self.linea=linea
        self.columna=columna

    def Ejecutar(self, entorno):
        #print("break")
        s=Singleton.getInstance()
        codigoSalida=""
        
        if self.expresion!=None:
            retornoexpresion=self.expresion.obtener3D(entorno)
            codigoSalida+=retornoexpresion.codigo
            temp=s.obtenerTemporal()
            codigoSalida+=f"/* BREAK */\n"
            codigoSalida+=f"{s.temporalLoop}= {retornoexpresion.temporal};\n"
            codigoSalida+="goto REEMPLAZOBREAK;\n"
            s.tipoTemporal=retornoexpresion.tipo
            return codigoSalida
        else:
            codigoSalida+=f"/* BREAK */\n"
            codigoSalida+="goto REEMPLAZOBREAK;\n"
            return codigoSalida