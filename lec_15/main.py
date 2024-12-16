from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

data_file = 'cars.json'

def read_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return []


def write_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)


@app.route('/cars', methods=['GET'])
def get_cars():
    cars = read_data()
    return jsonify(cars)


@app.route('/cars/<int:id>', methods=['GET'])
def get_car(id):
    cars = read_data()
    car = next((car for car in cars if car['id'] == id), None)
    if car:
        return jsonify(car)
    return jsonify({"message": "Car not found"}), 404


@app.route('/cars', methods=['POST'])
def add_car():
    new_car = request.get_json()
    cars = read_data()
    new_car['id'] = cars[-1]['id'] + 1 if cars else 1  
    cars.append(new_car)
    write_data(cars)
    return jsonify(new_car), 201


@app.route('/cars/<int:id>', methods=['PUT'])
def update_car(id):
    updated_car = request.get_json()
    cars = read_data()
    car = next((car for car in cars if car['id'] == id), None)
    if car:
        car.update(updated_car)
        write_data(cars)
        return jsonify(car)
    return jsonify({"message": "Car not found"}), 404


@app.route('/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    cars = read_data()
    car = next((car for car in cars if car['id'] == id), None)
    if car:
        cars.remove(car)
        write_data(cars)
        return jsonify({"message": "Car deleted"})
    return jsonify({"message": "Car not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
