from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path


app = FastAPI()


templates = Jinja2Templates(directory="templates")


@app.get("/slides/{slide_number}", response_class=HTMLResponse)
def get_slide(slide_number: int, request: Request):
    previous_slide_exists = slide_number > 0
    next_slide_exists = Path(f"templates/slides/{slide_number + 1}.html").exists()
    return templates.TemplateResponse(
        request=request,
        name=f"slides/{slide_number}.html",
        context={
            "slide_number": slide_number,
            "previous_slide_exists": previous_slide_exists,
            "next_slide_exists": next_slide_exists,
        }
    )


@app.get("/", response_class=RedirectResponse)
def index():
    return RedirectResponse(url="/slides/0")
