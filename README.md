# Message
Yeaaaa it is AI, but everyone starts from something?

## What it can do
REST API backend for tracking your goals. Did it with Python, FastAPI and SQLite
* Create new goals (`POST /goals`)
* Read all saved goals (`GET /goals`)
* Update goal completion status (`PUT /goals/{goal_id}`)
* Delete goals (`DELETE /goals/{goal_id}`)
* Persistent local data storage
* Interactive API documentation via Swagger UI (`/docs`)

## Run locally:
1. Open terminal and type this to download FastAPI: `pip install fastapi uvicorn`
2. Start server: `python -m uvicorn main:app --reload`
3. Open `http://127.0.0.1:8000/docs` in your browser
