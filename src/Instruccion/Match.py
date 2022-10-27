from src.Abstract.RetornoType import TipoDato,RetornoType
from src.Abstract.Instruccion import Instruccion
from src.Symbol.Symbol import Simbolo
from src.Symbol.EntornoTabla import EntornoTabla
from src.Instruccion.Return import Return
from src.Instruccion.Break import Break
from src.Instruccion.Continue import Continue

from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

class Match(Instruccion):
    def __init__(self,valor,expresion1,instruccion1,expresion2,instruccion2,instruccion3,linea, columna):
        self.valor=valor
        self.expresion1=expresion1
        self.instruccion1=instruccion1
        self.expresion2=expresion2
        self.instruccion2=instruccion2
        self.instruccion3=instruccion3
        self.linea=linea
        self.columna=columna
        
    def Ejecutar(self, entorno):
        s=Singleton.getInstance()
        codigoSalida=""
        etq1=s.obtenerEtiqueta()
        etq2=s.obtenerEtiqueta()
        etq3=s.obtenerEtiqueta()
        etq4=s.obtenerEtiqueta()
        etqSalida=s.obtenerEtiqueta()
        
        
        codigoSalida += "/* INSTRUCCION MATCH */\n"
        valor=self.valor.obtener3D(entorno)
        expresion1=self.expresion1.obtener3D(entorno)
        codigoSalida += valor.codigo

        codigoSalida += expresion1.codigo
        codigoSalida += f"if({expresion1.temporal} == {valor.temporal}) goto {etq1};\n"
        codigoSalida += f"goto {etq2};\n"
        codigoSalida += f"{etq1}:\n"
        codigoSalida += self.instruccion1.Ejecutar(entorno)
        codigoSalida += f"goto {etqSalida};\n"
        codigoSalida += f"{etq2}:\n"

        expresion2=self.expresion2.obtener3D(entorno)
        codigoSalida += expresion2.codigo
        codigoSalida += f"if({expresion2.temporal} == {valor.temporal}) goto {etq3};\n"
        codigoSalida += f"goto {etq4};\n"
        codigoSalida += f"{etq3}:\n"
        codigoSalida += self.instruccion2.Ejecutar(entorno)
        codigoSalida += f"goto {etqSalida};\n"
        codigoSalida += f"{etq4}:\n"
        codigoSalida += self.instruccion3.Ejecutar(entorno)

        codigoSalida += f"{etqSalida}:\n"
        return codigoSalida