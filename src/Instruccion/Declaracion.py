from src.Abstract.RetornoType import RetornoType, TipoDato
from src.Abstract.Instruccion import Instruccion
from src.Symbol.Symbol import Simbolo

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error
from src.Symbol.EntornoTabla import EntornoTabla

class Declaracion(Instruccion):
    def __init__(self, id, expresion, mutable,linea,columna, tipo=None):
        self.id=id
        self.expresion=expresion
        self.mutable=mutable
        self.tipo=tipo
        self.linea=linea
        self.columna=columna

        self.expresionCompilada=None
        self.puntero_entornoN=""
        self.ejecuta_en_funcion=False
        
    def Ejecutar(self, entorno):
        codigoSalida=""
        existe=entorno.existeSimboloEnEntornoActual(self.id)
        s=Singleton.getInstance()
        if existe:
            raise Exception(s.addError(Error(f"Variable {self.id} ya existente en este entorno",self.linea,self.columna)))
        
        valor:RetornoType=None
        if self.expresion is not None:
            valor:RetornoType=self.expresion.obtener3D(entorno)
        elif self.expresionCompilada is not None:
            valor=self.expresionCompilada

        punteroEntorno="SP"

        if self.ejecuta_en_funcion:
            punteroEntorno=self.puntero_entornoN

        tamaño=entorno.tamaño
        temp1=s.obtenerTemporal()


        
        if self.tipo==None:
            codigoSalida += "/* DECLARACIÓN DE UNA VARIABLE */\n"
            codigoSalida += valor.codigo + '\n'
            codigoSalida += f'{temp1} = {punteroEntorno} + {tamaño}; \n'
            codigoSalida += f'Stack[(int) {temp1}] = {valor.temporal};\n'
            nueva=Simbolo()
            nueva.Simbolo_primitivo(self.id,None,valor.tipo,self.linea,self.columna,tamaño,self.mutable)
            entorno.agregarSimbolo(nueva)
            entorno.tamaño+=1
            return codigoSalida
        else:
            if valor.tipo==TipoDato.I64 and self.tipo==TipoDato.USIZE:
                codigoSalida += "/* DECLARACIÓN DE UNA VARIABLE */\n"
                codigoSalida += valor.codigo +'\n'
                codigoSalida += f'{temp1} = {punteroEntorno} + {tamaño};\n'
                codigoSalida += f'Stack[(int) {temp1}] = {valor.temporal};\n'
                nueva=Simbolo()
                nueva.Simbolo_primitivo(self.id,None,self.tipo,self.linea,self.columna,tamaño,self.mutable)
                entorno.agregarSimbolo(nueva)
                entorno.tamaño+=1
                return codigoSalida
            elif valor.tipo==self.tipo:
                codigoSalida += "/* DECLARACIÓN DE UNA VARIABLE */\n"
                codigoSalida += valor.codigo +'\n'
                codigoSalida += f'{temp1} = {punteroEntorno} + {tamaño};\n'
                codigoSalida += f'Stack[(int) {temp1}] = {valor.temporal};\n'
                nueva=Simbolo()
                nueva.Simbolo_primitivo(self.id,None,self.tipo,self.linea,self.columna,tamaño,self.mutable)
                entorno.agregarSimbolo(nueva)
                entorno.tamaño+=1
                return codigoSalida
            else:
                raise Exception(s.addError(Error("Tipo de expresion no coincide con el tipo de dato especificado",self.linea,self.columna)))