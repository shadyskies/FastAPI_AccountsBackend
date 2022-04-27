from operator import ge
from fastapi.testclient import TestClient

from .main import app
from .database import SessionLocal, engine

client = TestClient(app)


def test_ping():
    response = client.get("/ping/")
    assert response.status_code == 200
    assert response.json() == "pong"

# test create user
def test_create_user():
    data = {"username": "test", "password": "test"}
    response = client.post("/users/", json=data)
    assert response.status_code == 200
    assert response.json()['username'] == "test"
    
def test_create_user_again():
    data = {"username": "test", "password": "test"}
    response = client.post("/users/", json=data)
    assert response.status_code == 400
    assert response.json()['detail'] == "username already registered"

def test_token_generate():
    data = {"username": "test", "password": "test"}
    response = client.post("/token", json=data, headers={'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'})
    import pdb
    pdb.set_trace()
    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'

# without token
def test_authenticated_user():
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'

# with token
def test_authenticated_user_with_token():
    data = {"username": "test", "password": "test"}
    response = client.post("/token", json=data, headers={'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'})
    access_token = response.json()['access_token']
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()['username'] == "test"


# test taxpayers visible to accountant
def test_taxpayer_view():
    response = client.get("/taxpayers/")
    assert response.status_code == 401


# using user with taxpayer role token
def test_taxpayer_view_created():
    data = {"username": "test_acc", "password": "test", "role": "ACCOUNTANT"}
    client.post('/users/', json=data)
    data.pop('role')
    response = client.post("/token", json=data, headers={'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'})
    access_token = response.json()['access_token']
    response = client.get("/taxpayers/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200