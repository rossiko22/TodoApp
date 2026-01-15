"""Pytest configuration and fixtures for testing the Todo Flask API."""
import pytest
import os
import tempfile


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Ensure tests use SQLite (not PostgreSQL) by clearing DATABASE_URL."""
    monkeypatch.delenv('DATABASE_URL', raising=False)


@pytest.fixture
def app():
    """Create a test Flask application with a temporary database."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix='.db')

    # Set environment to use the temp database
    os.environ.pop('DATABASE_URL', None)

    # Import app after setting environment
    import app as todo_app

    # Store original db path and override for testing
    original_get_db = todo_app.get_db_connection

    def get_test_db_connection():
        import sqlite3
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    todo_app.get_db_connection = get_test_db_connection

    # Initialize the test database
    conn = get_test_db_connection()
    cursor = conn.cursor()
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

    todo_app.app.config['TESTING'] = True

    yield todo_app.app

    # Cleanup
    todo_app.get_db_connection = original_get_db
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def sample_todo(client):
    """Create a sample todo for testing."""
    response = client.post('/api/todos',
                           json={'title': 'Test Todo'},
                           content_type='application/json')
    return response.get_json()
