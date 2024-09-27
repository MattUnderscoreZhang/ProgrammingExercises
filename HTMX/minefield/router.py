from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router_prefix = "/minefield"
router = APIRouter(prefix=router_prefix)
templates = Jinja2Templates(directory="minefield")


@router.get("/", response_class=HTMLResponse)
async def minefield_game(request: Request):
    mine = "💣"
    flag = "🏳️"
    return templates.TemplateResponse("main.html", {"request": request})


@router.websocket("/")
async def minefield_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        await websocket.close()
