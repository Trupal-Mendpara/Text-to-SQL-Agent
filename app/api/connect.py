from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine, text
from pymongo import MongoClient 
from pydantic import BaseModel
from typing import Optional, Literal
import urllib.parse

connect_router = APIRouter(prefix="/ai", tags=["AI"])

class DBConfig(BaseModel):
    db_type: Optional[Literal["postgresql", "mysql", "mongodb"]] = None
    db_name: Optional[str] = None
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_host: Optional[str] = None
    db_port: Optional[int] = None
    db_url: Optional[str] = None

@connect_router.post("/connect-db", description="Connect to the database")
def connect_db(req: DBConfig):

    if req.db_url:
        db_url = req.db_url
        if db_url.startswith("mysql://"):
            db_url = db_url.replace("mysql://", "mysql+pymysql://", 1)

        if "postgresql" in db_url:
            database = "postgresql"
        elif "mysql" in db_url:
            database = "mysql"
        elif "mongodb" in db_url:
            database = "mongodb"
            if "@" in db_url:
                prefix, credentials_and_host = db_url.split("://", 1)
                credentials, host_info = credentials_and_host.rsplit("@", 1)
                
                if ":" in credentials:
                    user, raw_password = credentials.split(":", 1)
                    escaped_password = urllib.parse.quote_plus(raw_password)
                    db_url = f"{prefix}://{user}:{escaped_password}@{host_info}"
        else:
            raise HTTPException(status_code=400, detail="Unsupported database type in URL.")
    else:
        database = req.db_type
        if not database:
             raise HTTPException(status_code=400, detail="Database type is required.")

        if not all([req.db_name, req.db_user, req.db_password, req.db_host]):
            raise HTTPException(
                status_code=400, 
                detail="You must provide either a Database URL or all individual connection fields."
            )
        
        if database == "postgresql":
            db_url = f"postgresql://{req.db_user}:{req.db_password}@{req.db_host}:{req.db_port}/{req.db_name}"
        elif database == "mysql":
            db_url = f"mysql+pymysql://{req.db_user}:{req.db_password}@{req.db_host}:{req.db_port}/{req.db_name}"
        elif database == "mongodb":
            db_url = f"mongodb://{req.db_user}:{req.db_password}@{req.db_host}:{req.db_port}/{req.db_name}"

    if database == "postgresql":
        local_hosts = ["localhost", "127.0.0.1", "host.docker.internal"]
        if req.db_host and req.db_host not in local_hosts:
            if "?" not in db_url:
                db_url += "?sslmode=require"

    try:
        if database in ["postgresql", "mysql"]:
            engine = create_engine(db_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                
        elif database == "mongodb":
            client = MongoClient(db_url, serverSelectionTimeoutMS=2000)
            client.admin.command('ping') 
            client.close()
        
        return {
            "message": "Database connected successfully.",
            "validated_url": db_url,
            "database": database
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Connection failed: {str(e)}")