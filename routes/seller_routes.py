from flask import request, jsonify
from app import app
from db_config import get_connection

@app.route("/", methods=["GET"])
def home():
    return "running. use /orders"


@app.route("/orders", methods=["GET"])
def get_orders():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM seller_orders")
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/orders", methods=["POST"])
def add_order():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO seller_orders (customer_name, blanket_model, quantity, order_date) VALUES (%s, %s, %s, %s)", 
                       (data["customer_name"], data["blanket_model"], data["quantity"], data["order_date"]))
        conn.commit()
        return jsonify({"message": "Order added!"})
    except Exception as e:
        return jsonify({"error": str(e)})
