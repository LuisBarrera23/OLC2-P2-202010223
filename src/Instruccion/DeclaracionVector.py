from hashlib import new
from src.Abstract.Instruccion import Instruccion
from src.Abstract.RetornoType import TipoDato,RetornoType

from src.Symbol.VectorInstancia import VectorInstancia

from src.Symbol.Error import Error
from src.PatronSingleton.Singleton import Singleton

from src.Symbol.Symbol import Simbolo
from src.Expresion.dimensionA import Dimension

class DeclaracionVector(Instruccion):

    def __init__(self,idInstancia, expresion, linea, columna,dimensiones=None,mutable=False,tipo=TipoDato.ERROR):
        self.idInstancia = idInstancia
        self.dimensiones = dimensiones
        self.expresion = expresion
        self.linea=linea
        self.columna=columna
        self.mutable=mutable
        self.tipo=tipo

        self.expresionCompilada=None
        self.puntero_entornoN=""
        self.ejecuta_en_funcion=False


    def Ejecutar(self, entorno):
        codigoSalida=""
        s=Singleton.getInstance()
        
        expresionVector:RetornoType() = None
        if self.expresion is not None:
            expresionVector:RetornoType=self.expresion.obtener3D(entorno)
        elif self.expresionCompilada is not None:
            expresionVector=self.expresionCompilada

        punteroEntorno="SP"
        if self.ejecuta_en_funcion:
            punteroEntorno=self.puntero_entornoN

        if expresionVector.tipo != TipoDato.VECTOR:
            raise Exception(s.addError(Error(f"La expresion necesita ser un vector",self.linea,self.columna)))
        if expresionVector.tipo==TipoDato.VECTOR:
            if self.tipo==TipoDato.ERROR and self.expresion.tipodeclaracion==1:
                expresionVector.tipo=expresionVector.valor.tipo
            else:
                expresionVector.tipo=self.tipo
        
        if self.dimensiones==None:
            #print("sin dimensiones especificadas")
            objetoVector:VectorInstancia = expresionVector.valor
            if entorno.existeSimboloEnEntornoActual(self.idInstancia):
                raise Exception(s.addError(Error(f"Variable ya existente con el nombre {self.idInstancia}",self.linea,self.columna)))

            temp1=s.obtenerTemporal()
            codigoSalida+="/* DECLARACION VECTOR */\n"
            codigoSalida += expresionVector.codigo
            codigoSalida += f"{temp1} = {punteroEntorno} + {entorno.tamaño};\n"
            codigoSalida += f"Stack[(int){temp1}] = {expresionVector.temporal};\n"


            objetoVector.identificador = self.idInstancia
            objetoVector.editable=self.mutable
            objetoVector.direccionRelativa=entorno.tamaño
            objetoVector.tipo=expresionVector.tipo
            

            
            
            entorno.agregarSimbolo(objetoVector)
            return codigoSalida

        else:
            #print("con dimensiones especificadas")
            Dimensiones:Dimension=self.dimensiones

            objetoVector:VectorInstancia = expresionVector.valor
            if entorno.existeSimboloEnEntornoActual(self.idInstancia):
                raise Exception(s.addError(Error(f"Variable ya existente con el nombre {self.idInstancia}",self.linea,self.columna)))
            if objetoVector.tipo!=Dimensiones.tipo:
                raise Exception(s.addError(Error(f"Tipo de datos no coinciden",self.linea,self.columna)))
            if len(Dimensiones.dimensiones)!=len(objetoVector.dimensiones):
                raise Exception(s.addError(Error(f"Las dimensiones no son iguales con la expresion",self.linea,self.columna)))
            temp1=s.obtenerTemporal()
            codigoSalida+="/* DECLARACION VECTOR */\n"
            codigoSalida += expresionVector.codigo
            codigoSalida += f"{temp1} = SP + {entorno.tamaño};\n"
            codigoSalida += f"Stack[(int){temp1}] = {expresionVector.temporal};\n"


            objetoVector.identificador = self.idInstancia
            objetoVector.editable=self.mutable
            objetoVector.direccionRelativa=entorno.tamaño
            entorno.agregarSimbolo(objetoVector)
            return codigoSalida
        
