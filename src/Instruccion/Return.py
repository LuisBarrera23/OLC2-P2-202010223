from src.Abstract.Instruccion import Instruccion
from src.Abstract.RetornoType import RetornoType

from src.PatronSingleton.Singleton import Singleton
class Return(Instruccion):

    def __init__(self,expresion,linea,columna):
        self.expresion=expresion
        self.linea=linea
        self.columna=columna
        self.Retorno=RetornoType()

    def Ejecutar(self, entorno):
        #print("returnnnnn")
        s=Singleton.getInstance()
        codigoSalida=""
        
        if self.expresion!=None:
            retornoexpresion=self.expresion.obtener3D(entorno)
            codigoSalida+=retornoexpresion.codigo
            temp=s.obtenerTemporal()
            codigoSalida+=f"/* RETORNO */\n"
            codigoSalida+=f"{temp} = SP;\n"
            codigoSalida+=f"Stack[(int){temp}] = {retornoexpresion.temporal};\n"
            codigoSalida+="goto REEMPLAZORETURN;\n"
            return codigoSalida
        else:
            return "goto REEMPLAZORETURN;\n"