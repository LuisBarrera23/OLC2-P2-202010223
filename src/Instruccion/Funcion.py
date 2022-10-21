from src.Instruccion.DeclaracionArreglo import DeclaracionArreglo
from src.Abstract.Instruccion import Instruccion
from src.Abstract.Expresion import Expresion
from src.Symbol.Symbol import Simbolo

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

from src.Instruccion.Return import Return
from src.Instruccion.Declaracion import Declaracion
from src.Instruccion.Llamada import Llamada
from src.Expresion.Referencia import Referencia

class Funcion(Simbolo,Instruccion):
    def __init__(self, identificador,parametros,bloque,tipo,linea,columna):
        self.identificador=identificador
        self.parametros=parametros
        self.bloque=bloque
        self.tipo=tipo
        self.linea=linea
        self.columna=columna
        super().__init__()
        super().Simbolo_funcion(identificador,parametros,bloque,linea,columna,tipo)
        self.generada=False
        self.entornoFuncion=None

    def Ejecutar(self, entorno):
        s=Singleton.getInstance()
        codigoSalida=""
        etqReturn=s.obtenerEtiqueta()
        codigoSalida += f"void {self.identificador}(){{\n"
        for i in self.bloque:
            codigoSalida += i.Ejecutar(entorno)
            try:
                #codigoSalida += i.Ejecutar(entorno)
                pass
            except:
                pass
        codigoSalida=codigoSalida.replace("REEMPLAZORETURN",etqReturn)
        codigoSalida+=f"{etqReturn}:\n"
        codigoSalida+=f"return;\n"
        codigoSalida+=f"}}\n"
        return codigoSalida

    def EjecutarParametros(self,entornoFuncion,entornoQueLlamo,nuevoPuntero,expresiones=[]):
        s=Singleton.getInstance()
        if len(self.parametros)!=len(expresiones):
            raise Exception(s.addError(Error("La cantidad de parametros no son correctos",self.linea,self.columna)))
        # codigoSalida1="/* DECLARACION DE LLAMADAS */\n"
        # codigoSalida2="/* DECLARACION DE VALORES */\n"
        codigoSalida1=""
        for i in range(len(expresiones)):
            declaracion=self.parametros[i]
            expresion:Expresion=expresiones[i]
            if isinstance(declaracion,Declaracion):
                declaracion.puntero_entornoN=nuevoPuntero
                declaracion.ejecuta_en_funcion=True
                declaracion.expresionCompilada=expresion.obtener3D(entornoQueLlamo)
                codigoSalida1+=declaracion.Ejecutar(entornoFuncion)
            elif isinstance(declaracion,DeclaracionArreglo):
                declaracion.puntero_entornoN=nuevoPuntero
                declaracion.ejecuta_en_funcion=True
                declaracion.expresionCompilada=expresion.obtener3D(entornoQueLlamo)
                codigoSalida1+=declaracion.Ejecutar(entornoFuncion)

        return codigoSalida1

    

    # def Ejecutar_main(self,entorno):
    #     s=Singleton.getInstance()
    #     AST=self.bloque
    #     for i in AST:
    #         s.agregarInstruccion(i.Ejecutar(entorno))
    #         try:
    #             """"""
    #             #s.agregarInstruccion(i.Ejecutar(entorno))
    #         except:
    #             print("error")
        