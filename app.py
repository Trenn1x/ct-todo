from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, os
import os, sqlite3
DB = 'tasks.db'

# one‑time DB setup
if not os.path.exists(DB):
    conn = sqlite3.connect(DB)
    conn.execute('CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT)')
    conn.commit()
    conn.close()


app = Flask(__name__)
CORS(app)
DB = 'tasks.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/tasks', methods=['GET'])
def list_tasks():
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute('SELECT id, title FROM tasks').fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/tasks', methods=['POST'])
def add_task():
    title = request.json.get('title','').strip()
    if not title:
        return jsonify(error="Title required"), 400
    with sqlite3.connect(DB) as conn:
        cur = conn.execute('INSERT INTO tasks (title) VALUES (?)',(title,))
        task_id = cur.lastrowid
    return jsonify(id=task_id, title=title), 201

@app.route('/tasks/<int:id>', methods=['DELETE'])
def del_task(id):
    with sqlite3.connect(DB) as conn:
        conn.execute('DELETE FROM tasks WHERE id=?',(id,))
    return '', 204

if __name__=='__main__':
    app.run(debug=True)

