from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_cors import CORS
from htmlParser import get_offers

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carlton_keys.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    amount = db.Column(db.Integer, nullable=False, unique=False)
    holders = db.Column(db.Array, default=[], nullable=False)


    def to_json(self):
        return {
            'name': self.name,
            'amount': self.amount,
            'holders': self.holders
        }
    def __repr__(self):
        return f"Key('{self.key}')"


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
    name = data['name']
    amount = data['amount']
    holders = data['holders']
    if not name or not amount or not holders:
        return jsonify({'message': 'Missing data'}), 400
    new_key = Key(key=data['key'], amount=data['amount'], holders=data['holders'])
    try:
        db.session.add(new_key)
        db.session.commit()
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    return jsonify({'message': 'Key added'}, 201)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=os.getenv('DEBUG'), ssl_context='adhoc')
