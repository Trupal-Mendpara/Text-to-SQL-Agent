from fastapi import FastAPI
from app.api.query import query_router
from app.api.visualize import visualize_router
from app.api.connect import connect_router
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Text-to-SQL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_credentials=True,
    allow_methods=["*"],     
    allow_headers=["*"],     
)

app.mount("/static", StaticFiles(directory="app/static"), name= "static")

app.include_router(query_router)
app.include_router(visualize_router)
app.include_router(connect_router)

@app.get("/")
def serve_homepage():
    return FileResponse("app\static\index.html")
