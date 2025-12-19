from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "hhh123",
    "database": "fish_health",
    "charset": "utf8mb4"
}

def get_db():
    return pymysql.connect(**db_config)

@app.route("/api/save_fish_health", methods=["POST"])
def save_fish_health():
    data = request.json

    species = data.get("species")
    frame_id = data.get("frame_id")
    status = data.get("status")
    temperature = data.get("temperature")
    tds = data.get("tds")

    if not species or frame_id is None:
        return jsonify({"msg": "missing key data"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()

        sql = """
        INSERT INTO fish_health (种类, 时隙, 状态, 温度, tds)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            状态 = VALUES(状态),
            温度 = VALUES(温度),
            tds = VALUES(tds)
        """

        cursor.execute(sql, (
            species,
            str(frame_id),
            status,
            temperature,
            tds
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"msg": "ok"})

    except Exception as e:
        return jsonify({"msg": "db error", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
