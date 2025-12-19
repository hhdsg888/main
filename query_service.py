from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="hhh123",
        database="fish_health",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/api/fish_health/query", methods=["POST"])
def query_fish_health():
    data = request.json or {}
    species = data.get("species", "")
    timeslot = data.get("timeslot", "")

    sql = "SELECT 种类, 时隙, 状态, 温度, tds FROM fish_health WHERE 1=1"
    params = []

    if species:
        sql += " AND 种类 LIKE %s"
        params.append("%" + species + "%")

    if timeslot:
        sql += " AND 时隙 LIKE %s"
        params.append("%" + timeslot + "%")

    sql += " ORDER BY 时隙 DESC LIMIT 50"

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    result = []
    for r in rows:
        item = {
            "species": r["种类"],
            "timeslot": r["时隙"],
            "status": r["状态"],
            "temperature": float(r["温度"]) if r["温度"] is not None else None,
            "tds": float(r["tds"]) if r["tds"] is not None else None
        }
        result.append(item)

    return jsonify({
        "success": True,
        "count": len(result),
        "data": result
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
