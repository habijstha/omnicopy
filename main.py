from datetime import datetime
from fastapi import FastAPI, Request, Body
from typing import Any
import random

app = FastAPI(root_path="/api/v1")

@app.get("/")   
async def read_root():
    return {"message": "Hello, World!"}

data: Any = [
    {
        "campaign_id": 1,
        "name": "Campaign 1",
        "due_date": datetime.now() ,
        "created_at": datetime.now()
    },
    {
        "campaign_id": 2,
        "name": "Campaign 2",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    }
]
"""
Campaigns
- campaign_id
- name
- due_date
- created_at
"""

@app.get("/campaigns")
async def read_campaigns():
    return {"Campaigns": data}


@app.get("/campaigns/{campaign_id}")
async def read_campaign(campaign_id: int):
    return {"Campaign": next((item for item in data if item["campaign_id"] == campaign_id), None)}

@app.post("/campaigns")
async def create_campaign(request: dict[str, Any] = Body(...)):

    new_campaign: Any = {
        "campaign_id": random.randint(1, 1000),
        "name": request.get("name"),
        "due_date": request.get("due_date"),
        "created_at": datetime.now()
    }
    data.append(new_campaign)
    return {"Campaign": new_campaign}