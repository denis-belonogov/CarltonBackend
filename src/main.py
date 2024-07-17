import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from src.config import config_by_name
from src.db import db
from src.routes.keys import keys_blueprint
from src.routes.offers import offers_blueprint
from src.routes.rooms import rooms_blueprint

load_dotenv()

environment = os.getenv('FLASK_ENV', 'default')

app = Flask(__name__)
CORS(app)
app.config.from_object(config_by_name[environment])

db.init_app(app)

app.register_blueprint(keys_blueprint, url_prefix='/keys')
app.register_blueprint(offers_blueprint, url_prefix='/offers')
app.register_blueprint(rooms_blueprint, url_prefix='/rooms')


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Carlton Tools API!'})


# Global error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(ssl_context='adhoc')
