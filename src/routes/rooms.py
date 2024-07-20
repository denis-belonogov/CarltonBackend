from flask import Blueprint, request, jsonify

from src.db import db
from src.models.room import Room, RoomType

rooms_blueprint = Blueprint('rooms', __name__)


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
    room.name = data.get('name', room.name).strip()
    room.type = RoomType[data.get('type', room.type.name)] if data.get('type') else room.type
    room.floor = data.get('floor', room.floor)
    db.session.commit()
    return jsonify(room.to_json()), 200


@rooms_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete_room(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Room deleted successfully'}), 200
