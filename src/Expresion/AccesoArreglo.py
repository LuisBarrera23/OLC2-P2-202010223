
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import RetornoType,TipoDato
from src.Symbol.ArrayInstancia import ArrayInstancia

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Symbol.Symbol import Simbolo
from src.Symbol.ArrayInstancia import ArrayInstancia

class AccesoArreglo(Expresion):
    def __init__(self, idArreglo, listaExpresiones, linea, columna):
        self.idArreglo = idArreglo
        self.listaExpresiones = listaExpresiones
        self.linea=linea
        self.columna=columna

    def obtener3D(self, entorno) -> RetornoType:
        s=Singleton.getInstance()
        arreglo:Simbolo = entorno.obtenerSimbolo(self.idArreglo)
        if entorno.existeSimboloEnEntornoActual(self.idArreglo) is not True:
            raise Exception(s.addError(Error(f"Arreglo {self.idArreglo} no existe",self.linea,self.columna)))

        arreglo:Simbolo = entorno.obtenerSimbolo(self.idArreglo)
        if isinstance(arreglo,ArrayInstancia) is False:
            raise Exception(s.addError(Error(f"Arreglo {self.id} no existe",self.linea,self.columna)))

        temp1=s.obtenerTemporal()
        temp2=s.obtenerTemporal()
        etqSalida=s.obtenerEtiqueta()

        codigoSalida=""
        codigoSalida += "/* ACCESO A UN ARREGLO */\n"
        codigoSalida += f"{temp1} = SP + {arreglo.direccionRelativa};\n"
        codigoSalida += f"{temp2} = Stack[(int) {temp1}]; \n"
        
        indices=self.EjecutarDimensiones(entorno)
        for i in indices:
            codigoSalida+=i.codigo

        valor=self.Acceso(indices,temp2,etqSalida,entorno)
        codigoSalida += valor.codigo
        codigoSalida+= f"{etqSalida}:\n"

        retorno=RetornoType()
        retorno.iniciarRetorno(codigoSalida,"",valor.temporal,arreglo.tipo)
        return retorno


    def Acceso(self,dimensiones,temporal,etqSalida,entorno):
        s=Singleton.getInstance()
        actual:RetornoType=dimensiones.pop(0)

        temp1=s.obtenerTemporal()
        temp2=s.obtenerTemporal()
        temp3=s.obtenerTemporal()
        temp4=s.obtenerTemporal()
        etqIncorrecto=s.obtenerEtiqueta()
        etqCorrecto=s.obtenerEtiqueta()

        codigoSalida=""
        codigoSalida += f"{temp1} = Heap[(int) {temporal}];//tamaño del arreglo\n "
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
        codigoSalida += f"{temp2} = {temporal} + 1;\n"
        codigoSalida += f"{temp3} = {temp2} + {actual.temporal};\n"
        codigoSalida += f"{temp4} = Heap[(int){temp3}];\n"


        retorno=RetornoType()
        if len(dimensiones)>0:
            resultado=self.Acceso(dimensiones,temp4,etqSalida,entorno)
            codigoSalida+=resultado.codigo
            retorno.iniciarRetorno(codigoSalida,"",resultado.temporal,None)
        else:
            
            retorno.iniciarRetorno(codigoSalida,"",temp4,None)

        return retorno

    def EjecutarDimensiones(self,entorno):
        s=Singleton.getInstance()
        dimensionesEjecutadas=[]
        for e in self.listaExpresiones:
            exp=e.obtener3D(entorno)
            dimensionesEjecutadas.append(exp)
            if exp.tipo!=TipoDato.I64:
                raise Exception(s.addError(Error(f"Para acceso se necesitan expresiones tipo I64 o USIZE",self.linea,self.columna)))
        return dimensionesEjecutadas

