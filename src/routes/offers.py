from flask import Blueprint, request, jsonify

from src.html_parser import get_offers

offers_blueprint = Blueprint('offers', __name__)


@offers_blueprint.route('/', methods=['GET'])
def get_offers():
    return jsonify({'offer': get_offers(request.args)})
