from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import RetornoType,TipoDato

from src.Symbol.Error import Error
from src.PatronSingleton.Singleton import Singleton
from src.Symbol.VectorInstancia import VectorInstancia

class VectorContenido(Expresion):
    def __init__(self,tipodeclaracion, expresiones,linea,columna,capacidad=999,repeticiones=0):
        self.tipodeclaracion=tipodeclaracion
        self.expresiones=expresiones
        self.linea=linea
        self.columna=columna
        self.capacidad=capacidad
        self.repeticiones=repeticiones

        self.aux1=None

    def obtener3D(self, entorno) -> RetornoType:
        s=Singleton.getInstance()
        if self.tipodeclaracion==1:
            codigoSalida=""
            dimensiones = []
            temporalPosicion=s.obtenerTemporal()
            temp=s.obtenerTemporal()
            
            codigoSalida+=f"{temporalPosicion} = HP;//posicion del vector en el heap\n"
            
            expresionesEjecutadas=self.ejecutarExpresiones(entorno)

            dimensiones.append(len(expresionesEjecutadas))
            codigoSalida+=f"HP = HP + {len(expresionesEjecutadas)+2};\n"
            codigoSalida+=f"Heap[(int){temporalPosicion}] = {len(expresionesEjecutadas)};//largo del vector\n"
            codigoSalida += f"{temp} = {temporalPosicion} + 1;\n"
            codigoSalida+=f"Heap[(int){temp}] = {len(expresionesEjecutadas)};//capacidad del arreglo\n"
            
            iterador=2
            for e in expresionesEjecutadas:
                if e.tipo==TipoDato.VECTOR:
                    codigoSalida += "/* referencia a un sub-vector */\n"
                    codigoSalida += e.codigo
                    codigoSalida += f"{temp} = {temporalPosicion} + {iterador};\n"
                    codigoSalida += f"Heap[(int){temp}] = {e.temporal};\n"
                    if iterador==2:
                        dimensiones.extend(e.valor.dimensiones)
                else:
                    codigoSalida += "/* almacenando valor cualquiera en el vector */\n"
                    codigoSalida += e.codigo
                    codigoSalida += f"{temp} = {temporalPosicion} + {iterador};\n"
                    codigoSalida += f"Heap[(int){temp}] = {e.temporal};\n"
                iterador+=1

            nuevaInstancia=VectorInstancia(self.tipo,dimensiones,[])
            nuevaInstancia.capacidad=len(expresionesEjecutadas)
            retorno=RetornoType()
            retorno.iniciarRetornoVector(codigoSalida,temporalPosicion,TipoDato.VECTOR,nuevaInstancia)
            return retorno

        elif self.tipodeclaracion==2:
            codigoSalida=""
            dimensiones = []
            temporalPosicion=s.obtenerTemporal()
            temp=s.obtenerTemporal()

            codigoSalida+=f"{temporalPosicion} = HP;//posicion del vector en el heap\n"
            
            expresion=self.expresiones.obtener3D(entorno)
            repeticiones=self.repeticiones.valor
            self.tipo=expresion.tipo
            dimensiones.append(repeticiones)
            codigoSalida+=f"HP = HP + {repeticiones+2};\n"
            codigoSalida+=f"Heap[(int){temporalPosicion}] = {repeticiones};//largo del vector\n"
            codigoSalida += f"{temp} = {temporalPosicion} + 1;\n"
            codigoSalida+=f"Heap[(int){temp}] = {repeticiones};//capacidad del arreglo\n"

            codigoSalida += expresion.codigo
            for e in range(repeticiones):
                codigoSalida += "/* almacenando valor cualquiera en el vector */\n"
                codigoSalida += f"{temp} = {temporalPosicion} + {e+2};\n"
                codigoSalida += f"Heap[(int){temp}] = {expresion.temporal};\n"

            nuevaInstancia=VectorInstancia(self.tipo,dimensiones,[])
            nuevaInstancia.capacidad=repeticiones
            retorno=RetornoType()
            retorno.iniciarRetornoVector(codigoSalida,temporalPosicion,TipoDato.VECTOR,nuevaInstancia)
            return retorno

        elif self.tipodeclaracion==3:
            codigoSalida=""
            dimensiones = []
            temporalPosicion=s.obtenerTemporal()
            temp=s.obtenerTemporal()

            codigoSalida+=f"{temporalPosicion} = HP;//posicion del vector en el heap\n"
            
            dimensiones.append(0)
            codigoSalida+=f"HP = HP + 2;\n"
            codigoSalida+=f"Heap[(int){temporalPosicion}] = 0;//largo del vector\n"
            codigoSalida += f"{temp} = {temporalPosicion} + 1;\n"
            codigoSalida+=f"Heap[(int){temp}] = 0;//capacidad del arreglo\n"

            nuevaInstancia=VectorInstancia(TipoDato.VECTOR,dimensiones,[])
            retorno=RetornoType()
            retorno.iniciarRetornoVector(codigoSalida,temporalPosicion,TipoDato.VECTOR,nuevaInstancia)
            return retorno

        elif self.tipodeclaracion==4:
            codigoSalida=""
            dimensiones = []
            temporalPosicion=s.obtenerTemporal()
            temp=s.obtenerTemporal()

            codigoSalida+=f"{temporalPosicion} = HP;//posicion del vector en el heap\n"
            
            dimensiones.append(0)
            codigoSalida+=f"HP = HP + 2;\n"
            codigoSalida+=f"Heap[(int){temporalPosicion}] = 0;//largo del vector\n"
            capacidad=self.expresiones.obtener3D(entorno)
            codigoSalida+=capacidad.codigo
            codigoSalida += f"{temp} = {temporalPosicion} + 1;\n"
            codigoSalida+=f"Heap[(int){temp}] = {capacidad.temporal};//capacidad del arreglo\n"

            nuevaInstancia=VectorInstancia(TipoDato.VECTOR,dimensiones,[])
            retorno=RetornoType()
            retorno.iniciarRetornoVector(codigoSalida,temporalPosicion,TipoDato.VECTOR,nuevaInstancia)
            return retorno

        elif self.tipodeclaracion==5:#para el push
            codigoSalida=""
            dimensiones = []
            temporalPosicion=s.obtenerTemporal()
            temp=s.obtenerTemporal()
            capacidad=self.aux1.obtener3D(entorno)
            codigoSalida+=f"{temporalPosicion} = HP;//posicion del vector en el heap\n"
            
            expresionesEjecutadas=self.ejecutarExpresiones(entorno)

            

            dimensiones.append(len(expresionesEjecutadas))
            codigoSalida+=f"HP = HP + {len(expresionesEjecutadas)+2};\n"
            codigoSalida+=f"Heap[(int){temporalPosicion}] = {len(expresionesEjecutadas)};//largo del vector\n"
            codigoSalida += f"{temp} = {temporalPosicion} + 1;\n"
            codigoSalida+=capacidad.codigo
            codigoSalida+=f"Heap[(int){temp}] = {capacidad.temporal};//capacidad del arreglo\n"
            
            iterador=2
            for e in expresionesEjecutadas:
                if e.tipo==TipoDato.VECTOR:
                    codigoSalida += "/* referencia a un sub-vector */\n"
                    codigoSalida += e.codigo
                    codigoSalida += f"{temp} = {temporalPosicion} + {iterador};\n"
                    codigoSalida += f"Heap[(int){temp}] = {e.temporal};\n"
                    if iterador==2:
                        dimensiones.extend(e.valor.dimensiones)
                else:
                    codigoSalida += "/* almacenando valor cualquiera en el vector */\n"
                    codigoSalida += e.codigo
                    codigoSalida += f"{temp} = {temporalPosicion} + {iterador};\n"
                    codigoSalida += f"Heap[(int){temp}] = {e.temporal};\n"
                iterador+=1

            nuevaInstancia=VectorInstancia(self.tipo,dimensiones,[])
            nuevaInstancia.capacidad=len(expresionesEjecutadas)
            retorno=RetornoType()
            retorno.iniciarRetornoVector(codigoSalida,temporalPosicion,TipoDato.VECTOR,nuevaInstancia)
            return retorno



    def ejecutarExpresiones(self,entorno):
        s=Singleton.getInstance()
        expresiones=[]
        iterador=0
        for e in self.expresiones:
            RetornoResultado=e.obtener3D(entorno)
            if iterador==0:
                if isinstance(e,VectorContenido):
                    self.tipo=RetornoResultado.valor.tipo
                else:
                    self.tipo=RetornoResultado.tipo
            else:
                if isinstance(e,VectorContenido):
                    if self.tipo!=RetornoResultado.valor.tipo:
                        raise Exception(s.addError(Error(f"Tipo de datos no coinciden en el arreglo",self.linea,self.columna)))
                else:
                    if self.tipo!=RetornoResultado.tipo:
                        raise Exception(s.addError(Error(f"Tipo de datos no coinciden en el arreglo",self.linea,self.columna)))

            iterador+=1
            expresiones.append(RetornoResultado)
        return expresiones


        