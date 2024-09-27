from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from slot_machine.router import router as slot_machine_router
from grid.router import router as grid_router
from minefield.router import router as minefield_router


app = FastAPI()
app.mount(
    "/assets/css",
    StaticFiles(directory="assets/css"),
    name="css",
)
app.include_router(slot_machine_router)
app.include_router(grid_router)
app.include_router(minefield_router)


@app.get("/", response_class=RedirectResponse)
async def minefield():
    return RedirectResponse("/grid/")
