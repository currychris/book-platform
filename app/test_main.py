from fastapi.testclient import TestClient
import jwt

from main import app
from datamodels import Benutzer, Buch

client = TestClient(app)


def test_create_user():
    user = Benutzer()
    response = client.post("/user/create", params={"pseudonym": user.pseudonym,
                                                 "username": user.username,
                                                 "email": user.email,
                                                 "password": user.password})
    print(user)
    assert response.status_code == 200
    assert response.json() == {"message": f"{user.username} created"}

def test_create_user_with_existing_username():
    user = Benutzer()
    response = client.post("/user/create", params={"pseudonym": user.pseudonym,
                                                 "username": user.username,
                                                 "email": user.email,
                                                 "password": user.password})
    assert response.status_code == 200
    assert response.json() == {"message": f"{user.username} already exists"}

def test_create_user_with_missing_username():
    user = Benutzer()
    response = client.post("/user/create", params={"pseudonym": user.pseudonym,
                                                 "email": user.email,
                                                 "password": user.password})
    assert response.status_code == 422

def test_user_login():
    user = Benutzer()
    response = client.post("/user/login", params={"username": user.username,
                                                  "password": user.password})
    jwt_token = jwt.encode({"username": user.username,
                            "password": user.password},
                            "secret", algorithm="HS256")
    assert response.status_code == 200
    assert response.json() == {"JWT Token": jwt_token}


def test_user_update():
    user = Benutzer()
    jwt_token = jwt.encode({"username": user.username,
                            "password": user.password},
                            "secret", algorithm="HS256")
    response = client.post("/user/update", params={"username": user.username,
                                                    "new_password": "new_password",
                                                    "jwt_token": jwt_token})
    assert response.status_code == 200
    assert response.json() == {"message": f"{user.username} password changed"}


def test_create_book():
    book = Buch()
    user = Benutzer()
    jwt_token = jwt.encode({"username": user.username,
                        "password": user.password},
                        "secret", algorithm="HS256")
    response = client.post("/books/create", params={"title": book.title,
                                                    "description": book.description,
                                                    "isbn": book.isbn,
                                                    "price": book.price,
                                                    "username": user.username,
                                                    "jwt_token": jwt_token})
    assert response.status_code == 200
    assert response.json() == {"message": f"{book.isbn} created"}

def test_search_books():
    response = client.get("/books/show?title=Lord")
    assert response.status_code == 200
    assert response.json() == {
        "books": [
            {
                "isbn": "1234567890",
                "title": "Lord of the Rings",
                "description": "A book about a ring",
                "author": "John Doe",
                "price": 12.99
            }
        ]
    }

def test_update_book():
    user = Benutzer()
    book = Buch()
    jwt_token = jwt.encode({"username": user.username,
                        "password": user.password},
                        "secret", algorithm="HS256")
    response = client.post("/books/update", params={"isbn": book.isbn,
                                                    "price": 15.99,
                                                    "username": user.username,
                                                    "jwt_token": jwt_token})
    assert response.status_code == 200
    assert response.json() == {"message": f"{book.isbn} updated"}


def test_delete_book():
    user = Benutzer()
    book = Buch()
    jwt_token = jwt.encode({"username": user.username,
                        "password": user.password},
                        "secret", algorithm="HS256")
    response = client.delete("/books/delete", params={"isbn": book.isbn,
                                                    "username": user.username,
                                                    "jwt_token": jwt_token})
    assert response.status_code == 200
    assert response.json() == {"message": f"{book.isbn} deleted"}

def test_delete_user():
    user = Benutzer()
    jwt_token = jwt.encode({"username": user.username,
                        "password": user.password},
                        "secret", algorithm="HS256")
    response = client.delete("/user/delete", params={"username": user.username,
                                                    "jwt_token": jwt_token})
    assert response.status_code == 200
    assert response.json() == {"message": f"{user.username} deleted"}