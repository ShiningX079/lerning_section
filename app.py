from mimetypes import inited
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime, datetime

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('time_record.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            minutes INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute(
        'SELECT minutes FROM time_record WHERE date = ?', (today,))
    records = [row[0] for row in cursor.fetchall()]
    total_minutes = sum(records)
    conn.close()
    return render_template('index.html', total_minutes=total_minutes, records=records)


@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    minutes = data.get('minutes', 0)
    today = datetime.now().strftime('%Y-%m-%d')

    conn = get_db_connection
    cursor = conn.cursor()
    cursor.execute(
        'INSERT  INTO time_record (date,minutes) VALUES (?,?)', (today, minutes))
    conn.commit()
    conn.close()

    return jsonify({'message': f'Saved {minutes} minutes'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
