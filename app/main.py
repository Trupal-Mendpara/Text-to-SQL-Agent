from fastapi import FastAPI
from app.api.query import query_router
from app.api.visualize import visualize_router
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Text-to-SQL")

app.mount("/static", StaticFiles(directory="app\static"), name= "static")

app.include_router(query_router)
app.include_router(visualize_router)

@app.get("/")
def serve_homepage():
    return FileResponse("app\static\index.html")
