from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

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

@app.route("/api/save_fish_health", methods=["POST"])
def save_fish_health():
    data = request.json
    
    # 根据第一个代码的字段名，调整参数名称
    species = data.get("species")
    timeslot = data.get("timeslot")  # 改为timeslot，对应数据库的"时隙"字段
    status = data.get("status")
    temperature = data.get("temperature")
    tds = data.get("tds")
    
    # 检查必要字段
    if not species or not timeslot:
        return jsonify({
            "success": False,
            "msg": "缺少必要数据: species 和 timeslot 必须提供"
        }), 400
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # 使用与第一个代码一致的字段名
        sql = """
        INSERT INTO fish_health (种类, 时隙, 状态, 温度, tds)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            状态 = VALUES(状态),
            温度 = VALUES(温度),
            tds = VALUES(tds)
        """
        
        # 执行SQL，参数顺序与SQL中的字段顺序一致
        cursor.execute(sql, (
            species,        # 对应 种类
            timeslot,       # 对应 时隙
            status,         # 对应 状态
            temperature,    # 对应 温度
            tds             # 对应 tds
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "msg": "数据保存成功"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "msg": "数据库错误",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)