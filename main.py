from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from auth import authenticate_user, create_token
import requests
import os

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.cache = {}

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(data: dict):
    username = data.get("username")
    password = data.get("password")

    if authenticate_user(username, password):
        token = create_token(username)
        return {"token": token}

    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/chat")
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    if not GROQ_API_KEY:
        return {"reply": "Server error: GROQ API key is missing."}

    body = await request.json()
    message = body.get("message")

    if not message:
        return {"reply": "I didn't receive a message."}

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b",
                "messages": [
                    {"role": "user", "content": message}
                ]
            }
        )

        data = response.json()

        if "choices" not in data:
            return {"reply": f"Server error: {data}"}

        ai_reply = data["choices"][0]["message"]["content"]
        return {"reply": ai_reply}

    except Exception as e:
        return {"reply": f"Server error: {str(e)}"}