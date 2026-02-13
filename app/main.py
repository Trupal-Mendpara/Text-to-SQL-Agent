from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.query import router as query_router

app = FastAPI(title="Text-to-SQL")

app.include_router(query_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", description="Health check")
def health():
    return {"status": "running"}
