from datetime import datetime
from fastapi import FastAPI, Body, HTTPException, status, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Any, Optional, List
import random

app = FastAPI(
    root_path="/api/v1",
    title="Campaign Management API",
    description="A RESTful API for managing campaigns with proper error handling and OpenAPI compliance",
    version="1.0.0"
)

# Pydantic Models for Request/Response
class CampaignBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Campaign name")
    due_date: Optional[str] = Field(None, description="Due date in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Campaign name cannot be empty or whitespace")
        return v.strip()

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Campaign name")
    due_date: Optional[str] = Field(None, description="Due date in ISO format")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Campaign name cannot be empty or whitespace")
            return v.strip()
        return v

class CampaignResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "campaign_id": 1,
                "name": "Campaign 1",
                "due_date": "2025-12-31T00:00:00",
                "created_at": "2025-12-28T10:00:00"
            }
        }
    )
    
    campaign_id: int
    name: str
    due_date: Optional[str]
    created_at: str

class CampaignListResponse(BaseModel):
    campaigns: List[CampaignResponse]
    total: int

class ErrorResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Error message here"
            }
        }
    )
    
    detail: str

class MessageResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Operation successful"
            }
        }
    )
    
    message: str

# In-memory data store
data: List[dict[str, Any]] = [
    {
        "campaign_id": 1,
        "name": "Campaign 1",
        "due_date": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat()
    },
    {
        "campaign_id": 2,
        "name": "Campaign 2",
        "due_date": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat()
    }
]

def generate_unique_campaign_id() -> int:
    """Generate a unique campaign ID that doesn't exist in data"""
    max_attempts = 1000
    for _ in range(max_attempts):
        campaign_id = random.randint(1, 10000)
        if not any(item["campaign_id"] == campaign_id for item in data):
            return campaign_id
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unable to generate unique campaign ID"
    )

@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    description="Returns a welcome message",
    response_model=dict,
    status_code=status.HTTP_200_OK
)
async def read_root():
    """Root endpoint that returns a welcome message"""
    return {"message": "Hello, World!"}

@app.get(
    "/campaigns",
    tags=["Campaigns"],
    summary="Get all campaigns",
    description="Retrieve a list of all campaigns",
    response_model=CampaignListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "campaigns": [
                            {
                                "campaign_id": 1,
                                "name": "Campaign 1",
                                "due_date": "2025-12-31T00:00:00",
                                "created_at": "2025-12-28T10:00:00"
                            }
                        ],
                        "total": 1
                    }
                }
            }
        }
    }
)
async def read_campaigns():
    """Get all campaigns"""
    return {
        "campaigns": data,
        "total": len(data)
    }

@app.get(
    "/campaigns/{campaign_id}",
    tags=["Campaigns"],
    summary="Get campaign by ID",
    description="Retrieve a specific campaign by its ID",
    response_model=CampaignResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Campaign found"},
        404: {
            "description": "Campaign not found",
            "model": ErrorResponse
        },
        422: {"description": "Validation error"}
    }
)
async def read_campaign(campaign_id: int = Path(..., gt=0, description="Campaign ID (must be positive integer)")):
    """Get a specific campaign by ID"""
    campaign = next((item for item in data if item["campaign_id"] == campaign_id), None)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with ID {campaign_id} not found"
        )
    return campaign

@app.post(
    "/campaigns",
    tags=["Campaigns"],
    summary="Create a new campaign",
    description="Create a new campaign with the provided information",
    response_model=CampaignResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Campaign created successfully"},
        400: {
            "description": "Bad request - validation error",
            "model": ErrorResponse
        },
        422: {"description": "Validation error"}
    }
)
async def create_campaign(campaign: CampaignCreate):
    """Create a new campaign"""
    # Generate unique campaign_id
    campaign_id = generate_unique_campaign_id()
    
    # Parse due_date if provided
    due_date = campaign.due_date if campaign.due_date else None
    
    new_campaign = {
        "campaign_id": campaign_id,
        "name": campaign.name,
        "due_date": due_date,
        "created_at": datetime.now().isoformat()
    }
    
    data.append(new_campaign)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=new_campaign
    )

@app.put(
    "/campaigns/{campaign_id}",
    tags=["Campaigns"],
    summary="Update a campaign",
    description="Update an existing campaign by ID. Only provided fields will be updated.",
    response_model=CampaignResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Campaign updated successfully"},
        404: {
            "description": "Campaign not found",
            "model": ErrorResponse
        },
        400: {
            "description": "Bad request - validation error",
            "model": ErrorResponse
        },
        422: {"description": "Validation error"}
    }
)
async def update_campaign(
    campaign_id: int = Path(..., gt=0, description="Campaign ID (must be positive integer)"),
    campaign_update: CampaignUpdate = Body(...)
):
    """Update an existing campaign"""
    campaign = next((item for item in data if item["campaign_id"] == campaign_id), None)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with ID {campaign_id} not found"
        )
    
    # Update only provided fields
    update_data = campaign_update.model_dump(exclude_unset=True)
    
    # Don't allow updating campaign_id or created_at
    update_data.pop("campaign_id", None)
    update_data.pop("created_at", None)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    
    campaign.update(update_data)
    return campaign

@app.delete(
    "/campaigns/{campaign_id}",
    tags=["Campaigns"],
    summary="Delete a campaign",
    description="Delete a campaign by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Campaign deleted successfully"},
        404: {
            "description": "Campaign not found",
            "model": ErrorResponse
        },
        422: {"description": "Validation error"}
    }
)
async def delete_campaign(campaign_id: int = Path(..., gt=0, description="Campaign ID (must be positive integer)")):
    """Delete a campaign by ID"""
    campaign = next((item for item in data if item["campaign_id"] == campaign_id), None)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with ID {campaign_id} not found"
        )
    
    data.remove(campaign)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

# Custom exception handlers for better error responses
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )
