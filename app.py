from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from db_config import get_db_connection

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["*"])

#  GET Seller Stock
@app.route('/stock/<int:seller_id>', methods=['GET'])
def get_seller_stock(seller_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM seller_stock WHERE seller_id=%s", (seller_id,))
    stock = cursor.fetchall()
    conn.close()
    return jsonify(stock)

#  ADD New Stock Item (with model_number, price)
@app.route('/stock', methods=['POST'])
def add_seller_stock():
    data = request.json or {}
    seller_id = data.get('seller_id')
    blanket_model = data.get('blanket_model')
    model_number = data.get('model_number')    # optional
    price = data.get('price')                  # optional
    quantity = data.get('quantity', 0)
    min_required = data.get('min_required', 5)

    if not seller_id or not blanket_model:
        return jsonify({"msg": "seller_id and blanket_model are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO seller_stock (seller_id, blanket_model, model_number, price, quantity, min_required)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (seller_id, blanket_model, model_number, price, quantity, min_required))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Stock item added"})

#  UPDATE Stock Quantity
@app.route('/stock/<int:stock_id>', methods=['PUT'])
def update_seller_stock(stock_id):
    data = request.json or {}
    quantity = data.get('quantity')
    if quantity is None:
        return jsonify({"msg": "quantity is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE seller_stock SET quantity=%s WHERE id=%s", (quantity, stock_id))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Stock updated"})

#  DELETE Stock Item
@app.route('/stock/<int:stock_id>', methods=['DELETE'])
def delete_seller_stock(stock_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM seller_stock WHERE id=%s", (stock_id,))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Stock item deleted"})

#  SEND Stock Request to Distributor (unchanged payload)
@app.route('/request-stock', methods=['POST'])
def request_stock():
    data = request.json or {}
    seller_id = data.get('seller_id')
    distributor_id = data.get('distributor_id')
    blanket_model = data.get('blanket_model')
    quantity = data.get('quantity')

    if not seller_id or not distributor_id or not blanket_model or quantity is None:
        return jsonify({"msg": "seller_id, distributor_id, blanket_model, quantity are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO seller_requests (seller_id, distributor_id, blanket_model, quantity)
        VALUES (%s, %s, %s, %s)
    """, (seller_id, distributor_id, blanket_model, quantity))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Stock request sent to distributor"})

#  AUTO CHECK Low Stock (now returns more fields too)
@app.route('/check-low-stock/<int:seller_id>', methods=['GET'])
def check_low_stock(seller_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, blanket_model, model_number, price, quantity, min_required
        FROM seller_stock
        WHERE seller_id=%s AND quantity < min_required
    """, (seller_id,))
    low_stock = cursor.fetchall()
    conn.close()
    return jsonify({"low_stock": low_stock})

#  Health Check
@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "Seller Service Running"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
