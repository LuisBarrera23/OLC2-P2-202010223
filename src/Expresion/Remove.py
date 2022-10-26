
from src.Symbol.VectorInstancia import VectorInstancia
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import TipoDato,RetornoType

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Expresion.AccesoSimbolo import AccesoSimbolo
from src.Expresion.AccesoSimbolo import ArrayInstancia
from src.Expresion.AccesoArreglo import AccesoArreglo

from src.Symbol.Symbol import Simbolo


class Remove(Expresion):
    def __init__(self,expresion1,expresion2,linea,columna) -> None:
        self.expresion1:Expresion=expresion1
        self.expresion2:Expresion=expresion2
        self.linea=linea
        self.columna=columna
        
    def obtener3D(self, entorno):
        s=Singleton.getInstance()

        if isinstance(self.expresion1,AccesoSimbolo):
            if entorno.existeSimbolo(self.expresion1.id)==False:
                raise Exception(s.addError(Error(f"No existe arreglo con este ID",self.linea,self.columna)))
            vector:Simbolo=entorno.obtenerSimbolo(self.expresion1.id)
            if isinstance(vector,VectorInstancia) is False:
                raise Exception(s.addError(Error(f"remove es solo para vectores",self.linea,self.columna)))

            codigoSalida="/* REMOVE VECTOR */\n"
            s=Singleton.getInstance()
            temporalPosicion=s.obtenerTemporal()
            temporalRetorno=s.obtenerTemporal()
            etqCiclo=s.obtenerEtiqueta()
            etqVerdadera=s.obtenerEtiqueta()
            etqFalsa=s.obtenerEtiqueta()
            etqVerdadera1=s.obtenerEtiqueta()
            etqFalsa1=s.obtenerEtiqueta()
            temp1=s.obtenerTemporal()
            temp2=s.obtenerTemporal()
            temp3=s.obtenerTemporal()
            temp4=s.obtenerTemporal()
            temp5=s.obtenerTemporal()
            temp6=s.obtenerTemporal()
            temp7=s.obtenerTemporal()
            temp8=s.obtenerTemporal()

            codigoSalida += f"{temp1} = SP + {vector.direccionRelativa};\n"
            codigoSalida += f"{temporalPosicion} = Stack[(int){temp1}]; \n"

            codigoSalida += f"{temp2} = Heap[(int){temporalPosicion}];//valor len\n" 
            codigoSalida += f"{temp3} = {temp2} - 1;\n" 
            pos=self.expresion2.obtener3D(entorno)
            codigoSalida+=pos.codigo
            codigoSalida+=f"Heap[(int){temporalPosicion}] = {temp3};//largo del vector nuevo\n"

            codigoSalida += f"{temp4} = {temporalPosicion} + 2; //pos datos\n" 
            codigoSalida += f"{temp7} = {temporalPosicion} + 2; //pos pivote\n" 
            
            
            

            codigoSalida += f"{temp5} = 0;// iterador\n"

            codigoSalida+=f"{etqCiclo}:\n"
            codigoSalida +=f"if({temp5} < {temp2}) goto {etqVerdadera};\n"
            codigoSalida +=f"goto {etqFalsa};\n"
            codigoSalida+=f"{etqVerdadera}:\n"
            codigoSalida +=f"if({temp5} == {pos.temporal}) goto {etqVerdadera1};\n"
            codigoSalida +=f"goto {etqFalsa1};\n"


            codigoSalida+=f"{etqVerdadera1}:\n"
            codigoSalida+=f"{temporalRetorno} = Heap[(int){temp4}];\n" 
            codigoSalida+=f"{temp4} = {temp4} + 1;\n"
            codigoSalida += f"{pos.temporal} = -1;\n"
            #codigoSalida+=f"{temp5} = {temp5} + 1;\n"
            codigoSalida +=f"goto {etqCiclo};\n"

            codigoSalida+=f"{etqFalsa1}:\n"
            codigoSalida+=f"{temp6} = Heap[(int){temp4}];\n" 
            codigoSalida+=f"{temp8} = {temp7} + {temp5};\n"
            codigoSalida+=f"Heap[(int){temp8}] = {temp6};\n"
            codigoSalida+=f"{temp4} = {temp4} + 1;\n"
            codigoSalida+=f"{temp5} = {temp5} + 1;\n"
            codigoSalida +=f"goto {etqCiclo};\n"
        
            codigoSalida+=f"{etqFalsa}:\n"

            retorno=RetornoType()
            retorno.iniciarRetorno(codigoSalida,"",temporalRetorno,vector.tipo)
            vector.dimensiones[0]=vector.dimensiones[0]-1
            return retorno