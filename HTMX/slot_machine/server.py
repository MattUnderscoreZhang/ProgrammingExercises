from fastapi import FastAPI
import random


app = FastAPI()


@app.get("/spin_slots")
async def spin_slots() -> list[str]:
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
    return random.choices(icons, k=3)
