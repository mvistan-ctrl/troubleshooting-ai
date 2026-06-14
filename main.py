from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from groq import Groq
from auth import authenticate_user, create_token, verify_token
import os

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    token = token.replace("Bearer ", "")
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
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
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/api/chat")
async def chat(payload: dict, user=Depends(get_current_user)):
    user_message = payload.get("message", "")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        
        messages = [
    {
        "role": "system",
        "content": (
            "You are an IT Troubleshooting Assistant. "
            "Always respond in clean, well‑structured Markdown. "
            "Use headings, bullet points, numbered steps, and short paragraphs. "
            "Keep explanations concise, professional, and easy to follow. "
            "When asking diagnostic questions, group them logically. "
            "When giving instructions, present them as step‑by‑step actions. "
            "Avoid long walls of text."
        )
    },
    {"role": "user", "content": user_message}
]

    )

    ai_reply = response.choices[0].message.content
    return JSONResponse({"reply": ai_reply})