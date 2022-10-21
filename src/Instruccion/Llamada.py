from src.Instruccion.Declaracion import Declaracion
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import RetornoType, TipoDato
from src.Abstract.Instruccion import Instruccion

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error
from src.Symbol.EntornoTabla import EntornoTabla
from src.Expresion.AccesoSimbolo import AccesoSimbolo

class Llamada(Instruccion,Expresion):
    def __init__(self,id, expresiones,linea, columna):
        self.id=id
        self.expresiones=expresiones
        self.linea=linea
        self.columna=columna

    def Ejecutar(self, entorno):
        codigo=self.obtener3D(entorno)
        return codigo.codigo

    def obtener3D(self,entorno) -> RetornoType:
        s=Singleton.getInstance()
        codigoSalida=""
        if entorno.existeFuncion(self.id) is False:
            raise Exception(s.addError(Error(f"Funcion {self.id} no existe",self.linea,self.columna)))
        
        funcion=entorno.obtenerFuncion(self.id)
        codigoSalida+=f"/* LLAMADA A FUNCION {self.id} */\n"
        codigoSalida+=self.verificarParametrosLlamada(entorno)
        nuevoEntorno=EntornoTabla(entorno)
        nuevoEntorno.tamaño=1

        nuevoPuntero=s.obtenerTemporal()
        
        codigoSalida += f"{nuevoPuntero} = SP + {entorno.tamaño};\n"
        codigoSalida +=funcion.EjecutarParametros(nuevoEntorno,entorno,nuevoPuntero,self.expresiones)
        self.generarFuncion(nuevoEntorno,funcion)
        codigoSalida += f"SP = SP + {entorno.tamaño};\n"
        
        
        codigoSalida += f"{self.id}();\n"
        

        codigoSalida += f"SP = SP - {entorno.tamaño};\n"
        temp1=s.obtenerTemporal()
        temp2=s.obtenerTemporal()
        codigoSalida += f"{temp1} = SP + {entorno.tamaño};\n"
        codigoSalida += f"{temp2} = Stack[(int){temp1}];\n"
        

        retorno=RetornoType()
        retorno.iniciarRetorno(codigoSalida,"",temp2,funcion.tipo)
        retorno.RetornoPos=temp1
        return retorno

    def generarFuncion(self,entorno,funcion):
        s=Singleton.getInstance()
        if funcion.generada:
            return
        funcion.generada=True
        entorno.actualizarFuncion(funcion)
        codigoSalida=funcion.Ejecutar(entorno)
        s.agregarFuncion(codigoSalida)
        
        

    
    def strTipo(self,tipo:TipoDato)->str:
        if tipo==TipoDato.I64:
            return "I64"
        elif tipo==TipoDato.F64:
            return "F64"
        elif tipo==TipoDato.BOOL:
            return "BOOL"
        elif tipo==TipoDato.CHAR:
            return "CHAR"
        elif tipo==TipoDato.STRING:
            return "STRING"
        elif tipo==TipoDato.STR:
            return "&STR"
        elif tipo==TipoDato.USIZE:
            return "USIZE"
        elif tipo==TipoDato.ARREGLO:
            return "ARREGLO"
        return ""
    
    def verificarParametrosLlamada(self,entorno):
        codigoSalida=""
        s=Singleton.getInstance()
        temp=s.obtenerTemporal()
        for i in range(len(self.expresiones)):
            if isinstance(self.expresiones[i],Llamada):
                DeclaracionFantasma=Declaracion(temp,self.expresiones[i],True,self.expresiones[i].linea,self.expresiones[i].columna)
                codigoSalida+=DeclaracionFantasma.Ejecutar(entorno)
                AccesoFantasma=AccesoSimbolo(temp,self.expresiones[i].linea,self.expresiones[i].columna)
                self.expresiones[i]=AccesoFantasma
        return codigoSalida

    
        
