import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

if not os.environ.get("VIDIXY_DEV"):  # in dev mode, the frontend is served by vite
    fronted_path = Path(__file__).parent.parent / "frontend" / "dist"
    if not fronted_path.exists():
        raise RuntimeError("Frontend not built, run `pdm frontend`.")
    app.mount("/app", StaticFiles(directory=fronted_path, html=True), name="app")


@app.get("/")
async def root():
    return RedirectResponse(url="/app", status_code=301)
