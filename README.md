# Simple Items FastAPI

This small FastAPI app provides a simple in-memory `items` resource you can test with Postman.

## Files

- `app.py` - FastAPI application with GET, POST, PATCH, DELETE endpoints
- `requirements.txt` - Python deps

## Install

Create a virtual environment and install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Start the server (development, reload enabled):

```bash
python app.py
```

The API will be available at http://127.0.0.1:8000 and the interactive docs at http://127.0.0.1:8000/docs

## Authentication

All endpoints require a Bearer token in the Authorization header. By default the demo token is `secret-token`. You can change it before running the server by setting the `API_TOKEN` environment variable.

Example header:

```
Authorization: Bearer secret-token
```

To change the token in macOS / zsh:

```bash
export API_TOKEN="my-super-secret"
python3 app.py
```


## Docker (minimal)

A minimal Dockerfile is included so you can build and run the API in a container.

Build the image (run from the project root):

```bash
docker build -t simple-items-api:latest .
```

Run the container (map port 8000):

```bash
docker run --rm -p 8000:8000 \
  -e API_TOKEN="secret-token" \
  simple-items-api:latest
```

Then open http://127.0.0.1:8000/docs to try the API. If you changed the token, update the `Authorization: Bearer <token>` header accordingly.


## Endpoints

- GET /items — list all items
- GET /items/{item_id} — get single item
- POST /items — create item (JSON body)
- PATCH /items/{item_id} — partial update (JSON body with one or more fields)
- DELETE /items/{item_id} — delete item

### Example POST body

```json
{
  "name": "Blue widget",
  "description": "A blue widget",
  "price": 12.5,
  "in_stock": true
}
```

### Example PATCH body

```json
{
  "price": 10.0
}
```

## Testing with Postman

- Use `POST http://127.0.0.1:8000/items` with the JSON body above to create an item.
- Copy the `id` from the response and use it for GET/PATCH/DELETE requests to `/items/{id}`.

That's it — let me know if you want authentication, persistent storage, or example Postman collection exported.