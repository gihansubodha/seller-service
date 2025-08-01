# seller_service/app.py
from flask import Flask, request, jsonify
from auth_utils import require_token,get_db

app = Flask(__name__)

@app.route("/orders", methods=["GET","POST","PUT","DELETE"])
@require_token(role="seller")
def slr_orders():
    conn,cur=get_db(),get_db().cursor(dictionary=True)
    if request.method=="GET":
        cur.execute("SELECT * FROM orders"); return jsonify(cur.fetchall())
    d=request.json
    if request.method=="POST":
        cur.execute("INSERT INTO orders(blanket_name,quantity,customer_name) VALUES(%s,%s,%s)",
                    (d["blanket_name"],d["quantity"],d["customer_name"]))
        conn.commit(); return jsonify({"msg":"Order placed"}),201
    if request.method=="PUT":
        cur.execute("UPDATE orders SET status=%s WHERE id=%s",(d["status"],d["id"]))
        conn.commit(); return jsonify({"msg":"Status updated"})
    if request.method=="DELETE":
        cur.execute("DELETE FROM orders WHERE id=%s",(d["id"],))
        conn.commit(); return jsonify({"msg":"Deleted"})
    return "",400

@app.route("/request_inventory", methods=["POST"])
@require_token(role="seller")
def req_dist():
    d=request.json
    import requests
    resp = requests.post("https://your-distributor-url/orders", json=d, headers=request.headers)
    return jsonify(resp.json()), resp.status_code

if __name__=="__main__":
    app.run(debug=True)
