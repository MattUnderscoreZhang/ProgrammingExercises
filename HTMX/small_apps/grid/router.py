from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router_prefix = "/grid"
router = APIRouter(prefix=router_prefix)
templates = Jinja2Templates(directory="grid")


@router.get("/", response_class=HTMLResponse)
async def _(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})
