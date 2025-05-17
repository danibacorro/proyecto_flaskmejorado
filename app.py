from flask import Flask, render_template, request
import json

app = Flask(__name__)	

with open('pruebas_coches.json', encoding='utf-8') as f:
    coches_json = json.load(f)


@app.route('/')
def inicio():
    return render_template("index.html")


@app.route('/busqueda', methods=['GET', 'POST'])
def busqueda():
    if request.method == 'POST':
        listado = []
        nombre = request.form.get('buscador', '').lower()
        clima_seleccionado = request.form.get('clima', '')
        for coche in coches_json:
            for prueba in coche["pruebas"]:
                if (prueba["modelo"].lower().startswith(nombre) or nombre == '') and (prueba["condiciones"]["clima"] == clima_seleccionado or clima_seleccionado == ''):
                    listado.append({
                        "id": prueba["id"],
                        "modelo": prueba["modelo"],
                        "consumo_combinado": prueba["consumo"]["combinado"]
                    })
        return render_template('busqueda.html', listado=listado, nombre=nombre, clima_seleccionado=clima_seleccionado)
    else:
        return render_template('busqueda.html', listado=[], nombre='', clima_seleccionado='')


@app.route('/detalle/<id>')
def detalle(id):
    for item in coches_json:
        for prueba in item["pruebas"]:
            if prueba["id"] == id:
                return render_template('detalle.html', prueba=prueba)
    return "Error 404. Este modelo no existe.", 404

app.run("0.0.0.0",5000,debug=True)