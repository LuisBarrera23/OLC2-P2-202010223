
from src.Symbol.VectorInstancia import VectorInstancia
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import TipoDato,RetornoType

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Expresion.AccesoSimbolo import AccesoSimbolo

from src.Symbol.Symbol import Simbolo


class Contains(Expresion):
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

            codigoSalida="/* CONTAINS VECTOR */\n"
            s=Singleton.getInstance()
            temporalPosicion=s.obtenerTemporal()
            temporalactual=s.obtenerTemporal()
            temporalResultado=s.obtenerTemporal()

            etqCiclo=s.obtenerEtiqueta()
            etqCiclo1=s.obtenerEtiqueta()
            etqVerdadera=s.obtenerEtiqueta()
            etqFalsa=s.obtenerEtiqueta()
            
            temp1=s.obtenerTemporal()
            temp2=s.obtenerTemporal()
            temp3=s.obtenerTemporal()
            temp4=s.obtenerTemporal()
            

            codigoSalida += f"{temp1} = SP + {vector.direccionRelativa};\n"
            codigoSalida += f"{temporalPosicion} = Stack[(int){temp1}]; \n"

            codigoSalida += f"{temp2} = Heap[(int){temporalPosicion}];//valor len\n" 

            codigoSalida += f"{temp3} = {temporalPosicion} + 2; //pos datos\n" 
            
            valor=self.expresion2.obtener3D(entorno)
            codigoSalida+=valor.codigo
            codigoSalida += f"{temporalResultado} = 0;// resultado\n"
            codigoSalida += f"{temp4} = 0;// iterador\n"

            codigoSalida+=f"{etqCiclo}:\n"
            codigoSalida +=f"if({temp4} < {temp2}) goto {etqVerdadera};\n"
            codigoSalida +=f"goto {etqFalsa};\n"

            codigoSalida+=f"{etqVerdadera}:\n"
            codigoSalida+=f"{temporalactual} = Heap[(int){temp3}];\n"

            if vector.tipo==TipoDato.STR or vector.tipo==TipoDato.STRING:
                etq1=s.obtenerEtiqueta()
                etq2=s.obtenerEtiqueta()
                caracter1=s.obtenerTemporal()
                caracter2=s.obtenerTemporal()
                temp8=s.obtenerTemporal()
                temp9=s.obtenerTemporal()

                codigoSalida += "/* COMPARANDO UN VALOR CADENA STRING*/\n"
                codigoSalida +=f"{temp8} = {temporalactual};\n"
                codigoSalida +=f"{temp9} = {valor.temporal};\n"
                codigoSalida +=f"{etqCiclo1}:\n"
                codigoSalida +=f"{caracter1} = Heap[(int){temp8}];\n"
                codigoSalida +=f"{caracter2} = Heap[(int){temp9}];\n"

                codigoSalida +=f"if({caracter1} == 0) goto {etq1};\n"
                codigoSalida +=f"if({caracter1} != {caracter2}) goto {etq2};\n"
                codigoSalida +=f"   {temp8} = {temp8} + 1;\n"
                codigoSalida +=f"   {temp9} = {temp9} + 1;\n"
                codigoSalida +=f"   goto {etqCiclo1};\n"
                codigoSalida +=f"{etq2}:\n"
                codigoSalida+=f"{temp3} = {temp3} + 1;\n"
                codigoSalida+=f"{temp4} = {temp4} + 1;\n"
                codigoSalida +=f"goto {etqCiclo};\n"

                codigoSalida +=f"{etq1}:\n"
                codigoSalida +=f"{temporalResultado} = 1;\n"
                codigoSalida +=f"goto {etqFalsa};\n"
            else:
                etq1=s.obtenerEtiqueta()
                etq2=s.obtenerEtiqueta()
                codigoSalida +=f"if({temporalactual} != {valor.temporal}) goto {etq1};\n"
                codigoSalida += f"{temporalResultado} = 1;\n"
                codigoSalida +=f"goto {etqFalsa};\n"
                codigoSalida +=f"{etq1}:\n"
            
            codigoSalida+=f"{temp3} = {temp3} + 1;\n"
            codigoSalida+=f"{temp4} = {temp4} + 1;\n"
            codigoSalida +=f"goto {etqCiclo};\n"

        
            codigoSalida+=f"{etqFalsa}:\n"

            retorno=RetornoType()
            retorno.iniciarRetorno(codigoSalida,"",temporalResultado,TipoDato.BOOL)
            vector.dimensiones[0]=vector.dimensiones[0]-1
            return retorno
    
