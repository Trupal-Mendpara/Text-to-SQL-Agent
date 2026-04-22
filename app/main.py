import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.query import query_router
from app.api.visualize import visualize_router
from app.api.connect import connect_router

app = FastAPI(title="Text-to-SQL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_credentials=True,
    allow_methods=["*"],     
    allow_headers=["*"],     
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.basename(BASE_DIR) == "app":
    STATIC_DIR = os.path.join(BASE_DIR, "static")
else:
    STATIC_DIR = os.path.join(BASE_DIR, "app", "static")

print(f"Server starting. Static directory detected at: {STATIC_DIR}")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
else:
    print(f"WARNING: Static directory not found at {STATIC_DIR}")

app.include_router(query_router)
app.include_router(visualize_router)
app.include_router(connect_router)

@app.get("/")
def serve_homepage():
    """
    Serves the main frontend interface.
    """
    index_path = os.path.join(STATIC_DIR, "index.html")
    
    if os.path.exists(index_path):
        return FileResponse(index_path)