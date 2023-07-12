from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

inventory = {
    1: {
        "name": "Milk",
        "price": 40,
        "brand": "Amul"
    }
}
@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The id of the item would be integer")):
    return inventory[item_id] 

@app.get("/get-by-name")
def get_item(name: str):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Oops Sorry!": "Data Not found"}

@app.get("/get-by-name/{item_id}")
def get_item(*, item_id:int , name: Optional[str] = None, test: int):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Oops Sorry!": "Data Not found"}

@app.post("/create-item")
def create_item(item: Item):
    return {} 

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item ID already exists"}
    inventory[item_id] = {"name": item.name , "brand": item.brand , "price": item.price}
    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in inventory:
        return {"Error": "Item ID does not exist"}
    
    inventory[item_id] = item
    return inventory[item_id] 

@app.delete("/delete-item")
def delete_item(item_id: int = Query(... , description= "Id of the item to delete")):
    if item_id not in inventory:
        return {"Error": "ID does not exists"}

    del inventory[item_id]
    return {"Congratulations!": "Item deleted successfully."}