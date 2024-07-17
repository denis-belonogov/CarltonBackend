import enum
import os

from dotenv import dotenv_values
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from htmlParser import get_offers

config = dotenv_values(".env")

load_dotenv(find_dotenv())

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carlton_keys.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class RoomType(enum.Enum):
    GUEST = 1
    STAFF = 2


key_room = db.Table('key_room',
                    db.Column('room_id', db.Integer, db.ForeignKey('room.id'), primary_key=True),
                    db.Column('key_id', db.Integer, db.ForeignKey('key.id'), primary_key=True)
                    )


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    type = db.Column(db.Enum(RoomType), nullable=False, unique=False)
    floor = db.Column(db.Integer, nullable=False, unique=False)
    keys = db.relationship('Key', secondary=key_room, lazy='subquery',
                           backref=db.backref('room', lazy=True))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'floor': self.floor,
            'keys': [key.to_json() for key in self.keys]
        }

    def __repr__(self):
        return f"Room('{self.id}')"


class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(20), nullable=False, unique=False)
    name = db.Column(db.String(20), nullable=False, unique=True)
    amount = db.Column(db.Integer, nullable=False, unique=False)
    rooms = db.relationship('Room', secondary=key_room, lazy='subquery',
                            backref=db.backref('key', lazy=True))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'room_name': self.room_name,
            'amount': self.amount,
            'rooms': [room.to_json() for room in self.rooms]
        }

    def __repr__(self):
        return f"Key('{self.id}')"


@app.route('/', methods=['GET'])
def home():
    return jsonify({'offer': get_offers(request.args)})


@app.route('/keys', methods=['GET'])
def get_keys():
    keys = Key.query.all()
    return jsonify({'keys': [key.to_json() for key in keys]})


@app.route('/keys', methods=['POST'])
def add_key():
    data = request.get_json()
    brand = data['brand']
    name = data['name']
    amount = data['amount']
    room_name = data['room_name']
    if not name or not amount or not brand or not room_name:
        return jsonify({'message': 'Missing data'}), 400
    new_key = Key(brand=brand, name=name, amount=amount, room_name=room_name)
    try:
        db.session.add(new_key)
        db.session.commit()
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    return jsonify({'message': 'Key added'}, 201)


@app.route('/keys/<int:key_id>', methods=['DELETE'])
def delete_key(key_id):
    key = Key.query.get(key_id)
    if key:
        db.session.delete(key)
        db.session.commit()
        return jsonify({'message': 'Key deleted'})
    return jsonify({'message': 'Key not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=os.getenv('DEBUG') == "True", ssl_context='adhoc')
