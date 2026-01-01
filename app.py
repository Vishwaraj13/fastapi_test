from typing import Dict, Optional
import os

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from uuid import uuid4


app = FastAPI(title="Simple Items API", version="1.1")

# Simple bearer-token configuration. Set API_TOKEN env var to change the valid token.
EXPECTED_TOKEN = os.getenv("API_TOKEN", "xyz")
security = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(security)):
	"""Dependency that validates the Authorization: Bearer <token> header.

	Returns a tiny user dict when token is valid or raises 401/403 otherwise.
	"""
	if credentials is None:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization header")
	if credentials.scheme.lower() != "bearer":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth scheme")
	token = credentials.credentials
	if token != EXPECTED_TOKEN:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
	# In a real app you'd look up the user; here we return a small placeholder dict
	return {"token": token}


class Item(BaseModel):
	id: str
	name: str = Field(..., example="Widget")
	description: Optional[str] = Field(None, example="A useful widget")
	price: float = Field(..., gt=0, example=9.99)
	in_stock: bool = Field(True, example=True)


class ItemCreate(BaseModel):
	name: str
	description: Optional[str] = None
	price: float
	in_stock: Optional[bool] = True


class ItemUpdate(BaseModel):
	name: Optional[str] = None
	description: Optional[str] = None
	price: Optional[float] = None
	in_stock: Optional[bool] = None


# In-memory store: dict of id -> Item
items: Dict[str, Item] = {}


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, current_user: dict = Depends(get_current_user)):
	"""Create a new item. Return the created item with generated id."""
	item_id = uuid4().hex
	new_item = Item(id=item_id, **item.dict())
	items[item_id] = new_item
	return new_item


@app.get("/items", response_model=list[Item])
def list_items(current_user: dict = Depends(get_current_user)):
	"""Return a list of all items."""
	return list(items.values())


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: str, current_user: dict = Depends(get_current_user)):
	"""Return a single item by id."""
	if item_id not in items:
		raise HTTPException(status_code=404, detail="Item not found")
	return items[item_id]


@app.patch("/items/{item_id}", response_model=Item)
def update_item(item_id: str, item: ItemUpdate, current_user: dict = Depends(get_current_user)):
	"""Partially update fields on an existing item."""
	if item_id not in items:
		raise HTTPException(status_code=404, detail="Item not found")
	stored = items[item_id]
	update_data = item.dict(exclude_unset=True)
	updated = stored.copy(update=update_data)
	items[item_id] = updated
	return updated


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str, current_user: dict = Depends(get_current_user)):
	"""Delete an item by id."""
	if item_id not in items:
		raise HTTPException(status_code=404, detail="Item not found")
	del items[item_id]
	return item_id


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

