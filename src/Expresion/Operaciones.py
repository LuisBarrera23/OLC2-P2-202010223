from enum import Enum
from src.Abstract.Expresion import Expresion
from src.Abstract.RetornoType import RetornoType, TipoDato
from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error

class TIPO_OPERACION(Enum):
    SUMA = 1,
    RESTA = 2,
    MULTIPLICACION = 3,
    DIVISION = 4,
    POTENCIA = 5,
    MODULO = 6,
    MAYOR = 7,
    MENOR = 8,
    MAYORIGUAL = 9,
    MENORIGUAL = 10,
    IGUALIGUAL = 11,
    DIFERENTE = 12,
    OR = 13,
    AND = 14,
    NOT = 15,

class Operacion(Expresion):

    def __init__(self,izquierda,tipo,derecha,unario,linea,columna):
        self.izquierda=izquierda
        self.tipo=tipo
        self.derecha=derecha
        self.unario=unario
        self.linea=linea
        self.columna=columna
        self.tipo2:TipoDato=TipoDato.ERROR
        self.etiquetaVerdadera=""
        self.etiquetaFalsa=""
        

    def obtener3D(self, entorno) -> RetornoType:
        s=Singleton.getInstance()
        E1=RetornoType()
        E2=RetornoType()
        RetornoUnario=RetornoType()

        if self.unario:
            RetornoUnario=self.izquierda.obtener3D(entorno)
            if RetornoUnario.tipo==TipoDato.I64:
                return RetornoType(valor=int(RetornoUnario.valor*-1),tipo=RetornoUnario.tipo)
            elif RetornoUnario.tipo==TipoDato.F64:
                return RetornoType(valor=float(RetornoUnario.valor*-1),tipo=RetornoUnario.tipo)
            elif RetornoUnario.tipo==TipoDato.BOOL and self.tipo==TIPO_OPERACION.NOT:
                return RetornoType(valor=not RetornoUnario.valor,tipo=TipoDato.BOOL)

        else:
            E1:RetornoType=self.izquierda.obtener3D(entorno)
            E2:RetornoType=self.derecha.obtener3D(entorno)
            temp1=s.obtenerTemporal()
            retorno=RetornoType()
            codigoSalida=""
            
            if self.tipo==TIPO_OPERACION.SUMA:
                if E1.tipo==TipoDato.F64 and E2.tipo==TipoDato.F64:
                    codigoSalida+="/* SUMA */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = {E1.temporal} + {E2.temporal};\n'
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.F64)
                    return retorno
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.I64:
                    codigoSalida+="/* SUMA */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = {E1.temporal} + {E2.temporal};\n'
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.I64)
                    return retorno
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.USIZE:
                    codigoSalida+="/* SUMA */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = {E1.temporal} + {E2.temporal};\n'
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.USIZE)
                    return retorno
                elif E1.tipo==TipoDato.USIZE and E2.tipo==TipoDato.I64:
                    codigoSalida+="/* SUMA */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = {E1.temporal} + {E2.temporal};\n'
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.USIZE)
                    return retorno
                elif E1.tipo==TipoDato.USIZE and E2.tipo==TipoDato.USIZE:
                    codigoSalida+="/* SUMA */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = {E1.temporal} + {E2.temporal};\n'
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.USIZE)
                    return retorno
                elif E1.tipo==TipoDato.STRING and E2.tipo==TipoDato.STR:
                    codigoSalida+="/* SUMA */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = HP;\n'
                    codigoSalida += self.operacionConcatenar(entorno,E1)
                    codigoSalida += self.operacionConcatenar(entorno,E2)
                    codigoSalida += f'Heap[HP] = 0;\n'  #agregamos caracter de escape
                    codigoSalida += f'HP = HP + 1;\n'   #modificamos el apuntador del heap a una posicion vacia
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.STRING)
                    return retorno
                elif E1.tipo==TipoDato.STR and E2.tipo==TipoDato.STRING:
                    codigoSalida+="/* SUMA */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = HP;\n'
                    codigoSalida += self.operacionConcatenar(entorno,E1)
                    codigoSalida += self.operacionConcatenar(entorno,E2)
                    codigoSalida += f'Heap[HP] = 0;\n'  #agregamos caracter de escape
                    codigoSalida += f'HP = HP + 1;\n'   #modificamos el apuntador del heap a una posicion vacia
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.STRING)
                    return retorno

                else:
                    raise Exception(s.addError(Error("Tipo de suma no valida",self.linea,self.columna)))
            
            elif self.tipo==TIPO_OPERACION.RESTA:
                if E1.tipo==TipoDato.F64 and E2.tipo==TipoDato.F64:
                    codigoSalida+="/* RESTA */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = {E1.temporal} - {E2.temporal};\n'
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.F64)
                    return retorno
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.I64:
                    codigoSalida+="/* RESTA */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = {E1.temporal} - {E2.temporal};\n'
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.I64)
                    return retorno
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.USIZE:
                    codigoSalida+="/* RESTA */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = {E1.temporal} - {E2.temporal};\n'
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.USIZE)
                    return retorno
                elif E1.tipo==TipoDato.USIZE and E2.tipo==TipoDato.I64:
                    codigoSalida+="/* RESTA */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = {E1.temporal} - {E2.temporal};\n'
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.USIZE)
                    return retorno
                elif E1.tipo==TipoDato.USIZE and E2.tipo==TipoDato.USIZE:
                    codigoSalida+="/* RESTA */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = {E1.temporal} - {E2.temporal};\n'
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.USIZE)
                    return retorno
                else:
                    raise Exception(s.addError(Error("Tipo de resta no valida",self.linea,self.columna)))
            
            elif self.tipo==TIPO_OPERACION.MULTIPLICACION:
                if E1.tipo==TipoDato.F64 and E2.tipo==TipoDato.F64:
                    codigoSalida+="/* MULTIPLICACION */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = {E1.temporal} * {E2.temporal};\n'
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.F64)
                    return retorno
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.I64:
                    codigoSalida+="/* MULTIPLICACION */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    codigoSalida += f'{temp1} = {E1.temporal} * {E2.temporal};\n'
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.I64)
                    return retorno
                else:
                    raise Exception(s.addError(Error("Tipo de multiplicacion no valida",self.linea,self.columna)))

            elif self.tipo==TIPO_OPERACION.DIVISION:
                if E1.tipo==TipoDato.F64 and E2.tipo==TipoDato.F64:
                    codigoSalida+="/* DIVISION */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    etqVerdadera = s.obtenerEtiqueta()
                    codigoSalida += f"if ({E2.temporal} != 0) goto {etqVerdadera};\n"
                    codigoSalida += f"  printf(\"%c\", 77);\n"
                    codigoSalida += f"  printf(\"%c\", 97);\n"
                    codigoSalida += f"  printf(\"%c\", 116);\n"
                    codigoSalida += f"  printf(\"%c\", 104);\n"
                    codigoSalida += f"  printf(\"%c\", 69);\n"
                    codigoSalida += f"  printf(\"%c\", 114);\n"
                    codigoSalida += f"  printf(\"%c\", 114);\n"
                    codigoSalida += f"  printf(\"%c\", 111);\n"
                    codigoSalida += f"  printf(\"%c\", 114);\n"
                    codigoSalida += f"  printf(\"%c\", 68);\n"
                    codigoSalida += f"  printf(\"%c\", 73);\n"
                    codigoSalida += f"  printf(\"%c\\n\", 86);\n"
                    codigoSalida += f"  {temp1} = 0;\n"
                    etqSalida = s.obtenerEtiqueta()
                    codigoSalida += f"  goto {etqSalida};\n"
                    codigoSalida += f"{etqVerdadera}:\n"
                    codigoSalida += f"  {temp1} = {E1.temporal} / {E2.temporal};\n"
                    codigoSalida += f"{etqSalida}:\n"
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.F64)
                    return retorno
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.I64:
                    codigoSalida+="/* DIVISION */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    etqVerdadera = s.obtenerEtiqueta()
                    codigoSalida += f"if ({E2.temporal} != 0) goto {etqVerdadera};\n"
                    codigoSalida += f"  printf(\"%c\", 77);\n"
                    codigoSalida += f"  printf(\"%c\", 97);\n"
                    codigoSalida += f"  printf(\"%c\", 116);\n"
                    codigoSalida += f"  printf(\"%c\", 104);\n"
                    codigoSalida += f"  printf(\"%c\", 69);\n"
                    codigoSalida += f"  printf(\"%c\", 114);\n"
                    codigoSalida += f"  printf(\"%c\", 114);\n"
                    codigoSalida += f"  printf(\"%c\", 111);\n"
                    codigoSalida += f"  printf(\"%c\", 114);\n"
                    codigoSalida += f"  printf(\"%c\", 68);\n"
                    codigoSalida += f"  printf(\"%c\", 73);\n"
                    codigoSalida += f"  printf(\"%c\\n\", 86);\n"
                    codigoSalida += f"  {temp1} = 0;\n"
                    etqSalida = s.obtenerEtiqueta()
                    codigoSalida += f"  goto {etqSalida};\n"
                    codigoSalida += f"{etqVerdadera}:\n"
                    codigoSalida += f"  {temp1} = {E1.temporal} / {E2.temporal};\n"
                    codigoSalida += f"{etqSalida}:\n"
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.I64)
                    return retorno

                else:
                    raise Exception(s.addError(Error("Tipo de division no valida",self.linea,self.columna)))

            elif self.tipo==TIPO_OPERACION.POTENCIA:
                if E1.tipo==TipoDato.F64 and E2.tipo==TipoDato.F64 and self.tipo2==TipoDato.F64:
                    etqCiclo=s.obtenerEtiqueta()
                    etqSalida=s.obtenerEtiqueta()
                    temp2=s.obtenerTemporal()
                    codigoSalida+="/* POTENCIA */\n"
                    codigoSalida += f"{E1.codigo}\n"
                    codigoSalida += f"{E2.codigo}\n"
                    codigoSalida += f"{temp2} = 1;\n"
                    codigoSalida += f"{temp1} = {E1.temporal};\n"
                    codigoSalida += f"if ({E2.temporal} > 0) goto {etqCiclo};\n"
                    codigoSalida += f"  {temp1} = 1;\n"
                    codigoSalida += f"  goto {etqSalida};\n"
                    codigoSalida += f"{etqCiclo}:\n"
                    codigoSalida += f"if ({temp2} == {E2.temporal}) goto {etqSalida};\n"
                    codigoSalida += f"  {temp1} = {temp1} * {E1.temporal};\n"
                    codigoSalida += f"  {temp2} = {temp2} + 1;\n"
                    codigoSalida += f"  goto {etqCiclo};\n"
                    codigoSalida += f"{etqSalida}:\n"
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.F64)
                    return retorno
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.I64 and self.tipo2==TipoDato.I64:
                    etqCiclo=s.obtenerEtiqueta()
                    etqSalida=s.obtenerEtiqueta()
                    temp2=s.obtenerTemporal()
                    codigoSalida+="/* POTENCIA */\n"
                    codigoSalida += f"{E1.codigo}\n"
                    codigoSalida += f"{E2.codigo}\n"
                    codigoSalida += f"{temp2} = 1;\n"
                    codigoSalida += f"{temp1} = {E1.temporal};\n"
                    codigoSalida += f"if ({E2.temporal} > 0) goto {etqCiclo};\n"
                    codigoSalida += f"  {temp1} = 1;\n"
                    codigoSalida += f"  goto {etqSalida};\n"
                    codigoSalida += f"{etqCiclo}:\n"
                    codigoSalida += f"if ({temp2} == {E2.temporal}) goto {etqSalida};\n"
                    codigoSalida += f"  {temp1} = {temp1} * {E1.temporal};\n"
                    codigoSalida += f"  {temp2} = {temp2} + 1;\n"
                    codigoSalida += f"  goto {etqCiclo};\n"
                    codigoSalida += f"{etqSalida}:\n"
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.I64)
                    return retorno

                else:
                    raise Exception(s.addError(Error("Tipo de potencia no valida",self.linea,self.columna)))
            
            elif self.tipo==TIPO_OPERACION.MODULO:
                if E1.tipo==TipoDato.F64 and E2.tipo==TipoDato.F64:
                    codigoSalida+="/* MODULO */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    etqVerdadera = s.obtenerEtiqueta()
                    codigoSalida += f"if ({E2.temporal} != 0) goto {etqVerdadera};\n"
                    codigoSalida += f"  printf(\"%c\", 77);\n"
                    codigoSalida += f"  printf(\"%c\", 97);\n"
                    codigoSalida += f"  printf(\"%c\", 116);\n"
                    codigoSalida += f"  printf(\"%c\", 104);\n"
                    codigoSalida += f"  printf(\"%c\", 69);\n"
                    codigoSalida += f"  printf(\"%c\", 114);\n"
                    codigoSalida += f"  printf(\"%c\", 114);\n"
                    codigoSalida += f"  printf(\"%c\", 111);\n"
                    codigoSalida += f"  printf(\"%c\", 114);\n"
                    codigoSalida += f"  printf(\"%c\", 77);\n"
                    codigoSalida += f"  printf(\"%c\", 79);\n"
                    codigoSalida += f"  printf(\"%c\\n\", 68);\n"
                    codigoSalida += f"  {temp1} = 0;\n"
                    etqSalida = s.obtenerEtiqueta()
                    codigoSalida += f"  goto {etqSalida};\n"
                    codigoSalida += f"{etqVerdadera}:\n"
                    codigoSalida += f"  {temp1} = (int){E1.temporal} % (int){E2.temporal};\n"
                    codigoSalida += f"{etqSalida}:\n"
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.F64)
                    return retorno
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.I64:
                    codigoSalida+="/* MODULO */\n"
                    codigoSalida += E1.codigo +"\n"
                    codigoSalida += E2.codigo +"\n"
                    etqVerdadera = s.obtenerEtiqueta()
                    codigoSalida += f"if ({E2.temporal} != 0) goto {etqVerdadera};\n"
                    codigoSalida += f"  printf(\"%c\", 77);\n"
                    codigoSalida += f"  printf(\"%c\", 97);\n"
                    codigoSalida += f"  printf(\"%c\", 116);\n"
                    codigoSalida += f"  printf(\"%c\", 104);\n"
                    codigoSalida += f"  printf(\"%c\", 69);\n"
                    codigoSalida += f"  printf(\"%c\", 114);\n"
                    codigoSalida += f"  printf(\"%c\", 114);\n"
                    codigoSalida += f"  printf(\"%c\", 111);\n"
                    codigoSalida += f"  printf(\"%c\", 114);\n"
                    codigoSalida += f"  printf(\"%c\", 77);\n"
                    codigoSalida += f"  printf(\"%c\", 79);\n"
                    codigoSalida += f"  printf(\"%c\\n\", 68);\n"
                    codigoSalida += f"  {temp1} = 0;\n"
                    etqSalida = s.obtenerEtiqueta()
                    codigoSalida += f"  goto {etqSalida};\n"
                    codigoSalida += f"{etqVerdadera}:\n"
                    codigoSalida += f"  {temp1} = (int){E1.temporal} % (int){E2.temporal};\n"
                    codigoSalida += f"{etqSalida}:\n"
                    retorno.iniciarRetorno(codigoSalida,"",temp1,TipoDato.I64  )
                    return retorno
                else:
                    raise Exception(s.addError(Error("Tipo de modulo no valida",self.linea,self.columna)))


#--------------------------------------------------------------------------------
#Operaciones Relacionales
            elif self.tipo==TIPO_OPERACION.MAYOR:
                return self.Relacional(entorno)

            elif self.tipo==TIPO_OPERACION.MENOR:
                return self.Relacional(entorno)

            elif self.tipo==TIPO_OPERACION.MAYORIGUAL:
                return self.Relacional(entorno)

            elif self.tipo==TIPO_OPERACION.MENORIGUAL:
                return self.Relacional(entorno)
            
            elif self.tipo==TIPO_OPERACION.IGUALIGUAL:
                return self.Relacional(entorno)

            elif self.tipo==TIPO_OPERACION.DIFERENTE:
                return self.Relacional(entorno)

#--------------------------------------------------------------------------------
#Operaciones logicas

            elif self.tipo==TIPO_OPERACION.OR:
                if E1.tipo==TipoDato.BOOL and E2.tipo==TipoDato.BOOL:
                    return RetornoType(valor=E1.valor or E2.valor,tipo=TipoDato.BOOL)
                else:
                    raise Exception(s.addError(Error("Tipo de OR no valido",self.linea,self.columna)))

            elif self.tipo==TIPO_OPERACION.AND:
                if E1.tipo==TipoDato.BOOL and E2.tipo==TipoDato.BOOL:
                    return RetornoType(valor=E1.valor and E2.valor,tipo=TipoDato.BOOL)
                else:
                    raise Exception(s.addError(Error("Tipo de AND no valido",self.linea,self.columna)))



    def operacionConcatenar(self,entorno,expresionRetorno):
        s=Singleton.getInstance()
        codigoSalida = ""
        etqCiclo = s.obtenerEtiqueta()
        etqSalida = s.obtenerEtiqueta()
        CARACTER = s.obtenerTemporal()
        #concatenar recorriendo el heap hasta encontrar el caracter de escape 0
        codigoSalida += f'{etqCiclo}: \n'
        codigoSalida += f'{CARACTER} = Heap[(int){expresionRetorno.temporal}];\n'
        codigoSalida += f'if ( {CARACTER} == 0) goto {etqSalida};\n'
        codigoSalida += f'     Heap[HP] = {CARACTER};\n'
        codigoSalida += f'     HP = HP + 1;\n'
        codigoSalida += f'     {expresionRetorno.temporal} = {expresionRetorno.temporal} + 1;\n'
        codigoSalida += f'     goto {etqCiclo};\n'
        codigoSalida += f'{etqSalida}:\n'
        return codigoSalida

    def Relacional(self,entorno):
        codigoSalida=""
        s=Singleton.getInstance()
        E1:RetornoType=self.izquierda.obtener3D(entorno)
        E2:RetornoType=self.derecha.obtener3D(entorno)
        codigoSalida += E1.codigo
        codigoSalida += E2.codigo
        codigoSalida += f'if ({E1.temporal} {self.simbolo()} {E2.temporal}) goto {self.etiquetaVerdadera};\n'
        codigoSalida += f'goto {self.etiquetaFalsa}; \n'
        retorno=RetornoType()
        retorno.iniciarRetorno(codigoSalida,"","",TipoDato.BOOL)
        retorno.etiquetaV = self.etiquetaVerdadera
        retorno.etiquetaF = self.etiquetaFalsa
        return retorno
        

    def simbolo(self):
        if self.tipo == TIPO_OPERACION.MAYOR:
            return ">"
        elif self.tipo == TIPO_OPERACION.MENOR:
            return "<"
        elif self.tipo == TIPO_OPERACION.MAYORIGUAL:
            return ">="
        elif self.tipo == TIPO_OPERACION.MENORIGUAL:
            return "<="
        elif self.tipo == TIPO_OPERACION.IGUALIGUAL:
            return "=="
        elif self.tipo == TIPO_OPERACION.DIFERENTE:
            return "!="
        elif self.tipo == TIPO_OPERACION.AND:
            return "&&"
        elif self.tipo == TIPO_OPERACION.OR:
            return "||"
        