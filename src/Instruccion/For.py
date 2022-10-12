from src.Instruccion.Declaracion import Declaracion
from src.Abstract.Instruccion import Instruccion
from src.Abstract.RetornoType import RetornoType,TipoDato
from src.Symbol.EntornoTabla import EntornoTabla
from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error
from src.Symbol.Symbol import Simbolo

from src.Instruccion.Break import Break
from src.Instruccion.Continue import Continue
from src.Instruccion.Return import Return

from src.Symbol.ArrayInstancia import ArrayInstancia
from src.Expresion.AccesoSimbolo import AccesoSimbolo
from src.Expresion.Primitivo import Primitivo

class For(Instruccion):
    def __init__(self, variable, valor1, valor2, tipofor, bloque,linea, columna):
        self.variable=variable
        self.valor1=valor1
        self.valor2=valor2
        self.tipofor=tipofor
        self.bloque=bloque
        self.linea=linea
        self.columna=columna

    def Ejecutar(self, entorno):
        s=Singleton.getInstance()
        if self.tipofor==1:
            codigoSalida="/* FOR TIPO 1 */\n"
            E1:RetornoType=self.valor1.obtener3D(entorno)
            E2:RetornoType=self.valor2.obtener3D(entorno)

            etqCiclo=s.obtenerEtiqueta()
            etqActualizar=s.obtenerEtiqueta()
            etqSalida=s.obtenerEtiqueta()

            temp1=s.obtenerTemporal()
            temp2=s.obtenerTemporal()
            if E1.tipo!=TipoDato.I64 or E2.tipo!=TipoDato.I64:
                raise Exception(s.addError(Error(f"El rango del for necesita ser de tipo I64",self.linea,self.columna)))

            codigoSalida+=E1.codigo
            codigoSalida+=E2.codigo
            nuevoEntorno=EntornoTabla(entorno)
            nuevoEntorno.tamaño=entorno.tamaño
            variable=Declaracion(self.variable,None,True,self.linea,self.columna,TipoDato.I64)
            variable.expresionCompilada=E1
            codigoSalida+=variable.Ejecutar(nuevoEntorno)
            codigoSalida+=f"{etqCiclo}:\n"
            Acceso=AccesoSimbolo(self.variable,self.linea,self.columna).obtener3D(nuevoEntorno)
            codigoSalida+=Acceso.codigo
            codigoSalida += f"if({Acceso.temporal} >= {E2.temporal}) goto {etqSalida};\n"
            codigoSalida += self.EjecutarBloque(nuevoEntorno,self.bloque)
            codigoSalida+=f"{etqActualizar}:\n"
            codigoSalida += "/* ACTUALIZACION DEL ITERADOR */\n"
            variable:Simbolo=nuevoEntorno.obtenerSimbolo(self.variable)
            codigoSalida += f'{temp1} = SP + {variable.direccionRelativa}; \n'
            codigoSalida += f'{temp2} = Stack[(int) {temp1}]; \n'
            codigoSalida += f'Stack[(int) {temp1}] = {temp2} + 1;\n'
            codigoSalida += f"  goto {etqCiclo};\n"
            codigoSalida+=f"{etqSalida}:\n"
            codigoSalida=codigoSalida.replace("REEMPLAZOBREAK",etqSalida)
            codigoSalida=codigoSalida.replace("REEMPLAZOCONTINUE",etqActualizar)
            return codigoSalida


        elif self.tipofor==2:
            pass
        elif self.tipofor==3:
            pass
            

        return

    

    def EjecutarBloque(self,entorno,lista):
        codigoSalida = ""
        for i in lista :
            codigoSalida += i.Ejecutar(entorno)
        return codigoSalida
        