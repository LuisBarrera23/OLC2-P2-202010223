from pickle import FALSE
from re import S
from src.Abstract.RetornoType import TipoDato

class Simbolo:

    def __init__(self):
        #PARA SIMBOLOS PRIMITIVOS
        self.identificador=""
        self.valor=None
        self.tipo= TipoDato.ERROR
        self.editable=False
        self.direccionRelativa=0
        self.linea=0
        self.columna=0

        #EXTRA PARA FUNCIONES
        self.parametros=[]
        self.instrucciones=[]

        #EXTRA PARA ARREGLOS
        self.valores=[]
        self.dimensiones=[]
        
        #EXTRA PARA VECTORES
        self.punteroReferencia=""
        self.nombreAnterior=""
        self.aux1=False

        
    def Simbolo_primitivo(self, id, valor,tipo,linea, columna,direccionRelativa, editable=False):
        self.identificador=id
        self.valor=valor
        self.tipo=tipo
        self.linea=linea
        self.columna=columna
        self.direccionRelativa=direccionRelativa
        self.editable=editable
    
    def Simbolo_funcion(self, identificador, parametros, instrucciones,linea,columna, tipo=None):
        self.identificador=identificador
        self.parametros=parametros
        self.instrucciones=instrucciones
        self.tipo=tipo
        self.linea=linea
        self.columna=columna

    def Simbolo_arreglo(self,tipo, dimensiones, valores):
        self.tipo=tipo
        self.dimensiones=dimensiones
        self.valores=valores
        self.editable=False

    def Simbolo_vector(self,identificador,dimensiones,valoresInstancia,capacidad,tipo,editable=False):
        self.identificador=identificador
        self.dimensiones=dimensiones
        self.valores=valoresInstancia
        self.editable=editable
        self.capacidad=capacidad
        self.tipo=tipo

    def modificarDimension(self,nuevaDimension):
        if len(self.dimensiones)==1:
            self.dimensiones=nuevaDimension
        elif len(self.dimensiones)==2:
            self.dimensiones[0]=nuevaDimension[0]