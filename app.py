from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    """Create a database connection"""
    if DATABASE_URL:
        # For Render PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
    else:
        # For local development with SQLite fallback
        import sqlite3
        conn = sqlite3.connect('todos.db')
        conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with todos table"""
    conn = get_db_connection()
    cursor = conn.cursor()

    if DATABASE_URL:
        # PostgreSQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    else:
        # SQLite
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('frontend', 'index.html')

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor) if DATABASE_URL else conn.cursor()
    cursor.execute('SELECT * FROM todos ORDER BY created_at DESC')
    todos = cursor.fetchall()
    conn.close()

    if DATABASE_URL:
        return jsonify([dict(todo) for todo in todos])
    else:
        return jsonify([dict(todo) for todo in todos])

@app.route('/api/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    title = data['title'].strip()
    if not title:
        return jsonify({'error': 'Title cannot be empty'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor) if DATABASE_URL else conn.cursor()

    if DATABASE_URL:
        cursor.execute(
            'INSERT INTO todos (title) VALUES (%s) RETURNING *',
            (title,)
        )
        todo = cursor.fetchone()
    else:
        cursor.execute(
            'INSERT INTO todos (title) VALUES (?)',
            (title,)
        )
        todo_id = cursor.lastrowid
        cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
        todo = cursor.fetchone()

    conn.commit()
    conn.close()

    return jsonify(dict(todo)), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo"""
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor) if DATABASE_URL else conn.cursor()

    if 'completed' in data:
        if DATABASE_URL:
            cursor.execute(
                'UPDATE todos SET completed = %s WHERE id = %s RETURNING *',
                (data['completed'], todo_id)
            )
            todo = cursor.fetchone()
        else:
            cursor.execute(
                'UPDATE todos SET completed = ? WHERE id = ?',
                (data['completed'], todo_id)
            )
            cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
            todo = cursor.fetchone()

    if 'title' in data:
        title = data['title'].strip()
        if not title:
            conn.close()
            return jsonify({'error': 'Title cannot be empty'}), 400

        if DATABASE_URL:
            cursor.execute(
                'UPDATE todos SET title = %s WHERE id = %s RETURNING *',
                (title, todo_id)
            )
            todo = cursor.fetchone()
        else:
            cursor.execute(
                'UPDATE todos SET title = ? WHERE id = ?',
                (title, todo_id)
            )
            cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
            todo = cursor.fetchone()

    conn.commit()
    conn.close()

    if todo:
        return jsonify(dict(todo))
    else:
        return jsonify({'error': 'Todo not found'}), 404

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    conn = get_db_connection()
    cursor = conn.cursor()

    if DATABASE_URL:
        cursor.execute('DELETE FROM todos WHERE id = %s', (todo_id,))
    else:
        cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))

    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()

    if deleted:
        return jsonify({'message': 'Todo deleted successfully'})
    else:
        return jsonify({'error': 'Todo not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
