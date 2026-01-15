"""Unit tests for the Todo Flask API."""
import json


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_returns_200(self, client):
        """Health endpoint should return 200 status."""
        response = client.get('/api/health')
        assert response.status_code == 200

    def test_health_returns_healthy_status(self, client):
        """Health endpoint should return healthy status."""
        response = client.get('/api/health')
        data = response.get_json()
        assert data['status'] == 'healthy'

    def test_health_returns_timestamp(self, client):
        """Health endpoint should return a timestamp."""
        response = client.get('/api/health')
        data = response.get_json()
        assert 'timestamp' in data
        assert len(data['timestamp']) > 0


class TestGetTodos:
    """Tests for getting todos."""

    def test_get_todos_empty(self, client):
        """Should return empty list when no todos exist."""
        response = client.get('/api/todos')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_todos_with_data(self, client, sample_todo):
        """Should return todos when they exist."""
        response = client.get('/api/todos')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Test Todo'

    def test_get_todos_multiple(self, client):
        """Should return multiple todos."""
        client.post('/api/todos', json={'title': 'Todo 1'})
        client.post('/api/todos', json={'title': 'Todo 2'})
        client.post('/api/todos', json={'title': 'Todo 3'})

        response = client.get('/api/todos')
        data = response.get_json()
        assert len(data) == 3


class TestCreateTodo:
    """Tests for creating todos."""

    def test_create_todo_success(self, client):
        """Should create a todo successfully."""
        response = client.post('/api/todos',
                               json={'title': 'New Todo'},
                               content_type='application/json')
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'New Todo'
        assert data['completed'] in [False, 0]
        assert 'id' in data

    def test_create_todo_missing_title(self, client):
        """Should return 400 when title is missing."""
        response = client.post('/api/todos',
                               json={},
                               content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Title is required' in data['error']

    def test_create_todo_empty_title(self, client):
        """Should return 400 when title is empty."""
        response = client.post('/api/todos',
                               json={'title': '   '},
                               content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'empty' in data['error'].lower()

    def test_create_todo_no_json(self, client):
        """Should return 400 when no JSON body is provided."""
        response = client.post('/api/todos',
                               content_type='application/json')
        assert response.status_code == 400

    def test_create_todo_strips_whitespace(self, client):
        """Should strip whitespace from title."""
        response = client.post('/api/todos',
                               json={'title': '  Trimmed Title  '},
                               content_type='application/json')
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'Trimmed Title'


class TestUpdateTodo:
    """Tests for updating todos."""

    def test_update_todo_completed(self, client, sample_todo):
        """Should update todo completed status."""
        todo_id = sample_todo['id']
        response = client.put(f'/api/todos/{todo_id}',
                              json={'completed': True},
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['completed'] in [True, 1]

    def test_update_todo_title(self, client, sample_todo):
        """Should update todo title."""
        todo_id = sample_todo['id']
        response = client.put(f'/api/todos/{todo_id}',
                              json={'title': 'Updated Title'},
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Updated Title'

    def test_update_todo_empty_title(self, client, sample_todo):
        """Should return 400 when updating with empty title."""
        todo_id = sample_todo['id']
        response = client.put(f'/api/todos/{todo_id}',
                              json={'title': '   '},
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_update_todo_not_found(self, client):
        """Should return 404 when todo doesn't exist."""
        response = client.put('/api/todos/99999',
                              json={'completed': True},
                              content_type='application/json')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_update_todo_both_fields(self, client, sample_todo):
        """Should update both completed and title."""
        todo_id = sample_todo['id']
        response = client.put(f'/api/todos/{todo_id}',
                              json={'completed': True, 'title': 'New Title'},
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['completed'] in [True, 1]
        assert data['title'] == 'New Title'


class TestDeleteTodo:
    """Tests for deleting todos."""

    def test_delete_todo_success(self, client, sample_todo):
        """Should delete todo successfully."""
        todo_id = sample_todo['id']
        response = client.delete(f'/api/todos/{todo_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

        # Verify it's deleted
        get_response = client.get('/api/todos')
        todos = get_response.get_json()
        assert len(todos) == 0

    def test_delete_todo_not_found(self, client):
        """Should return 404 when todo doesn't exist."""
        response = client.delete('/api/todos/99999')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'not found' in data['error'].lower()


class TestIndexRoute:
    """Tests for the index route."""

    def test_index_returns_html(self, client):
        """Index route should return HTML content."""
        response = client.get('/')
        assert response.status_code == 200
