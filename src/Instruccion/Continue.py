from src.Abstract.Instruccion import Instruccion

class Continue(Instruccion):
    def __init__(self, linea, columna):
        self.linea=linea
        self.columna=columna

    def Ejecutar(self, entorno):
        codigoSalida=""
        codigoSalida+=f"/* CONTINUE */\n"
        codigoSalida+="goto REEMPLAZOCONTINUE;\n"
        return codigoSalida