
from src.Abstract.Instruccion import Instruccion
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import TipoDato,RetornoType

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error



from src.Symbol.Symbol import Simbolo
from src.Expresion.VectorContenido import VectorContenido,VectorInstancia
from src.Expresion.AccesoVector import AccesoVector
from src.Expresion.AccesoSimbolo import AccesoSimbolo
from src.Expresion.Capacity import Capacity
from src.Expresion.Primitivo import Primitivo


class Insert(Instruccion):
    def __init__(self,id,expresion1,expresion2,linea,columna) -> None:
        self.id=id
        self.expresion1:Expresion=expresion1
        self.expresion2:Expresion=expresion2
        self.linea=linea
        self.columna=columna
        
    def Ejecutar(self, entorno):
        s=Singleton.getInstance()
        temporalPosicion=s.obtenerTemporal()
        temporalLargo=s.obtenerTemporal()
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
        temp9=s.obtenerTemporal()
        temp10=s.obtenerTemporal()
        temp11=s.obtenerTemporal()

        codigoSalida="/* INSERT VECTOR */\n"

        if entorno.existeSimbolo(self.id)==False:
            raise Exception(s.addError(Error(f"Vector no existe",self.linea,self.columna)))
        vector:Simbolo=entorno.obtenerSimbolo(self.id)
        if isinstance(vector,VectorInstancia) is False:
            raise Exception(s.addError(Error(f"insert es solo para vectores",self.linea,self.columna)))
        
        
        #realizando copia del vector
        codigoSalida += f"{temp1} = SP + {vector.direccionRelativa};\n"
        codigoSalida += f"{temp2} = Stack[(int){temp1}]; \n"

        codigoSalida+=f"{temporalPosicion} = HP;//nueva posicion del vector en el heap\n"
        codigoSalida+=f"HP = HP + {vector.dimensiones[0]+3};//reservacion del espacio del nuevo vector\n"
        
        codigoSalida += f"{temp3} = Heap[(int){temp2}];\n" 
        codigoSalida += f"{temp3} = {temp3} + 1;\n" 
        codigoSalida+=f"Heap[(int){temporalPosicion}] = {temp3};//largo del vector nuevo\n"
        codigoSalida+=f"{temporalLargo} = Heap[(int){temporalPosicion}];//largo del vector nuevo\n"
        
        codigoSalida += f"{temp4} = {temp2} + 1; //pos anterior del capacity vector viejo\n" 
        codigoSalida += f"{temp5} = Heap[(int){temp4}];// valor capacity vector viejo\n" 
        codigoSalida += f"{temp6} = {temporalPosicion} + 1;\n"
        codigoSalida+=f"Heap[(int){temp6}] = {temp5};//capacidad del vector nuevo\n"
        
        
        codigoSalida += f"{temp7} = {temp2} + 2; //pos datos viejos\n" 
        codigoSalida += f"{temp8} = {temporalPosicion} + 2; //inicio datos nuevos\n"

        pos=self.expresion1.obtener3D(entorno)
        valor=self.expresion2.obtener3D(entorno)
        codigoSalida+=pos.codigo
        codigoSalida+=valor.codigo
        codigoSalida += f"{temp9} = 0;// iterador\n"
        codigoSalida+=f"{etqCiclo}:\n"
        codigoSalida +=f"if({temp9} < {temporalLargo}) goto {etqVerdadera};\n"
        codigoSalida +=f"goto {etqFalsa};\n"
        codigoSalida+=f"{etqVerdadera}:\n"
        codigoSalida +=f"if({temp9} == {pos.temporal}) goto {etqVerdadera1};\n"
        codigoSalida +=f"goto {etqFalsa1};\n"


        codigoSalida+=f"{etqVerdadera1}:\n"
        #codigoSalida += f'printf(\"%d\", (int){temp9}); \n'
        codigoSalida+=f"Heap[(int){temp8}] = {valor.temporal};\n"
        codigoSalida+=f"{temp8} = {temp8} + 1;\n"
        codigoSalida+=f"{temp9} = {temp9} + 1;\n"
        codigoSalida +=f"goto {etqCiclo};\n"

        codigoSalida+=f"{etqFalsa1}:\n"
        codigoSalida +=f"{temp10} = Heap[(int){temp7}];\n"
        codigoSalida+=f"{temp7} = {temp7} + 1;\n"
        codigoSalida+=f"Heap[(int){temp8}] = {temp10};\n"
        codigoSalida+=f"{temp8} = {temp8} + 1;\n"
        codigoSalida+=f"{temp9} = {temp9} + 1;\n"
        codigoSalida +=f"goto {etqCiclo};\n"
       
        codigoSalida+=f"{etqFalsa}:\n"






        codigoSalida += f"{temp11} = SP + {vector.direccionRelativa};\n"
        codigoSalida += f"Stack[(int){temp11}] = {temporalPosicion}; //nueva ubicacion del vector\n"
        vector.dimensiones[0]=vector.dimensiones[0]+1

        
        
        
        return codigoSalida
        