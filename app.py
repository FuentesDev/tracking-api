from flask import Flask, request, jsonify
import json
import re
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    """
    Carga y devuelve la lista de paquetes desde el archivo JSON.
    """
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/tracking/<tracking_number>', methods=['GET'])
def get_tracking(tracking_number):
    """
    Endpoint que recibe un número de rastreo de 8 dígitos y
    retorna la información del paquete en formato JSON.
    """
    # Validar que el número de rastreo tenga exactamente 8 dígitos
    if not re.match(r'^\d{8}$', tracking_number):
        return jsonify({"error": "Número de rastreo inválido. Debe tener 8 dígitos."}), 400

    # Cargar datos desde el archivo data.json
    data = load_data()

    # Buscar paquete con ese número de rastreo
    for item in data:
        if item.get("trackingNumber") == tracking_number:
            # Retornar los campos en la estructura requerida
            return jsonify({
                "trakingNumber": item.get("trackingNumber", ""),
                "email": item.get("email", ""),
                "cellphone": item.get("cellphone", ""),
                "address": item.get("address", ""),
                "price": item.get("price", ""),
                "creationDate": item.get("creationDate", ""),
                "deliveryDate": item.get("deliveryDate", ""),
                "size": item.get("size", ""),
                "weight": item.get("weight", ""),
                "pos": item.get("pos", "")
            }), 200

    # Si no encuentra el trackingNumber
    return jsonify({"error": "No se encontró información para este número de rastreo."}), 404

@app.errorhandler(404)
def page_not_found(e):
    """
    Manejo de error para rutas no definidas en el servidor.
    """
    return jsonify({"error": "Endpoint no encontrado."}), 404

@app.errorhandler(500)
def server_error(e):
    """
    Manejo de error para errores internos del servidor.
    """
    return jsonify({"error": "Error interno del servidor."}), 500

if __name__ == '__main__':
    # Ejecutar en modo debug para desarrollo
    app.run(debug=True, host='0.0.0.0', port=5000)
