from flask import Flask, render_template, request, redirect, url_for
from db import get_db, get_tareas_collection
from datetime import datetime
from bson.objectid import ObjectId

db = get_db()
tareas_collection = get_tareas_collection()
app = Flask(__name__)

# Ruta principal
@app.route('/')
def index():
    """
    Muestra la lista de tareas.
    """
    return render_template('index.html', tareas=tareas_collection.find(), tareas_length=tareas_collection.count_documents({}))

@app.route('/add/', methods=['POST'])
def add_task():
    """
    Agrega una nueva tarea a la colección 'tareas'.
    """
    ahora = datetime.now()
    fecha_formateada = ahora.strftime("%Y-%m-%d %H:%M:%S")
    title = request.form.get('titulo')
    tareas_collection.insert_one({'titulo': title, 'fecha': fecha_formateada})
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_task():
    """
    Elimina una tarea de la colección 'tareas'.
    """
    id_to_delete = ObjectId(request.form.get('id'))
    tareas_collection.delete_one({'_id': id_to_delete})
    return redirect(url_for('index'))

@app.route('/edit', methods=['POST'])
def edit_task():
    """
    Edita una tarea en la colección 'tareas'.
    """
    id_to_edit = ObjectId(request.form.get('id'))
    new_title = request.form.get('title')
    print(f"Editing task with ID: {id_to_edit}, new title: {new_title}")
    tareas_collection.update_one(
      {'_id': id_to_edit},
      {'$set': {'titulo': new_title}}
    )
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
