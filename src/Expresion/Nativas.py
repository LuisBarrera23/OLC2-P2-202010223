from cmath import sqrt
import imp
from lib2to3.pgen2.token import STRING
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import TipoDato,RetornoType

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error


class Nativa(Expresion):
    def __init__(self,expresion,tipo,linea,columna) -> None:
        self.expresion:Expresion=expresion
        self.tipo=tipo
        self.linea=linea
        self.columna=columna
        
    def obtener3D(self, entorno) -> RetornoType:
        s=Singleton.getInstance()
        codigoSalida=""
        retorno=RetornoType()
        E1:RetornoType=self.expresion.obtener3D(entorno)
        #raise Exception(s.addError(Error(f"Se necesita un cadena para ejecutar to_string o to_owned",self.linea,self.columna)))
        if(self.tipo==1):
            if E1.tipo==TipoDato.I64 or E1.tipo==TipoDato.F64:
                etq=s.obtenerEtiqueta()
                codigoSalida += "/* Funcion Nativa ABS() */\n"
                codigoSalida += E1.codigo
                codigoSalida += f"if({E1.temporal} > 0) goto {etq};\n"
                codigoSalida += f"{E1.temporal} = {E1.temporal} * -1;\n"
                codigoSalida += f"{etq}:\n"
                retorno.iniciarRetorno(codigoSalida,"",E1.temporal,TipoDato.I64)
                return retorno
            else:
                raise Exception(s.addError(Error(f"Se necesita tipo de dato I64 o F64 para la funcion abs()",self.linea,self.columna)))
        elif self.tipo==2:
            if E1.tipo==TipoDato.I64 or E1.tipo==TipoDato.F64:
                raiz=s.obtenerTemporal()
                temp=s.obtenerTemporal()
                aux=s.obtenerTemporal()
                etqCiclo=s.obtenerEtiqueta()
                etqSalida=s.obtenerEtiqueta()

                codigoSalida += "/* Funcion Nativa ABS() */\n"
                codigoSalida += E1.codigo
                codigoSalida += f"{raiz} = {E1.temporal} / 2;\n"
                codigoSalida += f"{temp} = 0;\n"
                codigoSalida += f"{etqCiclo}:\n"
                codigoSalida += f"if({raiz} == {temp}) goto {etqSalida};\n"
                codigoSalida += f"  {temp} = {raiz};\n"
                codigoSalida += f"  {aux} = {E1.temporal} / {temp};\n"
                codigoSalida += f"  {aux} = {aux} + {temp};\n"
                codigoSalida += f"  {aux} = {aux} / 2;\n"
                codigoSalida += f"  {raiz} = {aux};\n"
                codigoSalida += f"  goto {etqCiclo};\n"


                codigoSalida += f"{etqSalida}:\n"
                retorno.iniciarRetorno(codigoSalida,"",raiz,TipoDato.I64)
                return retorno
            else:
                raise Exception(s.addError(Error(f"Se necesita tipo de dato I64 o F64 para la funcion sqrt()",self.linea,self.columna)))
        return retorno