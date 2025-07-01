from flask import Blueprint, request, jsonify
from balance.data import balance

post_bp = Blueprint('post_balance', __name__)

@post_bp.route('/balance', methods=['POST'])
def add_balance():
    data = request.get_json()

    balance.append(data)
    return jsonify({"added_balance": data}), 201

