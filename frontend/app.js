// API base URL - works both locally and on Render
const API_BASE = window.location.origin;

let todos = [];

// Fetch all todos from the backend
async function fetchTodos() {
    try {
        const response = await fetch(`${API_BASE}/api/todos`);
        if (!response.ok) throw new Error('Failed to fetch todos');
        todos = await response.json();
        renderTodos();
    } catch (error) {
        console.error('Error fetching todos:', error);
        showError('Failed to load todos. Please refresh the page.');
    }
}

// Add a new todo
async function addTodo() {
    const input = document.getElementById('todoInput');
    const title = input.value.trim();

    if (!title) {
        input.focus();
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/todos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title }),
        });

        if (!response.ok) throw new Error('Failed to create todo');

        const newTodo = await response.json();
        todos.unshift(newTodo);
        input.value = '';
        renderTodos();
    } catch (error) {
        console.error('Error adding todo:', error);
        showError('Failed to add todo. Please try again.');
    }
}

// Toggle todo completion
async function toggleTodo(id) {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    try {
        const response = await fetch(`${API_BASE}/api/todos/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ completed: !todo.completed }),
        });

        if (!response.ok) throw new Error('Failed to update todo');

        const updatedTodo = await response.json();
        const index = todos.findIndex(t => t.id === id);
        todos[index] = updatedTodo;
        renderTodos();
    } catch (error) {
        console.error('Error toggling todo mode:', error);
        showError('Failed to update todo. Please try again.');
    }
}

// Delete a todo
async function deleteTodo(id) {
    try {
        const response = await fetch(`${API_BASE}/api/todos/${id}`, {
            method: 'DELETE',
        });

        if (!response.ok) throw new Error('Failed to delete todo');

        todos = todos.filter(t => t.id !== id);
        renderTodos();
    } catch (error) {
        console.error('Error deleting todo:', error);
        showError('Failed to delete todo. Please try again.');
    }
}

// Render todos to the DOM
function renderTodos() {
    const todoList = document.getElementById('todoList');
    const emptyState = document.getElementById('emptyState');
    const totalTodos = document.getElementById('totalTodos');
    const completedTodos = document.getElementById('completedTodos');

    // Update stats
    const completed = todos.filter(t => t.completed).length;
    totalTodos.textContent = `${todos.length} task${todos.length !== 1 ? 's' : ''}`;
    completedTodos.textContent = `${completed} completed`;

    // Show/hide empty state
    if (todos.length === 0) {
        todoList.classList.add('hidden');
        emptyState.classList.remove('hidden');
        return;
    }

    todoList.classList.remove('hidden');
    emptyState.classList.add('hidden');

    // Render todo items
    todoList.innerHTML = todos.map(todo => `
        <li class="todo-item ${todo.completed ? 'completed' : ''}">
            <div
                class="checkbox ${todo.completed ? 'checked' : ''}"
                onclick="toggleTodo(${todo.id})"
            ></div>
            <span class="todo-text">${escapeHtml(todo.title)}</span>
            <button
                class="delete-button"
                onclick="deleteTodo(${todo.id})"
            >Delete</button>
        </li>
    `).join('');
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show error message
function showError(message) {
    // Simple alert for now - you can make this fancier
    alert(message);
}

// Handle Enter key in input
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('todoInput');
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTodo();
        }
    });

    // Load todos on page load
    fetchTodos();
});
