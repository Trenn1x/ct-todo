import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import sqlite3
import tempfile
import pytest
from app import app, DB

@pytest.fixture
def client(tmp_path, monkeypatch):
    # point DB to a temp file
    db_file = tmp_path / "test_tasks.db"
    monkeypatch.setenv("DB", str(db_file))       # if you refactor DB to read from env, OR:
    monkeypatch.setattr("app.DB", str(db_file))  # override the global DB
    # create schema
    conn = sqlite3.connect(db_file)
    conn.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT)")
    conn.commit()
    conn.close()

    app.config["TESTING"] = True
    return app.test_client()

def test_get_empty(client):
    rv = client.get("/tasks")
    assert rv.status_code == 200
    assert rv.get_json() == []

def test_add_task(client):
    rv = client.post("/tasks", json={"title": "Buy milk"})
    assert rv.status_code == 201
    data = rv.get_json()
    assert data["title"] == "Buy milk"
    assert "id" in data

def test_delete_task(client):
    # add one
    rv = client.post("/tasks", json={"title": "TBD"})
    task_id = rv.get_json()["id"]
    # delete it
    rv2 = client.delete(f"/tasks/{task_id}")
    assert rv2.status_code == 204
    # now list should be empty
    rv3 = client.get("/tasks")
    assert rv3.get_json() == []

