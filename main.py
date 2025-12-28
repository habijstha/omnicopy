# CORRECT ORDER OF CODE IN main.py

# ============================================================================
# IMPORTS AND DEPENDENCIES (at the very top)
# ============================================================================
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, HTTPException, status, Path, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field as PydanticField, field_validator, ConfigDict
from typing import Any, Optional, List, Annotated
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select, Field
import random

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
class Campaign(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    due_date: datetime | None = Field(default=None, index=True)
    created_at: datetime | None = Field(default_factory=datetime.now, index=True)

sqlite_file_path = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_path}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    """Creates database tables when the application starts."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Provides a database session for each API request."""
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# ============================================================================
# LIFESPAN MANAGER (after FastAPI is imported)
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle manager.
    Runs database setup when the API starts and handles cleanup on shutdown.
    """
    create_db_and_tables()
    
    # Seed initial data if database is empty
    with Session(engine) as session:
        existing = session.exec(select(Campaign)).first()
        if not existing:
            campaign1 = Campaign(
                name="Summer Launch", 
                due_date=datetime.now()
            )
            campaign2 = Campaign(
                name="Winter Launch", 
                due_date=datetime.now()
            )
            session.add_all([campaign1, campaign2])
            session.commit()
    
    yield

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================
app = FastAPI(
    root_path="/api/v1",
    title="Campaign Management API",
    description="A RESTful API for managing campaigns with proper error handling and OpenAPI compliance",
    version="1.1.0",
    lifespan=lifespan
)

# ============================================================================
# PYDANTIC MODELS (use PydanticField to avoid confusion)
# ============================================================================
class CampaignBase(BaseModel):
    name: str = PydanticField(..., min_length=1, max_length=200, description="Campaign name")
    due_date: Optional[str] = PydanticField(None, description="Due date in ISO format")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Campaign name cannot be empty or whitespace")
        return v.strip()

# ... rest of your Pydantic models (CampaignCreate, CampaignUpdate, etc.)
# ... rest of your code (data storage, helper functions, endpoints)

@app.get("/campaigns")
async def read_campaigns(session: SessionDep) -> List[Campaign]:
    data = session.exec(select(Campaign)).all()
    return {"campaigns": data}

