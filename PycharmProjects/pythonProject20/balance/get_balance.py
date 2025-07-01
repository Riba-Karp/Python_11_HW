from flask import Blueprint, jsonify
from balance.data import balance

get_bp = Blueprint("get_balance", __name__)

@get_bp.route('/balance', methods=['GET'])
def get_balance():
    return jsonify({"balance": balance}), 200
