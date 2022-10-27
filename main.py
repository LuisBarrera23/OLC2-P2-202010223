from flask import Flask,jsonify,request

from flask_cors import CORS

import json

app = Flask(__name__)
CORS(app)




from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error
from src.Symbol.Simbolo import SimboloT
from src.Symbol.EntornoTabla import EntornoTabla
from gramatica import gramatica
from src.Instruccion.Funcion import Funcion

@app.route('/',methods=['GET'])
def inicializacion():
    return("<h1>Servidor Corriendo con exito</h1>")

@app.route('/ejecutar',methods=['POST'])
def ejecutar():
    entrada=request.json['entrada']
    s=Singleton.getInstance()
    s.reset()

    EntornoPadre=EntornoTabla(None)
    AST = gramatica.parse(entrada)
    #print(AST)
    for i in AST:
        try:
            if isinstance(i,Funcion):
                existe=EntornoPadre.existeFuncion(i.identificador)
                if existe:
                    s.addError(Error(f"Funcion {i.identificador} ya existe",i.linea,i.columna))
                else:
                    EntornoPadre.agregarFuncion(funcionAdd=i)
        except:
            print("error.........................")
    
    main=EntornoPadre.existeFuncion("main")
    if main:
        principal=EntornoPadre.obtenerFuncion("main")
        for instruccion in principal.bloque:
            try:
                s.agregarInstruccion(instruccion.Ejecutar(EntornoPadre))
                pass
            except:
                print("error.........................")
            #s.agregarInstruccion(instruccion.Ejecutar(EntornoPadre))
    else:
        s.addError(Error(f"No existe funcion main()",0,0))

    print("ERRORES-----------------------------------------")
    errores:Error=s.getErrores()
    for e in errores:
        print(e.descripcion,e.tiempo," linea: ",e.linea," columna: ",e.columna)
    return jsonify({'salida':s.generarMain()})

@app.route('/errores',methods=['GET'])
def errores():
    s=Singleton.getInstance()
    errores:Error=s.getErrores()
    arreglo=[]
    for e in errores:
        temp={
            'descripcion':e.descripcion,
            'linea':e.linea,
            'columna':e.columna,
            'fecha':e.tiempo
        }
        arreglo.append(temp)
    return jsonify(arreglo)

@app.route('/simbolos',methods=['GET'])
def simbolos():
    s=Singleton.getInstance()
    simbolos:SimboloT=s.getSimbolos()
    arreglo=[]
    for s in simbolos:
        temp={
            'nombre':s.nombre,
            'tipo':s.tipo,
            'ambito':s.ambito,
            'linea':s.linea,
            'columna':s.columna
        }
        arreglo.append(temp)
    return jsonify(arreglo)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
