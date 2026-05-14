from flask import Flask, request, jsonify
from database import db
from curd import PatientCRUD


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Patient Management API Running"

@app.route('/patients', methods=['POST'])
def create_patient():
    data = request.get_json()
    patient = PatientCRUD.create_patient(data)
    return jsonify({"message": "Patient created", "id": patient.id})

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = PatientCRUD.get_all_patients()
    result = []
    for p in patients:
        result.append({
            "id": p.id,
            "first_name": p.first_name,
            "last_name": p.last_name,
            "address": p.address,
            "email": p.email,
            "phone": p.phone
        })
    return jsonify(result)

@app.route('/patients/<int:id>', methods=['GET'])
def get_patient(id):
    patient = PatientCRUD.get_patient_by_id(id)
    if not patient:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "id": patient.id,
        "first_name": patient.first_name,
        "last_name": patient.last_name,
        "address": patient.address,
        "email": patient.email,
        "phone": patient.phone
    })

@app.route('/patients/<int:id>', methods=['PUT'])
def update_patient(id):
    data = request.get_json()
    patient = PatientCRUD.update_patient(id, data)

    if not patient:
        return jsonify({"error": "Not found"}), 404

    return jsonify({"message": "Updated successfully"})

@app.route('/patients/<int:id>', methods=['DELETE'])
def delete_patient(id):
    success = PatientCRUD.delete_patient(id)

    if not success:
        return jsonify({"error": "Not found"}), 404

    return jsonify({"message": "Deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)