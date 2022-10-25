
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


class Push(Instruccion):
    def __init__(self,id,expresion2,linea,columna) -> None:
        self.id=id
        self.expresion2=expresion2
        self.linea=linea
        self.columna=columna
        
    def Ejecutar(self, entorno):
        s=Singleton.getInstance()
        temp1=s.obtenerTemporal()
        temp2=s.obtenerTemporal()
        codigoSalida="/* PUSH VECTOR */\n"

        if entorno.existeSimbolo(self.id)==False:
            raise Exception(s.addError(Error(f"Vector no existe",self.linea,self.columna)))
        vector:Simbolo=entorno.obtenerSimbolo(self.id)
        if isinstance(vector,VectorInstancia) is False:
            raise Exception(s.addError(Error(f"push es solo para vectores",self.linea,self.columna)))
        
        
        #realizando copia del vector
        expresiones=[]
        for i in range(vector.dimensiones[0]):
            indice=[]
            x=Primitivo(i,TipoDato.I64)
            indice.append(x)
            acceso=AccesoVector(vector.identificador,indice,self.linea,self.columna)
            expresiones.append(acceso) 
        expresiones.append(self.expresion2)
        nuevoVector=VectorContenido(5,expresiones,self.linea,self.columna)
        accesosimbolo=AccesoSimbolo(self.id,self.linea,self.columna)
        capacidad=Capacity(accesosimbolo,self.linea,self.columna)
        nuevoVector.aux1=capacidad
        retorno=nuevoVector.obtener3D(entorno)

        codigoSalida+=retorno.codigo
        codigoSalida += f"{temp1} = SP + {vector.direccionRelativa};\n"
        codigoSalida += f"Stack[(int){temp1}] = {retorno.temporal}; //nueva ubicacion del vector\n"
        vector.modificarDimension(retorno.valor.dimensiones)

        
        
        
        return codigoSalida
        