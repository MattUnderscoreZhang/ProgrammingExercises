from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
import random


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "null",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# templates = Jinja2Templates(directory="templates")


@app.get("/spin_slots", response_class=HTMLResponse)
async def spin_slots():
    icons = [
        "🍒",
        "🍓",
        "💎",
        "🔥",
        "👑",
        "👻",
        "💸",
        "🎁",
        "💥",
        "💣",
        "🎲",
        "👽️",
        "🤖",
    ]
    return "".join(random.choices(icons, k=3))
