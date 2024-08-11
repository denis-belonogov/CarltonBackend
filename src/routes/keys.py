from flask import Blueprint, request, jsonify

from src.db import db
from src.models.key import Key

keys_blueprint = Blueprint('keys', __name__)


def _build_cors_prelight_response():
    response = jsonify({'message': 'CORS preflight response'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


@keys_blueprint.route('/', methods=['GET'])
def get_keys():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    keys = Key.query.all()
    return jsonify({'keys': [key.to_json() for key in keys]})


@keys_blueprint.route('/<int:key_id>', methods=['GET'])
def get_key(key_id):
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    key = Key.query.get_or_404(key_id)
    return jsonify(key.to_json()), 200


@keys_blueprint.route('/', methods=['POST'])
def add_key():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    brand = request.json.get('brand')
    name = request.json.get('name')
    amount = request.json.get('amount')
    if any([brand is None, amount is None]):
        return jsonify({'message': 'Missing data'}), 400
    try:
        new_key = Key(brand=brand, name=name, amount=amount)
        db.session.add(new_key)
        db.session.commit()
        return jsonify({'message': 'Key added'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@keys_blueprint.route('/update/<int:key_id>', methods=['PUT'])
def update_key(key_id):
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    key = Key.query.get_or_404(key_id)
    data = request.get_json()
    for filed_name, field_value in data.items():
        if filed_name == 'rooms':
            continue
        key.__setattr__(filed_name, field_value)
    try:
        db.session.commit()
        return jsonify({'message': 'Key updated'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@keys_blueprint.route('/delete/<int:key_id>', methods=['DELETE'])
def delete_key(key_id):
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    key = Key.query.get_or_404(key_id)
    try:
        db.session.delete(key)
        db.session.commit()
        return jsonify({'message': 'Key deleted'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
