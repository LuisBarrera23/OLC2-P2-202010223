from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import RetornoType,TipoDato
from src.Symbol.ArrayInstancia import ArrayInstancia

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error


class ArrayContenido(Expresion):

    def __init__(self, listaExpresiones,linea, columna):
        self.expresiones = listaExpresiones
        self.linea=linea
        self.columna=columna

    def obtener3D(self, entorno) -> RetornoType:
        codigoSalida=""
        dimensiones = []
        s=Singleton.getInstance()
        temporalPosicion=s.obtenerTemporal()
        temp=s.obtenerTemporal()

        codigoSalida+=f"{temporalPosicion} = HP;//posicion del arreglo en el heap\n"
        
        expresionesEjecutadas=self.ejecutarExpresiones(entorno)

        dimensiones.append(len(expresionesEjecutadas))
        codigoSalida+=f"HP = HP + {len(expresionesEjecutadas)+1};\n"
        codigoSalida+=f"Heap[(int){temporalPosicion}] = {len(expresionesEjecutadas)};//largo del arreglo\n"
        iterador=1

        for e in expresionesEjecutadas:
            if e.tipo==TipoDato.ARREGLO:
                codigoSalida += "/* referencia a un sub-arreglo */\n"
                codigoSalida += e.codigo
                codigoSalida += f"{temp} = {temporalPosicion} + {iterador};\n"
                codigoSalida += f"Heap[(int){temp}] = {e.temporal};\n"
                if iterador==1:
                    dimensiones.extend(e.valor.dimensiones)
            else:
                codigoSalida += "/* almacenando valor cualquiera */\n"
                codigoSalida += e.codigo
                codigoSalida += f"{temp} = {temporalPosicion} + {iterador};\n"
                codigoSalida += f"Heap[(int){temp}] = {e.temporal};\n"
            iterador+=1
        
        nuevaInstancia=ArrayInstancia(self.tipo,dimensiones,[])
        retorno=RetornoType()
        retorno.iniciarRetornoArray(codigoSalida,temporalPosicion,TipoDato.ARREGLO,nuevaInstancia)
        return retorno

    def ejecutarExpresiones(self,entorno):
        s=Singleton.getInstance()
        expresiones=[]
        iterador=0
        for e in self.expresiones:
            RetornoResultado=e.obtener3D(entorno)
            if iterador==0:
                if isinstance(e,ArrayContenido):
                    self.tipo=RetornoResultado.valor.tipo
                else:
                    self.tipo=RetornoResultado.tipo
            else:
                if isinstance(e,ArrayContenido):
                    if self.tipo!=RetornoResultado.valor.tipo:
                        raise Exception(s.addError(Error(f"Tipo de datos no coinciden en el arreglo",self.linea,self.columna)))
                else:
                    if self.tipo!=RetornoResultado.tipo:
                        raise Exception(s.addError(Error(f"Tipo de datos no coinciden en el arreglo",self.linea,self.columna)))

            iterador+=1
            expresiones.append(RetornoResultado)
        return expresiones