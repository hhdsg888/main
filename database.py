# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',      # 修改为你的用户名
    'password': '',      # 修改为你的密码
    'database': 'fish_health'
}

# 创建数据库连接
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"数据库连接失败: {err}")
        return None

@app.route('/api/fish-health', methods=['POST'])
def save_fish_health():
    try:
        data = request.json
        print("收到数据:", data)
        
        # 验证必要字段
        required_fields = ['species', 'time_slot', 'status']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'缺少必要字段: {field}'
                }), 400
        
        species = data['species']
        time_slot = data['time_slot']
        status = data['status']
        frame_id = data.get('frame_id', '0')
        
        # 获取数据库连接
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'message': '数据库连接失败'
            }), 500
        
        cursor = conn.cursor()
        
        # 检查表是否存在，如果不存在则创建
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fish_health (
                species VARCHAR(255) NOT NULL,
                time_slot VARCHAR(50) NOT NULL,
                status VARCHAR(50),
                temperature DECIMAL(5,2),
                tds DECIMAL(10,2),
                frame_id INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (species, time_slot)
            )
        """)
        
        # 插入数据（使用ON DUPLICATE KEY UPDATE处理重复）
        sql = """
            INSERT INTO fish_health (species, time_slot, status, frame_id) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            status = VALUES(status), 
            frame_id = VALUES(frame_id),
            created_at = CURRENT_TIMESTAMP
        """
        
        cursor.execute(sql, (species, time_slot, status, frame_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': '数据保存成功',
            'data': {
                'species': species,
                'time_slot': time_slot,
                'status': status,
                'frame_id': frame_id
            }
        })
        
    except Exception as e:
        print(f"保存数据时出错: {e}")
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
        }), 500

@app.route('/api/test-connection', methods=['GET'])
def test_connection():
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            return jsonify({'success': True, 'message': '数据库连接正常'})
        else:
            return jsonify({'success': False, 'message': '数据库连接失败'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    print("启动后端API服务器...")
    print("API地址: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)