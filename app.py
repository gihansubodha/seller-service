from flask import Flask, request, jsonify
import jwt
from functools import wraps
from db_config import get_connection

app = Flask(__name__)
AUTH_SECRET = "your_auth_secret"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").split(" ")[-1]
        if not token:
            return jsonify({"message": "Token required"}), 401
        try:
            jwt.decode(token, AUTH_SECRET, algorithms=["HS256"])
        except:
            return jsonify({"message": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/orders", methods=["GET"])
@token_required
def get_orders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route("/orders", methods=["POST"])
@token_required
def place_order():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (name, customer, quantity, min_stock) VALUES (%s, %s, %s, %s)",
                   (data["name"], data["customer"], data["quantity"], data["min_stock"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Order added"})

@app.route("/request_distributor", methods=["POST"])
@token_required
def request_to_distributor():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO distributor_orders (blanket_name, quantity, status) VALUES (%s, %s, %s)",
                   (data["blanket_name"], data["quantity"], "pending"))
    conn.commit()
    conn.close()
    return jsonify({"message": "Request sent to distributor"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
