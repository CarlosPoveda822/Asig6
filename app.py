import json
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

recetas_file = 'recetas.json'

try:
    with open(recetas_file, 'r') as f:
        recetas = json.load(f)
except FileNotFoundError:
    recetas = []

def guardar_recetas(recetas):
    with open(recetas_file, 'w') as f:
        json.dump(recetas, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_receta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ingredientes = request.form['ingredientes']
        pasos = request.form['pasos']
        nueva_receta = {
            "id": str(len(recetas) + 1),
            "nombre": nombre,
            "ingredientes": ingredientes.split(', '),
            "pasos": pasos.split('. ')
        }
        recetas.append(nueva_receta)
        guardar_recetas(recetas)
        return redirect(url_for('ver_listado'))
    return render_template('agregar.html')

@app.route('/eliminar/<string:id_receta>', methods=['POST'])
def eliminar_receta(id_receta):
    global recetas
    recetas = [receta for receta in recetas if receta.get('id') != id_receta]
    guardar_recetas(recetas)
    return redirect(url_for('ver_listado'))

@app.route('/recetas')
def ver_listado():
    return render_template('ver_listado.html', recetas=recetas)

@app.route('/buscar/ingredientes', methods=['GET', 'POST'])
def buscar_ingredientes():
    if request.method == 'GET' and 'ingredientes' in request.args:
        ingredientes_buscar = request.args['ingredientes'].split(', ')
        recetas_encontradas = [
            receta for receta in recetas
            if all(ingrediente in receta['ingredientes'] for ingrediente in ingredientes_buscar)
        ]
        return render_template('buscar_ingredientes.html', recetas=recetas_encontradas)
    return render_template('buscar_ingredientes.html')

@app.route('/buscar/pasos', methods=['GET', 'POST'])
def buscar_pasos():
    if request.method == 'GET' and 'pasos' in request.args:
        pasos_buscar = request.args['pasos'].split('. ')
        recetas_encontradas = [
            receta for receta in recetas
            if all(paso in receta['pasos'] for paso in pasos_buscar)
        ]
        return render_template('buscar_pasos.html', recetas=recetas_encontradas)
    return render_template('buscar_pasos.html')

@app.route('/receta/<string:id_receta>')
def ver_receta(id_receta):
    receta = next((receta for receta in recetas if receta.get('id') == id_receta), None)
    if receta:
        return render_template('ver_receta.html', receta=receta)
    return "Receta no encontrada."

if __name__ == '__main__':
    app.run(debug=True)



