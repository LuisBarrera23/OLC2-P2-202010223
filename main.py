from flask import Flask,jsonify,request

from flask_cors import CORS

import json

app = Flask(__name__)
CORS(app)




from src.PatronSingleton.Singleton import Singleton
from src.Symbol.Error import Error
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
            i.Ejecutar(EntornoPadre)
        except:
            print("error.........................")

    if EntornoPadre.existeFuncion("main"):
        funcion:Funcion=EntornoPadre.obtenerFuncion("main")
        funcion.Ejecutar_main(EntornoPadre)

    else:
        s.addError(Error("Debe existir la funcion main",0,0))

    print("ERRORES-----------------------------------------")
    errores:Error=s.getErrores()
    for e in errores:
        print(e.descripcion,e.tiempo," linea: ",e.linea," columna: ",e.columna)
    return jsonify({'salida':s.getConsola()})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
