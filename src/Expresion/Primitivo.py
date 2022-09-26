from enum import Enum
from src.Abstract.RetornoType import RetornoType,TipoDato
from src.PatronSingleton.Singleton import Singleton
from src.Abstract.Expresion import Expresion

class Primitivo(Expresion):

    def __init__(self,valor,tipo):
        self.valor=valor
        self.tipo=tipo

    def obtener3D(self,entorno):
        codigoSalida=""
        retorno=RetornoType()
        s=Singleton.getInstance()

        if(self.tipo==TipoDato.I64 or self.tipo==TipoDato.F64):
            temp1=s.obtenerTemporal()
            codigoSalida+=f"{temp1} = {self.valor};\n"
            retorno.iniciarRetorno(codigoSalida,"",temp1,self.tipo)
            return retorno
        elif(self.tipo==TipoDato.STR):
            temp1=s.obtenerTemporal()
            codigoSalida+=f"{temp1} = HP;\n"

            for c in self.valor:
                codigo=ord(c)
                codigoSalida+=f"Heap[HP] = {codigo};\n"
                codigoSalida+=f"HP = HP + 1;\n"

            codigoSalida += f'Heap[HP] = 0;\n'
            codigoSalida += f'HP = HP+1;\n'
            retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.STR)
            return retorno

        elif(self.tipo==TipoDato.BOOL):
            temp1=s.obtenerTemporal()
            codigoSalida=""
            if self.valor:
                codigoSalida+=f"{temp1} = {1};\n"
            else:
                codigoSalida+=f"{temp1} = {0};\n"
            retorno.iniciarRetorno(codigoSalida,"",temp1,self.tipo)
            return retorno
        elif(self.tipo==TipoDato.CHAR):
            temp1=s.obtenerTemporal()
            codigoSalida=""
            codigo=ord(self.valor)
            codigoSalida+=f"{temp1} = {codigo};\n"
            retorno.iniciarRetorno(codigoSalida,"",temp1,self.tipo)
            return retorno
        return

        