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
   arrival_date = request.args.get('arrival_date')
   departure_date = request.args.get('departure_date')
   n_guests = int(request.args.get('n_guests'))
   return jsonify({'offer': get_offers(arrival_date, departure_date, n_guests)})


if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG'), ssl_context='adhoc')