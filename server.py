from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder='')

DB_FILE = 'greetings.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS greetings (
                name TEXT PRIMARY KEY,
                count INTEGER NOT NULL
            )
        ''')

@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

@app.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('css', path)

@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('js', path)

@app.route('/greet', methods=['POST'])
def greet():
    data = request.get_json()
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Invalid name'}), 400

    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute('SELECT count FROM greetings WHERE name = ?', (name,))
        row = cur.fetchone()
        if row:
            count = row[0] + 1
            cur.execute('UPDATE greetings SET count = ? WHERE name = ?', (count, name))
        else:
            count = 1
            cur.execute('INSERT INTO greetings (name, count) VALUES (?, ?)', (name, count))
        conn.commit()

    return jsonify({'message': f'Hello {name}!', 'count': count})

@app.route("/stats")
def stats():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT name, count FROM greetings ORDER BY count DESC")
        rows = cur.fetchall()
        results = [{"name": row["name"], "count": row["count"]} for row in rows]
    return jsonify(results)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8000)


