from flask import Flask,jsonify,request

from flask_cors import CORS

import json

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
def inicializacion():
    return("<h1>Servidor Corriendo con exito</h1>")

@app.route('/ejecutar',methods=['POST'])
def ejecutar():
    entrada=request.json['entrada']
    print(entrada)
    return jsonify({'salida':'hola xdxdxd'})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
