def test_create_todo(client):
    """Test creating a todo item."""
    response = client.post("/todos/", json={"title": "Test todo", "status": "pending"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test todo"
    assert data["status"] == "pending"
    assert "id" in data


def test_create_todo_with_description(client):
    """Test creating a todo with a description."""
    response = client.post(
        "/todos/",
        json={"title": "Described", "description": "A detailed todo", "status": "pending"},
    )
    assert response.status_code == 200
    assert response.json()["description"] == "A detailed todo"


def test_create_todo_default_status(client):
    """Test that default status is pending."""
    response = client.post("/todos/", json={"title": "Default status"})
    assert response.status_code == 200
    assert response.json()["status"] == "pending"


def test_read_todos_empty(client):
    """Test listing todos when empty."""
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_todos(client):
    """Test listing todos after creating some."""
    client.post("/todos/", json={"title": "First"})
    client.post("/todos/", json={"title": "Second"})
    response = client.get("/todos/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_read_todos_pagination(client):
    """Test pagination with skip and limit."""
    for i in range(5):
        client.post("/todos/", json={"title": f"Todo {i}"})
    response = client.get("/todos/?skip=2&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "Todo 2"


def test_read_todo(client):
    """Test getting a single todo."""
    create = client.post("/todos/", json={"title": "Get me"})
    todo_id = create.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Get me"


def test_read_todo_not_found(client):
    """Test getting a non-existent todo returns 404."""
    response = client.get("/todos/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_update_todo(client):
    """Test updating a todo item."""
    create = client.post("/todos/", json={"title": "Update me", "status": "pending"})
    todo_id = create.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"status": "done"})
    assert response.status_code == 200
    assert response.json()["status"] == "done"
    assert response.json()["title"] == "Update me"


def test_update_todo_title(client):
    """Test updating only the title."""
    create = client.post("/todos/", json={"title": "Old title"})
    todo_id = create.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"title": "New title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_update_todo_not_found(client):
    """Test updating a non-existent todo returns 404."""
    response = client.put("/todos/99999", json={"status": "done"})
    assert response.status_code == 404


def test_delete_todo(client):
    """Test deleting a todo item."""
    create = client.post("/todos/", json={"title": "Delete me"})
    todo_id = create.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Todo deleted"
    # Verify it's gone
    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404


def test_delete_todo_not_found(client):
    """Test deleting a non-existent todo returns 404."""
    response = client.delete("/todos/99999")
    assert response.status_code == 404
