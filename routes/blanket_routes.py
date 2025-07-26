from flask import request, jsonify
from app import app
from db_config import get_connection

@app.route('/blankets', methods=['GET'])
def get_blankets():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM blankets")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)})
