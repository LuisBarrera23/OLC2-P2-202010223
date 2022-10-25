
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import RetornoType,TipoDato

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Symbol.Symbol import Simbolo
from src.Symbol.VectorInstancia import VectorInstancia

class AccesoVector(Expresion):
    def __init__(self, idArreglo, listaExpresiones, linea, columna):
        self.idArreglo = idArreglo
        self.listaExpresiones = listaExpresiones
        self.linea=linea
        self.columna=columna
        
        self.asignacion=False
        self.len=False
        self.devuelve_arreglo=False

    def obtener3D(self, entorno) -> RetornoType:
        s=Singleton.getInstance()
        vector:Simbolo = entorno.obtenerSimbolo(self.idArreglo)
        if entorno.existeSimbolo(self.idArreglo) is not True:
            raise Exception(s.addError(Error(f"Vector {self.idArreglo} no existe",self.linea,self.columna)))

        if isinstance(vector,VectorInstancia) is False:
            raise Exception(s.addError(Error(f"Vector {self.id} no existe",self.linea,self.columna)))

        temp1=s.obtenerTemporal()
        temp2=s.obtenerTemporal()
        etqSalida=s.obtenerEtiqueta()

        codigoSalida=""
        codigoSalida += "/* ACCESO A UN VECTOR */\n"
        codigoSalida += f"{temp1} = SP + {vector.direccionRelativa};\n"
        codigoSalida += f"{temp2} = Stack[(int){temp1}]; \n"
        
        indices=self.EjecutarDimensiones(entorno)
        for i in indices:
            codigoSalida+=i.codigo
        valor=self.Acceso(indices,temp2,etqSalida,entorno,vector.dimensiones)
        codigoSalida += valor.codigo
        codigoSalida+= f"{etqSalida}:\n"
        

        
        retorno=RetornoType()
        if self.devuelve_arreglo:
            retorno.vector=True
        retorno.iniciarRetorno(codigoSalida,"",valor.temporal,vector.tipo)
        return retorno


    def Acceso(self,dimensiones,temporal,etqSalida,entorno,dimOriginales):
        s=Singleton.getInstance()
        actual:RetornoType=dimensiones.pop(0)

        temp1=s.obtenerTemporal()
        temp2=s.obtenerTemporal()
        temp3=s.obtenerTemporal()
        temp4=s.obtenerTemporal()
        etqIncorrecto=s.obtenerEtiqueta()
        etqCorrecto=s.obtenerEtiqueta()

        codigoSalida=""
        codigoSalida += f"{temp1} = Heap[(int) {temporal}];//tamaño del vector\n "
        codigoSalida += f" if ({actual.temporal} < 0) goto {etqIncorrecto};\n"
        codigoSalida += f" if ({actual.temporal} >= {temp1}) goto {etqIncorrecto};\n"
        codigoSalida += f"goto {etqCorrecto};\n"
        codigoSalida += f"{etqIncorrecto}:\n"
        codigoSalida +="printf(\"%c\", 66); //B\n"
        codigoSalida +="printf(\"%c\", 111); //o\n"
        codigoSalida +="printf(\"%c\", 117); //u\n"
        codigoSalida +="printf(\"%c\", 110); //n\n"
        codigoSalida +="printf(\"%c\", 100); //d\n"
        codigoSalida +="printf(\"%c\", 115); //s\n"
        codigoSalida +="printf(\"%c\", 69); //E\n"
        codigoSalida +="printf(\"%c\", 114); //r\n"
        codigoSalida +="printf(\"%c\", 114); //r\n"
        codigoSalida +="printf(\"%c\", 111); //o\n"
        codigoSalida +="printf(\"%c\\n\", 114); //r\n"
        codigoSalida +=f"goto {etqSalida};\n"   
        codigoSalida += f"{etqCorrecto}:\n"
        codigoSalida += f"{temp2} = {temporal} + 2;\n"
        codigoSalida += f"{temp3} = {temp2} + {actual.temporal};\n"
        codigoSalida += f"{temp4} = Heap[(int){temp3}];\n"


        retorno=RetornoType()
        if len(dimensiones)>0:
            resultado=self.Acceso(dimensiones,temp4,etqSalida,entorno,dimOriginales)
            codigoSalida+=resultado.codigo
            retorno.iniciarRetorno(codigoSalida,"",resultado.temporal,None)
        else:
            if self.asignacion:
                retorno.iniciarRetorno(codigoSalida,"",temp3,None)
            elif self.len:
                retorno.iniciarRetorno(codigoSalida,"",temp4,None)
            else:
                if (len(self.listaExpresiones)!= len(dimOriginales)):
                    print("el acceso devuelve un vector")
                    self.devuelve_arreglo=True
                    retorno.iniciarRetorno(codigoSalida,"",temp4,None)
                    return retorno
                retorno.iniciarRetorno(codigoSalida,"",temp4,None)

        return retorno

    def EjecutarDimensiones(self,entorno):
        s=Singleton.getInstance()
        dimensionesEjecutadas=[]
        for e in self.listaExpresiones:
            exp=e.obtener3D(entorno)
            dimensionesEjecutadas.append(exp)
            if exp.tipo!=TipoDato.I64 and exp.tipo!=TipoDato.USIZE:
                raise Exception(s.addError(Error(f"Para acceso se necesitan expresiones tipo I64 o USIZE",self.linea,self.columna)))
        return dimensionesEjecutadas

