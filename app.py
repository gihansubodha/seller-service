from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from db_config import get_db_connection

app = Flask(__name__)
CORS(app)

# GET Seller Stock
@app.route('/stock/<int:seller_id>', methods=['GET'])
def get_seller_stock(seller_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM seller_stock WHERE seller_id=%s", (seller_id,))
    stock = cursor.fetchall()
    conn.close()
    return jsonify(stock)

# ADD New Stock Item
@app.route('/stock', methods=['POST'])
def add_seller_stock():
    data = request.json
    seller_id = data['seller_id']
    blanket_model = data['blanket_model']
    quantity = data['quantity']
    min_required = data.get('min_required', 5)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO seller_stock (seller_id, blanket_model, quantity, min_required) VALUES (%s, %s, %s, %s)",
                   (seller_id, blanket_model, quantity, min_required))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Stock item added"})

# UPDATE Stock Quantity
@app.route('/stock/<int:stock_id>', methods=['PUT'])
def update_seller_stock(stock_id):
    data = request.json
    quantity = data['quantity']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE seller_stock SET quantity=%s WHERE id=%s", (quantity, stock_id))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Stock updated"})

# DELETE Stock Item
@app.route('/stock/<int:stock_id>', methods=['DELETE'])
def delete_seller_stock(stock_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM seller_stock WHERE id=%s", (stock_id,))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Stock item deleted"})

# SEND Stock Request to Distributor
@app.route('/request-stock', methods=['POST'])
def request_stock():
    data = request.json
    seller_id = data['seller_id']
    distributor_id = data['distributor_id']
    blanket_model = data['blanket_model']
    quantity = data['quantity']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO seller_requests (seller_id, distributor_id, blanket_model, quantity) VALUES (%s, %s, %s, %s)",
                   (seller_id, distributor_id, blanket_model, quantity))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Stock request sent to distributor"})

# AUTO CHECK Low Stock
@app.route('/check-low-stock/<int:seller_id>', methods=['GET'])
def check_low_stock(seller_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM seller_stock WHERE seller_id=%s AND quantity < min_required", (seller_id,))
    low_stock = cursor.fetchall()
    conn.close()
    return jsonify({"low_stock": low_stock})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
