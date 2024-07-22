from flask import Blueprint, request, jsonify

from src.db import db
from src.models.key import Key

keys_blueprint = Blueprint('keys', __name__)


@keys_blueprint.route('/', methods=['GET'])
def get_keys():
    keys = Key.query.all()
    return jsonify({'keys': [key.to_json() for key in keys]})


@keys_blueprint.route('/', methods=['POST'])
def add_key():
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
    key = Key.query.get_or_404(key_id)
    data = request.get_json()
    key.brand = data.get('brand', key.brand)
    key.name = data.get('name', key.name)
    key.amount = data.get('amount', key.amount)
    try:
        db.session.commit()
        return jsonify({'message': 'Key updated'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@keys_blueprint.route('/delete/<int:key_id>', methods=['DELETE'])
def delete_key(key_id):
    key = Key.query.get_or_404(key_id)
    try:
        db.session.delete(key)
        db.session.commit()
        return jsonify({'message': 'Key deleted'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
