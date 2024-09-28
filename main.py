from flask import Flask, render_template, jsonify, request
from config import settings
from datetime import datetime
from logic.turn_taking_logic import AsignadorTurnos
import json
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home/index.html')

@app.route('/api/cajeros')
def api_cajeros():
    return jsonify(settings.CAJEROS)

@app.route('/api/cronogramas', methods=['GET'])
def api_cronogramas():
    return jsonify(settings.CRONOGRAMAS)

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

@app.route('/api/generar_cronograma', methods=['POST'])
def generar_cronograma():
    data = request.json
    tipo_periodo = data.get('tipo_periodo')
    fecha_inicio = data.get('fecha')

    try:
        with open('config/cajeros.json', 'r') as f:
            cajeras = json.load(f)["cajeros"]  # Cargar los cajeros desde el archivo JSON
        
        cajeras_aleatorias = random.sample(cajeras, len(cajeras))
        asignador = AsignadorTurnos(cajeras_aleatorias, tipo_periodo)
        fecha = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        
        # Asignar los turnos para el tipo de periodo seleccionado
        cronograma_dias, informe = asignador.asignar_turnos(fecha)
        #cronograma_dia = asignador.mostrar_cronograma()
        
        # Crear un nuevo objeto cronograma
        nuevo_cronograma = {
            "id": len(settings.CRONOGRAMAS) + 1,  # Generar un ID único basado en la cantidad de cronogramas
            "tipo": tipo_periodo,
            "cronogramas": cronograma_dias,  # Esto debería contener el cronograma para cada día
            "informe": informe  # Esto debería contener el informe de cada empleado
        }
        
        # Guardar el cronograma generado en el archivo JSON
        settings.CRONOGRAMAS.append(nuevo_cronograma)
        settings.guardar_cronogramas(settings.CRONOGRAMAS)
        
        return jsonify({"message": "Cronograma generado exitosamente", "success": True, "cronograma": nuevo_cronograma})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/cronogramas/semana/<int:cronograma_id>')
def cronograma_semana_detalle(cronograma_id):
    # Cargar el cronograma específico desde el JSON
    cronograma = next((c for c in settings.CRONOGRAMAS if c['id'] == cronograma_id and c['tipo'] == 'semana'), None)
    if not cronograma:
        return "Cronograma no encontrado", 404
    return render_template('cronogramas/cronogramas_semana.html', cronograma=cronograma)

@app.route('/cronogramas/mes/<int:cronograma_id>')
def cronograma_mes_detalle(cronograma_id):
    # Cargar el cronograma específico desde el JSON
    cronograma = next((c for c in settings.CRONOGRAMAS if c['id'] == cronograma_id and c['tipo'] == 'mes'), None)
    if not cronograma:
        return "Cronograma no encontrado", 404
    return render_template('cronogramas/cronogramas_mes.html', cronograma=cronograma)

@app.route('/api/cronogramas/<int:cronograma_id>', methods=['DELETE'])
def eliminar_cronograma(cronograma_id):
    # Buscar el índice del cronograma con el ID especificado
    cronograma_index = next((i for i, c in enumerate(settings.CRONOGRAMAS) if c['id'] == cronograma_id), None)
    
    if cronograma_index is not None:
        # Eliminar el cronograma de la lista en memoria
        eliminado = settings.CRONOGRAMAS.pop(cronograma_index)
        
        # Guardar la lista actualizada en el archivo JSON
        try:
            settings.guardar_cronogramas(settings.CRONOGRAMAS)
            return jsonify({'message': 'Cronograma eliminado correctamente', 'cronograma': eliminado}), 200
        except Exception as e:
            # En caso de error al guardar, restaurar el cronograma eliminado
            settings.CRONOGRAMAS.insert(cronograma_index, eliminado)
            return jsonify({'error': f'Error al actualizar el archivo JSON: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Cronograma no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)