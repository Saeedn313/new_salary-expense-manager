from fastapi import APIRouter, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from db.cost_db import CostDb
from models.costs import CostIn
import os

router = APIRouter(prefix="/costs", tags=["costs"])
cost_db = CostDb()
cost_db.create_cost_tables()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))

@router.get("/", response_class=HTMLResponse)
def get_all_costs(request: Request):
    try:
        costs = cost_db.get_all_costs()
        if len(costs) < 1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No cost found!")
        return templates.TemplateResponse("costs.html", {"request": request, "costs": costs})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.get("/{cost_id}", response_class=HTMLResponse)
def get_one_user(cost_id: int, request: Request):
    try:
        cost = cost_db.get_one_cost(cost_id)
        if cost == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no cost found")
        return templates.TemplateResponse("user_profile.html", {"request": request, "cost": cost})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/add-cost")
def add_new_cost(cost: CostIn):
    try:
        cost_db.add_cost(cost.dict())
        return RedirectResponse(url="/costs", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.post("/delete-cost/{cost_id}")
def delete_cost(cost_id: int):
    try:
        deleted = cost_db.delete_cost(cost_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No cost found to delete!")
        return RedirectResponse(url="/costs", status_code=status.HTTP_303_SEE_OTHER)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/update-cost/{cost_id}")
def update_cost(cost_id: int, cost: CostIn):
    print(cost)
    try:
        updated = cost_db.update_cost(cost_id, cost.dict())
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found to update!")
        return RedirectResponse(url="/costs", status_code=status.HTTP_303_SEE_OTHER)
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

