from src.Abstract.Instruccion import Instruccion
from src.Abstract.RetornoType import RetornoType, TipoDato

from src.Symbol.ArrayInstancia import ArrayInstancia

from src.Symbol.Error import Error
from src.PatronSingleton.Singleton import Singleton
from src.Expresion.dimensionA import Dimension


class DeclaracionArreglo(Instruccion):

    def __init__(self,idInstancia, expresion, linea, columna,dimensiones=None,mutable=False):
        self.idInstancia = idInstancia
        self.dimensiones = dimensiones
        self.expresion = expresion
        self.linea=linea
        self.columna=columna
        self.mutable=mutable

        self.expresionCompilada=None
        self.puntero_entornoN=""
        self.ejecuta_en_funcion=False

    def Ejecutar(self, entorno):
        codigoSalida=""
        s=Singleton.getInstance()
        
        expresionArreglo:RetornoType() = None
        if self.expresion is not None:
            expresionArreglo:RetornoType=self.expresion.obtener3D(entorno)
        elif self.expresionCompilada is not None:
            expresionArreglo=self.expresionCompilada

        punteroEntorno="SP"
        if self.ejecuta_en_funcion:
            punteroEntorno=self.puntero_entornoN

        if expresionArreglo.tipo != TipoDato.ARREGLO:
            raise Exception(s.addError(Error(f"La expresion necesita ser un arreglo",self.linea,self.columna)))
        if self.dimensiones==None:
            #print("sin dimensiones especificadas")
            objetoArreglo:ArrayInstancia = expresionArreglo.valor
            if entorno.existeSimboloEnEntornoActual(self.idInstancia):
                raise Exception(s.addError(Error(f"Variable ya existente con el nombre {self.idInstancia}",self.linea,self.columna)))

            temp1=s.obtenerTemporal()
            codigoSalida+="/* DECLARACION ARREGLO */\n"
            codigoSalida += expresionArreglo.codigo
            codigoSalida += f"{temp1} = {punteroEntorno} + {entorno.tamaño};\n"
            codigoSalida += f"Stack[(int){temp1}] = {expresionArreglo.temporal};\n"


            objetoArreglo.identificador = self.idInstancia
            objetoArreglo.editable=self.mutable
            objetoArreglo.direccionRelativa=entorno.tamaño
            entorno.agregarSimbolo(objetoArreglo)
            return codigoSalida
        else:
            #print("con dimensiones especificadas")
            Dimensiones:Dimension=self.dimensiones

            objetoArreglo:ArrayInstancia = expresionArreglo.valor
            if entorno.existeSimboloEnEntornoActual(self.idInstancia):
                raise Exception(s.addError(Error(f"Variable ya existente con el nombre {self.idInstancia}",self.linea,self.columna)))
            if objetoArreglo.tipo!=Dimensiones.tipo:
                raise Exception(s.addError(Error(f"Tipo de datos no coinciden",self.linea,self.columna)))
            if len(Dimensiones.dimensiones)!=len(objetoArreglo.dimensiones):
                raise Exception(s.addError(Error(f"Las dimensiones no son iguales con la expresion",self.linea,self.columna)))
            temp1=s.obtenerTemporal()
            codigoSalida+="/* DECLARACION ARREGLO */\n"
            codigoSalida += expresionArreglo.codigo
            codigoSalida += f"{temp1} = SP + {entorno.tamaño};\n"
            codigoSalida += f"Stack[(int){temp1}] = {expresionArreglo.temporal};\n"


            objetoArreglo.identificador = self.idInstancia
            objetoArreglo.editable=self.mutable
            objetoArreglo.direccionRelativa=entorno.tamaño
            entorno.agregarSimbolo(objetoArreglo)
            return codigoSalida