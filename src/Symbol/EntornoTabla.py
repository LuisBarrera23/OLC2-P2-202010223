from src.Symbol.Symbol import Simbolo
from src.PatronSingleton.Singleton import Singleton,SimboloT
from src.Symbol.ArrayInstancia import ArrayInstancia
from src.Symbol.VectorInstancia import VectorInstancia


class EntornoTabla:
    def __init__(self,padre=None):
        self.padre=padre
        self.tabla={}
        self.tablaFunciones={}
        self.tablaClases={}
        self.tamaño=0

# Manejo de simbolos--------------------------------------------------------
    def existeSimbolo(self,identificador):
        entorno = self

        while entorno is not None:
            existe = entorno.tabla.get(identificador)
            if existe is not None:
                return True
            else:
                entorno = entorno.padre

        return False

    def existeSimboloEnEntornoActual(self,identificador):
        existe = self.tabla.get(identificador)
        if existe is not None:
            return True
        else:
            return False

    def obtenerSimbolo(self,identificador) -> Simbolo:
        entorno = self
        while entorno is not None:
            simbolo = entorno.tabla.get(identificador)
            if simbolo is not None:
                return simbolo
            else:
                entorno = entorno.padre

        return Simbolo()

    def agregarSimbolo(self, simboloAdd:Simbolo):
        s=Singleton.getInstance()
        self.tabla[simboloAdd.identificador] = simboloAdd
        self.tamaño+=1
        if isinstance(simboloAdd,ArrayInstancia):
            s.addSimbolo(SimboloT(simboloAdd.identificador,"Arreglo","Local",simboloAdd.linea,simboloAdd.columna))
        elif isinstance(simboloAdd,VectorInstancia):
            s.addSimbolo(SimboloT(simboloAdd.identificador,"Vector","Local",simboloAdd.linea,simboloAdd.columna))
        else:
            s.addSimbolo(SimboloT(simboloAdd.identificador,"Simbolo Primitivo","Local",simboloAdd.linea,simboloAdd.columna))




    def modificarSimbolo(self,identificador,valor):
        entorno = self
        while entorno is not None:
            simbolo:Simbolo = entorno.tabla.get(identificador)
            if simbolo is not None:
                simbolo.valor=valor
                return
            else:
                entorno = entorno.padre

# Manejo de funciones------------------------------------------------------------------

    def existeFuncion(self,identificador):
        entorno = self
        while entorno is not None:
            existe = entorno.tablaFunciones.get(identificador)
            if existe is not None:
                return True
            else:
                entorno = entorno.padre
        return False

    def obtenerFuncion(self,identificador):
        entorno = self
        while entorno is not None:
            simbolo = entorno.tablaFunciones.get(identificador)
            if simbolo is not None:
                return simbolo
            else:
                entorno = entorno.padre

        return None

    def agregarFuncion(self,funcionAdd):
        s=Singleton.getInstance()
        self.tablaFunciones[funcionAdd.identificador] = funcionAdd
        s.addSimbolo(SimboloT(funcionAdd.identificador,"Funcion","Global",funcionAdd.linea,funcionAdd.columna))
        #print(f"funcion {funcionAdd.identificador} agregada con exito")

    def actualizarFuncion(self,funcion):
        entorno = self
        while entorno is not None:
            simbolo = entorno.tablaFunciones.get(funcion.identificador)
            if simbolo is not None:
                entorno.tablaFunciones[funcion.identificador] = funcion
                return
            else:
                entorno = entorno.padre
