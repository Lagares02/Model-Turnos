from flask import Flask, render_template, jsonify, request
from config import settings

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home/index.html')

@app.route('/api/cajeros')
def api_cajeros():
    return jsonify(settings.CAJEROS)

@app.route('/api/add_cajero', methods=['POST'])
def add_cajero():
    nuevo_cajero = request.json
    nombre = nuevo_cajero.get('nombre').upper()  # Convertir el nombre a mayúsculas
    cargo = nuevo_cajero.get('cargo')

    if nombre in settings.CAJEROS:
        return jsonify({"message": f"El empleado {nombre} ya se encuentra añadido", "success": False})

    if cargo == "Cajero(a)":
        settings.CAJEROS.append(nombre)
        settings.guardar_cajeros(settings.CAJEROS)
        return jsonify({"message": "Empleado ingresado exitosamente", "success": True})
    else:
        return jsonify({"message": "Solo se pueden agregar empleados con el cargo 'Cajero(a)'", "success": False})

@app.route('/api/eliminar_cajero', methods=['POST'])
def eliminar_cajero():
    nombre = request.json.get('nombre').upper()  # Convertir el nombre a mayúsculas para asegurarse de coincidir con el formato guardado
    
    if nombre in settings.CAJEROS:
        # Eliminar el cajero de la lista
        settings.CAJEROS = [cajero for cajero in settings.CAJEROS if cajero != nombre]
        
        # Guardar la lista actualizada en el archivo JSON
        settings.guardar_cajeros(settings.CAJEROS)
        
        return jsonify({"message": f"Empleado {nombre} eliminado exitosamente.", "success": True})
    else:
        return jsonify({"message": f"Empleado {nombre} no encontrado.", "success": False})

if __name__ == '__main__':
    app.run(debug=True)