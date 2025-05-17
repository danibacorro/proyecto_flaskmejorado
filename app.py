from flask import Flask, render_template, request
import json

app = Flask(__name__)	

with open('pruebas_coches.json', encoding='utf-8') as f:
    coches_json = json.load(f)


@app.route('/')
def inicio():
    return render_template("index.html")

@app.route("/busqueda")
def busqueda():
    return render_template("busqueda.html")

@app.route('/lista', methods=['POST'])
def lista():
    listado = []
    nombre = request.form.get('buscador', '').lower()
    for coche in coches_json:
        for prueba in coche["pruebas"]:
            if prueba["modelo"].lower().startswith(nombre) or nombre == '':
                listado.append({
                    "id": prueba["id"],
                    "modelo": prueba["modelo"],
                    "consumo_combinado": prueba["consumo"]["combinado"]
                })
    return render_template('lista.html', listado=listado)

@app.route('/detalle/<id>')
def detalle(id):
    for item in coches_json:
        for prueba in item["pruebas"]:
            if prueba["id"] == id:
                return render_template('detalle.html', prueba=prueba)
    return "Error 404. Este modelo no existe.", 404

app.run("0.0.0.0",5000,debug=True)