from src.Symbol.Error import Error


class Singleton:

    __instance = None

    @staticmethod
    def getInstance():
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        self.consola = ""
        self.temporales = 0
        self.etiquetas = 0
        self.codigo = ""
        self.main = ""
        self.funciones=""
        self.errores = []
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self

    def reset(self):
        self.consola = ""
        self.temporales = 0
        self.etiquetas = 0
        self.codigo = ""
        self.funciones = ""
        self.main = ""
        self.errores = []

    def addError(self, Error: Error):
        self.errores.append(Error)

    def getErrores(self):
        return self.errores

    def obtenerTemporal(self):
        temporal = "t"+self.temporales.__str__()
        self.temporales  += 1
        return temporal

    def obtenerEtiqueta(self):
        etiqueta = "L"+self.etiquetas.__str__()
        self.etiquetas += 1
        return etiqueta

    def generarEncabezado(self):
        codigo = "#include <stdio.h>\nfloat Stack[10000];\nfloat Heap[10000];\nint SP;\nint HP;\n"
        if self.temporales > 0:
            codigo += "float "
            for i in range(0, self.temporales):
                if i % 15 == 0 and i > 0:
                    codigo += "\n"
                codigo += f"t{i}"
                if i < self.temporales - 1:
                    codigo += ","
            codigo += ";\n"
        return codigo

    def agregarInstruccion(self, codigo):
        self.main += codigo+"\n"

    def agregarFuncion(self, codigo):
        self.funciones += codigo+"\n"

    def generarMain(self):
        codigo = self.generarEncabezado()
        codigo += self.codigo+"\n"
        codigo += self.funciones+"\n"
        codigo += "int main(){\n"
        codigo += f"{self.main}\n"
        codigo += "return 0;\n}"
        return codigo
