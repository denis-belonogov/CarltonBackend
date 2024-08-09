from flask import Blueprint, request, jsonify

from src.db import db
from src.models.key import Key
from src.models.room import Room, RoomType

rooms_blueprint = Blueprint('rooms', __name__)


def _build_cors_prelight_response():
    response = jsonify({'message': 'CORS preflight response'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


@rooms_blueprint.route('/', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify({'rooms': [room.to_json() for room in rooms]}), 200


@rooms_blueprint.route('/<int:id>', methods=['GET'])
def get_room(id):
    room = Room.query.get_or_404(id)
    return jsonify(room.to_json()), 200


@rooms_blueprint.route('/', methods=['POST'])
def add_room():
    data = request.get_json()
    if any([data.get('name') is None, data.get('type') is None, data.get('floor') is None]):
        return jsonify({'message': 'Missing data'}), 400
    try:
        room = Room(name=data['name'], type=RoomType(int(data['type'])), floor=data['floor'])
        db.session.add(room)
        db.session.commit()
        return jsonify(room.to_json()), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@rooms_blueprint.route('/update/<int:id>', methods=['PUT'])
def update_room(id):
    room = Room.query.get_or_404(id)
    data = request.get_json()
    for field_name, field_value in data.items():
        room.__setattr__(field_name, field_value)
    db.session.commit()
    return jsonify(room.to_json()), 200


@rooms_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete_room(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Room deleted successfully'}), 200


@rooms_blueprint.route('/update/<int:room_id>/add_key/<int:key_id>', methods=['POST'])
def add_key_to_room(room_id, key_id):
    room = Room.query.get_or_404(room_id)
    key = Key.query.get_or_404(key_id)
    room.keys.append(key)
    try:
        db.session.commit()
        return jsonify({'message': 'Key added to room'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@rooms_blueprint.route('/update/<int:room_id>/remove_key/<int:key_id>', methods=['POST'])
def remove_key_from_room(room_id, key_id):
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    room = Room.query.get_or_404(room_id)
    key = Key.query.get_or_404(key_id)
    room.keys.remove(key)
    try:
        db.session.commit()
        return jsonify({'message': 'Key removed from room'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
