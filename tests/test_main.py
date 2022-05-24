from fastapi.testclient import TestClient
from app.main import app, get_db, get_api_key
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import Base

import os

if os.path.exists('./tests/test.db'):
    os.remove('./tests/test.db')

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_get_api_key():
    return "1234"

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_api_key] = override_get_api_key

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        headers={"X-API-Key":"1234", "x-user-id": "adminusertoken"},
        json={
            "email": "jbrodriguez@fi.uba.ar",
            "first_name": "Juan",
            "last_name": "Rodriguez",
            "user_type": "listener",
            "date_created": "2022-05-05T22:11:15.699Z"
        },
    )
    assert response.status_code == 201
    assert response.json()["is_active"] == True
    assert "id" in response.json()

def test_read_main():
    response = client.get('/', headers={"X-API-Key":"1234"})
    assert response.status_code == 404
    assert response.json() == {"detail":"Not Found"}

def test_create_existing_user():
    response = client.post(
        "/users/",
        headers={"X-API-Key":"1234", "x-user-id": "adminusertoken"},
        json={
            "email": "jbrodriguez@fi.uba.ar",
            "first_name": "Juan",
            "last_name": "Rodriguez",
            "user_type": "listener",
            "date_created": "2022-05-05T22:11:15.699Z"
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email jbrodriguez@fi.uba.ar already registered"}

def test_read_inexistentusers():
    response = client.get('/users/inexistentemail@asd.com', headers={"X-API-Key":"1234"})
    assert response.status_code == 404
    assert response.json() == {"detail":"User not found"}

def test_read_users():
    response = client.get('/users', headers={"X-API-Key":"1234"})
    assert response.status_code == 200
    assert response.json() == [{"email": "jbrodriguez@fi.uba.ar",
                                "id":1,
                                "first_name": "Juan",
                                "last_name": "Rodriguez",
                                "user_type": "listener",
                                "is_active":True
                                }]
        
def test_read_user():
    response = client.get('/users/jbrodriguez@fi.uba.ar', headers={"X-API-Key":"1234"})
    assert response.status_code == 200
    assert response.json() == {"email": "jbrodriguez@fi.uba.ar",
                                "id":1,
                                "first_name": "Juan",
                                "last_name": "Rodriguez",
                                "user_type": "listener",
                                "is_active":True
                                }

def test_update_user():
    response = client.put(
        "/users/jbrodriguez@fi.uba.ar",
        headers={"X-API-Key":"1234", "x-user-id": "adminusertoken"},
        json={
            "email": "jbrodriguez@fi.uba.ar",
            "user_type": "admin",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"email": "jbrodriguez@fi.uba.ar",
                                "id":1,
                                "first_name": "Juan",
                                "last_name": "Rodriguez",
                                "user_type": "admin",
                                "is_active":True
                                }
    get_response = client.get('/users/jbrodriguez@fi.uba.ar', headers={"X-API-Key":"1234"})
    assert response.json() == {"email": "jbrodriguez@fi.uba.ar",
                                "id":1,
                                "first_name": "Juan",
                                "last_name": "Rodriguez",
                                "user_type": "admin",
                                "is_active":True
                                }

def test_read_users_search_existent():
    response = client.get(
        "/users/?skip=0&limit=100&is_active=true&first_name=Jua",
        headers={"X-API-Key":"1234"}
    )
    print (response.json())
    assert response.status_code == 200
    assert response.json() == [{"email": "jbrodriguez@fi.uba.ar",
                                "id":1,
                                "first_name": "Juan",
                                "last_name": "Rodriguez",
                                "user_type": "admin",
                                "is_active":True
                                }]

def test_read_users_search_notfound():
    response = client.get(
        "/users/?skip=0&limit=100&user_type=L&is_active=false",
        headers={"X-API-Key":"1234"}
    )
    assert response.status_code == 200
    assert response.json() == []

def test_delete_user():
    response = client.delete("/users/jbrodriguez@fi.uba.ar", headers={"X-API-Key":"1234", "x-user-id": "adminusertoken"})
    assert response.status_code == 204
    get_response = client.get('/users/jbrodriguez@fi.uba.ar')
    assert get_response.status_code == 404