
from cgi import print_arguments
from typing import List
from src.Abstract.RetornoType import RetornoType, TipoDato
from src.Abstract.Instruccion import Instruccion
from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Symbol.ArrayInstancia import ArrayInstancia

class Print(Instruccion):

    def __init__(self,expresion,linea,columna):
        self.expresion:List=expresion
        self.linea = linea
        self.columna = columna

    def Ejecutar(self, entorno):
        s=Singleton.getInstance()
        if len(self.expresion)==1:
            return self.imprimir(self.expresion[0],entorno)+"printf(\"%c\",(char)10);\n"
        else:
            codigoSalida=""
            self.expresion[0].esFormato=True
            exp=self.expresion[0].obtener3D(entorno)

            temp1=s.obtenerTemporal()
            temp2=s.obtenerTemporal()
            caracter=s.obtenerTemporal()
            etqCiclo=s.obtenerEtiqueta()
            etqSalida=s.obtenerEtiqueta()
            etqImpresion=s.obtenerEtiqueta()

            etq1=s.obtenerEtiqueta()
            etq2=s.obtenerEtiqueta()

            codigoSalida += "/* PRINTLN */\n"
            codigoSalida += exp.codigo
            codigoSalida +=f"{temp1} = {exp.temporal};\n"
            codigoSalida +=f"{temp2} = 1;\n"
            codigoSalida +=f"{etqCiclo}:\n"
            codigoSalida +=f"{caracter} = Heap[(int){temp1}];\n"

            codigoSalida +=f"if({caracter} == 0) goto {etqSalida};\n"
            codigoSalida +=f"   if({caracter} == 123) goto {etq1};\n"
            codigoSalida +=f"   goto {etq2};\n"
            codigoSalida +=f"   {etq1}:\n"
            codigoSalida +=f"       {temp1} = {temp1} + 2;\n"
            codigoSalida +=f"       goto {etqImpresion};\n"
            
            codigoSalida +=f"   {etq2}:\n"
            codigoSalida +=f"       printf(\"%c\",(char){caracter});\n"
            codigoSalida +=f"       {temp1} = {temp1} + 1;\n"
            codigoSalida +=f"       goto {etqCiclo};\n"

            codigoSalida +=f"{etqImpresion}:\n"
            codigoSalida += self.bloqueExpresiones(etqCiclo,temp2,entorno)
            codigoSalida +=f"   goto {etqCiclo};\n"

            codigoSalida +=f"{etqSalida}:\n"
            codigoSalida+="printf(\"%c\",(char)10);\n"
            return codigoSalida

    def bloqueExpresiones(self,etqCiclo,contador,entorno):
        s=Singleton.getInstance()
        codigoSalida=""
        for i in range(1,len(self.expresion)):
            etqSalida=s.obtenerEtiqueta()
            codigoSalida += f"if({contador} != {i}) goto {etqSalida};\n"
            codigoSalida += self.imprimir(self.expresion[i],entorno)
            codigoSalida += f"{contador} = {contador} + 1;\n"
            codigoSalida += f"   goto {etqCiclo};\n"
            codigoSalida += f"{etqSalida}:\n"
        return codigoSalida


    def imprimir(self,expresion,entorno):
        codigoSalida=""
        exp:RetornoType=expresion.obtener3D(entorno)
        s=Singleton.getInstance()

        if exp.tipo == TipoDato.I64:
            codigoSalida += "/* IMPRIMIENDO UN VALOR ENTERO*/\n"
            codigoSalida += exp.codigo
            codigoSalida += f'printf(\"%d\", (int){exp.temporal}); \n'
            return codigoSalida

        elif exp.tipo == TipoDato.F64:
            codigoSalida += "/* IMPRIMIENDO UN VALOR DECIMAL*/\n"
            codigoSalida += exp.codigo
            codigoSalida += f'printf(\"%f\", (float){exp.temporal}); \n'
            return codigoSalida
        elif exp.tipo == TipoDato.STR:
            temp1=s.obtenerTemporal()
            caracter=s.obtenerTemporal()
            etqCiclo=s.obtenerEtiqueta()
            etqSalida=s.obtenerEtiqueta()

            codigoSalida += "/* IMPRIMIENDO UN VALOR CADENA STR*/\n"
            codigoSalida += exp.codigo
            codigoSalida +=f"{temp1} = {exp.temporal};\n"
            codigoSalida +=f"{etqCiclo}:\n"
            codigoSalida +=f"{caracter} = Heap[(int){temp1}];\n"

            codigoSalida +=f"if({caracter} == 0) goto {etqSalida};\n"
            codigoSalida +=f"   printf(\"%c\",(char){caracter});\n"
            codigoSalida +=f"   {temp1} = {temp1} + 1;\n"
            codigoSalida +=f"   goto {etqCiclo};\n"

            codigoSalida +=f"{etqSalida}:\n"
            return codigoSalida

        elif exp.tipo == TipoDato.STRING:
            temp1=s.obtenerTemporal()
            caracter=s.obtenerTemporal()
            etqCiclo=s.obtenerEtiqueta()
            etqSalida=s.obtenerEtiqueta()

            codigoSalida += "/* IMPRIMIENDO UN VALOR CADENA STRING*/\n"
            codigoSalida += exp.codigo
            codigoSalida +=f"{temp1} = {exp.temporal};\n"
            codigoSalida +=f"{etqCiclo}:\n"
            codigoSalida +=f"{caracter} = Heap[(int){temp1}];\n"

            codigoSalida +=f"if({caracter} == 0) goto {etqSalida};\n"
            codigoSalida +=f"   printf(\"%c\",(char){caracter});\n"
            codigoSalida +=f"   {temp1} = {temp1} + 1;\n"
            codigoSalida +=f"   goto {etqCiclo};\n"

            codigoSalida +=f"{etqSalida}:\n"
            return codigoSalida

        elif exp.tipo == TipoDato.BOOL:
            codigoSalida += "/* IMPRIMIENDO UN VALOR BOOLEANO*/\n"
            codigoSalida += exp.codigo
            codigoSalida += f'printf(\"%d\", (int){exp.temporal}); \n'
            return codigoSalida
        
        elif exp.tipo == TipoDato.CHAR:
            codigoSalida += "/* IMPRIMIENDO UN VALOR CHAR*/\n"
            codigoSalida += exp.codigo
            codigoSalida += f'printf(\"%c\", (char){exp.temporal}); \n'
            return codigoSalida

