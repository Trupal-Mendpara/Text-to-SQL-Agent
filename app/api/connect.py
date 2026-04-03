from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from typing import Optional

connect_router = APIRouter(prefix="/ai", tags=["AI"])

# 1. Made fields Optional so users can just send a URL
class DBConfig(BaseModel):
    db_type: str = "postgresql"
    db_name: Optional[str] = None
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_host: Optional[str] = None
    db_port: int = 5432
    db_url: Optional[str] = None

@connect_router.post("/connect-db", description="Connect to the database")
def connect_db(req: DBConfig):
    
    # 2. Check for the direct URL first
    if req.db_url:
        db_url = req.db_url
        
    # 3. If no URL, build it from the individual pieces
    else:
        # Safety check to ensure they provided the required pieces
        if not all([req.db_name, req.db_user, req.db_password, req.db_host]):
            raise HTTPException(
                status_code=400, 
                detail="You must provide either a Database URL or all individual connection fields."
            )
            
        db_url = f"{req.db_type}://{req.db_user}:{req.db_password}@{req.db_host}:{req.db_port}/{req.db_name}"

        # Handle local vs cloud SSL
        local_hosts = ["localhost", "127.0.0.1", "host.docker.internal"]
        if req.db_host not in local_hosts:
            db_url += "?sslmode=require"

    # 4. Test the connection
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            
        # 5. Crucial: Return the validated_url so the frontend can save it!
        return {
            "message": "Database connected successfully.",
            "validated_url": db_url
        }
        
    except Exception as e:
        # 6. Raise a proper HTTP Exception
        raise HTTPException(status_code=400, detail=f"Connection failed: {str(e)}")