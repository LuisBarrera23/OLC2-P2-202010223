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
                elif E1.tipo==TipoDato.STR and E2.tipo==TipoDato.STR:
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
                    return RetornoType(valor=str(E1.valor+E2.valor),tipo=TipoDato.STRING)

                else:
                    raise Exception(s.addError(Error("Tipo de suma no valida",self.linea,self.columna)))
            
            elif self.tipo==TIPO_OPERACION.RESTA:
                if E1.tipo==TipoDato.F64 and E2.tipo==TipoDato.F64:
                    return RetornoType(valor=float(E1.valor-E2.valor),tipo=TipoDato.F64)
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.I64:
                    return RetornoType(valor=int(E1.valor-E2.valor),tipo=TipoDato.I64)
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.USIZE:
                    return RetornoType(valor=int(E1.valor-E2.valor),tipo=TipoDato.USIZE)
                elif E1.tipo==TipoDato.USIZE and E2.tipo==TipoDato.I64:
                    return RetornoType(valor=int(E1.valor-E2.valor),tipo=TipoDato.USIZE)
                elif E1.tipo==TipoDato.USIZE and E2.tipo==TipoDato.USIZE:
                    return RetornoType(valor=int(E1.valor-E2.valor),tipo=TipoDato.USIZE)
                else:
                    raise Exception(s.addError(Error("Tipo de resta no valida",self.linea,self.columna)))
            
            elif self.tipo==TIPO_OPERACION.MULTIPLICACION:
                if E1.tipo==TipoDato.F64 and E2.tipo==TipoDato.F64:
                    return RetornoType(valor=float(E1.valor*E2.valor),tipo=TipoDato.F64)
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.I64:
                    return RetornoType(valor=int(E1.valor*E2.valor),tipo=TipoDato.I64)
                else:
                    raise Exception(s.addError(Error("Tipo de multiplicacion no valida",self.linea,self.columna)))

            elif self.tipo==TIPO_OPERACION.DIVISION:
                if E1.tipo==TipoDato.F64 and E2.tipo==TipoDato.F64:
                    return RetornoType(valor=float(E1.valor/E2.valor),tipo=TipoDato.F64)
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.I64:
                    return RetornoType(valor=int(E1.valor/E2.valor),tipo=TipoDato.I64)

                else:
                    raise Exception(s.addError(Error("Tipo de division no valida",self.linea,self.columna)))

            elif self.tipo==TIPO_OPERACION.POTENCIA:
                if E1.tipo==TipoDato.F64 and E2.tipo==TipoDato.F64 and self.tipo2==TipoDato.F64:
                    return RetornoType(valor=float(E1.valor**E2.valor),tipo=TipoDato.F64)
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.I64 and self.tipo2==TipoDato.I64:
                    return RetornoType(valor=int(E1.valor**E2.valor),tipo=TipoDato.I64)

                else:
                    raise Exception(s.addError(Error("Tipo de potencia no valida",self.linea,self.columna)))
            
            elif self.tipo==TIPO_OPERACION.MODULO:
                if E1.tipo==TipoDato.F64 and E2.tipo==TipoDato.F64:
                    return RetornoType(valor=float(E1.valor%E2.valor),tipo=TipoDato.F64)
                elif E1.tipo==TipoDato.I64 and E2.tipo==TipoDato.I64:
                    return RetornoType(valor=int(E1.valor%E2.valor),tipo=TipoDato.I64)
                else:
                    raise Exception(s.addError(Error("Tipo de modulo no valida",self.linea,self.columna)))


#--------------------------------------------------------------------------------
#Operaciones Relacionales
            elif self.tipo==TIPO_OPERACION.MAYOR:
                return RetornoType(valor=E1.valor>E2.valor,tipo=TipoDato.BOOL)

            elif self.tipo==TIPO_OPERACION.MENOR:
                return RetornoType(valor=E1.valor<E2.valor,tipo=TipoDato.BOOL)

            elif self.tipo==TIPO_OPERACION.MAYORIGUAL:
                return RetornoType(valor=E1.valor>=E2.valor,tipo=TipoDato.BOOL)

            elif self.tipo==TIPO_OPERACION.MENORIGUAL:
                return RetornoType(valor=E1.valor<=E2.valor,tipo=TipoDato.BOOL)
            
            elif self.tipo==TIPO_OPERACION.IGUALIGUAL:
                return RetornoType(valor=E1.valor==E2.valor,tipo=TipoDato.BOOL)

            elif self.tipo==TIPO_OPERACION.DIFERENTE:
                return RetornoType(valor=E1.valor!=E2.valor,tipo=TipoDato.BOOL)

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
