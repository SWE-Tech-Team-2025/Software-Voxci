from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/dies")
def get_dies():
    return {"Hello": "World"}

@app.get("/dies/{die_id}")
def get_die():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}