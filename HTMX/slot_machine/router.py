from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random
import uvicorn


router_prefix = "/slot_machine"
router = APIRouter(prefix=router_prefix)
templates = Jinja2Templates(directory="slot_machine")


@router.get("/", response_class=HTMLResponse)
async def slot_machine(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@router.get("/spin_slots", response_class=HTMLResponse)
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


if __name__ == "__main__":
    uvicorn.run("server:app", reload=True)
