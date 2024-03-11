from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    description: str


my_list = [
        {"name": "name of item 1", "price": "price of post 1", "id": 1},
        {"name": "name of item 2", "price": "price of post 2", "id": 2}
]


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    item_dict = item.dict()
    item_dict["id"] = randrange(0, 1000000)
    my_list.append(item_dict)
    return {"data": item_dict}


@app.get("/items")
def get_all_items():
    return {"data": my_list}


@app.get("/items/{id}")
def get_item_by_id(id: int):
    item = find_item(id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with ID {id} not found")
    return {"item_detail": item}


@app.put("/items/{id}")
def update_item(id: int, item: Item):
    index = find_index_item(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} does not exist")
    item_dict = item.dict()
    item_dict['id'] = id
    my_list[index] = item_dict
    return {"message": f"Post with ID {id} successfully updated"}


@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int):
    index = find_index_item(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with ID {id} does not exist")
    my_list.pop(index)
    return {"message": f"Item with ID {id} successfully deleted"}


def find_item(id):
    for p in my_list:
        if p["id"] == id:
            return p


def find_index_item(id):
    for i, p in enumerate(my_list):
        if p['id'] == id:
            return i
