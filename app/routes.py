from flask import Blueprint, jsonify, request
from app.analysis import cal_data, predict_increase, get_stock_code

main = Blueprint('main', __name__)

# 기본 라우트 추가
@main.route('/')
def home():
    return jsonify({"message": "Welcome to Stock Analysis API"})

@main.route('/analyze')
def analyze():
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "Stock code is required"}), 400
    result = cal_data(code)
    return jsonify(result)

@main.route('/predict')
def predict():
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "Stock code is required"}), 400
    result = predict_increase(code)
    return jsonify(result)

@main.route('/search')
def search():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
    result = get_stock_code(keyword)
    return jsonify(result)
