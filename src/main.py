from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_cors import CORS
from htmlParser import get_offers

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET'])
def home():
    return jsonify({'offer': get_offers(request.args)})


if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG'), ssl_context='adhoc')
