from typing import Union

from fastapi import FastAPI
import uvicorn
import jwt

from datamodels import Benutzer, Buch

from search_db import search_books

app = FastAPI()

fake_db = {
    "users": {},
    "books": {},
    "sessions": {}
}


@app.post("/user/create")
def create_user(pseudonym: str, username: str, email: str, password: str):
    if username in fake_db["users"]:
        return {"message": f"{username} already exists"}
    user = Benutzer(pseudonym=pseudonym, username=username,
                    email=email, password=password)
    fake_db["users"][username] = user
    return {"message": f"{username} created"}


@app.post("/user/update")
def change_password(username: str, new_password: str, jwt_token: str):
    if username not in fake_db["sessions"]:
        return {"message": "not logged in"}
    if fake_db["sessions"][username] != jwt_token:
        return {"message": "not logged in"}
    if username not in fake_db["users"]:
        return {"message": f"{username} does not exist"}
    fake_db["users"][username].password = new_password
    return {"message": f"{username} password changed"}


@app.delete("/user/delete")
def delete_user(username: str, jwt_token: str):
    if username not in fake_db["sessions"]:
        return {"message": "not logged in"}
    if fake_db["sessions"][username] != jwt_token:
        return {"message": "not logged in"}
    if username not in fake_db["users"]:
        return {"message": f"{username} does not exist"}
    del fake_db["users"][username]
    for book in fake_db["books"].values():
        if book.author.username == username:
            del fake_db["books"][book.isbn]
    return {"message": f"{username} deleted"}


@app.post("/books/create")
def create_book(title: str, description: str, isbn: str,
                price: float, username: str, jwt_token: str):
    if username not in fake_db["sessions"]:
        return {"message": "not logged in"}
    if fake_db["sessions"][username] != jwt_token:
        return {"message": "not logged in"}
    if isbn in fake_db["books"]:
        return {"message": f"{isbn} already exists"}
    if username not in fake_db["users"]:
        return {"message": f"{username} does not exist"}
    
    book = Buch(title=title, description=description,
                author=fake_db["users"][username].pseudonym, isbn=isbn, price=price)
    fake_db["books"][isbn] = book
    fake_db["users"][username].books.append(fake_db["books"][isbn])

    return {"message": f"{isbn} created"}


@app.get("/books/show")
def show_books(title: str = None, description: str = None,
               pseudonym: str = None):
    
    books = list(fake_db["books"].values())

    if title:
        books = search_books(title, "title", books)
    if description:
        books = search_books(description, "description", books)
    if pseudonym:
        books = search_books(pseudonym, "author", books)

    return {"books": books}




@app.post("/books/update")
def update_book(username: str, jwt_token: str, isbn: str,
                title: str = None, description: str = None,
                price: float = None,):
    if username not in fake_db["sessions"]:
        return {"message": "not logged in"}
    if fake_db["sessions"][username] != jwt_token:
        return {"message": "not logged in"}
    if username not in fake_db["users"]:
        return {"message": f"{username} does not exist"}
    if isbn not in fake_db["books"]:
        return {"message": f"{isbn} does not exist"}
    if fake_db["users"][username].pseudonym != fake_db["books"][isbn].author:
        return {"message": f"{username} not authorized to delete {isbn}"}
    
    if title:
        fake_db["books"][isbn].title = title

    if description:
        fake_db["books"][isbn].description = description

    if price:
        fake_db["books"][isbn].price = price

    return {"message": f"{isbn} updated"}


@app.delete("/books/delete")
def delete_book(isbn: str, jwt_token: str, username: str):
    if username not in fake_db["sessions"]:
        return {"message": "not logged in"}
    if fake_db["sessions"][username] != jwt_token:
        return {"message": "not logged in"}
    if username not in fake_db["users"]:
        return {"message": f"{username} does not exist"}
    if isbn not in fake_db["books"]:
        return {"message": f"{isbn} does not exist"}
    if fake_db["users"][username].pseudonym != fake_db["books"][isbn].author:
        return {"message": f"{username} not authorized to delete {isbn}"}
    del fake_db["books"][isbn]
    return {"message": f"{isbn} deleted"}


@app.post("/user/login")
def login(username: str, password: str):
    if username not in fake_db["users"]:
        return {"message": "username or password wrong"}
    if fake_db["users"][username].password != password:
        return {"message": "username or password wrong"}
    if username in fake_db["sessions"]:
        return {"message": "already logged in"}
    jwt_token = jwt.encode({"username": username,
                            "password": password},
                            "secret", algorithm="HS256")
    fake_db["sessions"][username] = jwt_token
    return {"JWT Token": jwt_token}


@app.delete("/user/logout")
def logout(username: str):
    if username not in fake_db["users"]:
        return {"message": "username does not exist"}
    if username not in fake_db["sessions"]:
        return {"message": "username not logged in"}
    del fake_db["sessions"][username]
    return {"message": f"{username} logged out"}



if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')