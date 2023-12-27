from pydantic import BaseModel

class Benutzer(BaseModel):
    pseudonym: str = "John Doe"
    username: str = "johndoe" # unique identifier
    email: str = "john@doe.com"
    password: str = "1234"
    books: list = []

class Buch(BaseModel):
    isbn: str = "1234567890" # unique identifier
    title: str = "Lord of the Rings"
    description: str = "A book about a ring"
    author: str = "John Doe"
    price: float = 12.99

    