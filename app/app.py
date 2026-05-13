from flask import Flask, jsonify
import pymysql
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host=DB_HOST, user=DB_USER,
        password=DB_PASSWORD, database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "2-Tier App is Live!"})

@app.route('/health')
def health():
    try:
        conn = get_db()
        conn.close()
        return jsonify({"status": "healthy", "db": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
