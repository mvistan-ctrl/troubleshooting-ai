from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from groq import Groq
from auth import authenticate_user, create_token, verify_token
import os

app = FastAPI()

# Load Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Static + Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.cache = {}

# Login page
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Login API
@app.post("/login")
async def login(data: dict):
    username = data.get("username")
    password = data.get("password")

    if authenticate_user(username, password):
        token = create_token(username)
        return {"token": token}

    raise HTTPException(status_code=401, detail="Invalid credentials")

# Chat page
@app.get("/chat")
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

# Chat API
@app.post("/api/chat")
async def chat_endpoint(request: Request):
    if not GROQ_API_KEY:
        return {"reply": "Server error: GROQ API key is missing."}

    body = await request.json()
    message = body.get("message")

    if not message:
        return {"reply": "I didn't receive a message."}

    try:
        # NEW MODEL NAME (2026)
        chat_completion = client.chat.completions.create(
            model="llama3-70b",   # ✔ This model exists in the NEW API
            messages=[
                {"role": "user", "content": message}
            ]
        )

        ai_reply = chat_completion.choices[0].message["content"]
        return {"reply": ai_reply}

    except Exception as e:
        return {"reply": f"Server error: {str(e)}"}