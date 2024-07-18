from flask import Blueprint, request, jsonify

from src.html_parser import generate_offers_text

offers_blueprint = Blueprint('offers', __name__)


@offers_blueprint.route('/', methods=['GET'])
def get_offers():
    return jsonify({'offer': generate_offers_text(request.args)})
