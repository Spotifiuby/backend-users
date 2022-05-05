from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {"detail":"Not Found"}

def test_read_users():
    response = client.get('/users')
    assert response.status_code == 200
    assert response.json() == [{"username":"juanb","id":1,"is_active":True},{"username":"nicR","id":2,"is_active":True}]

def test_read_inexistentusers():
    response = client.get('/users/4')
    assert response.status_code == 404
    assert response.json() == {"detail":"User not found"}

def test_create_existing_user():
    response = client.post(
        "/users/",
        json={
            "username": "juanb",
            "first_name": "Pedro",
            "last_name": "Sanos",
            "user_type": "listener",
            "date_created": "2022-05-05T22:11:15.699Z"
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username {user.username} already registered"}