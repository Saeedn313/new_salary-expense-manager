from fastapi import APIRouter, HTTPException, status
from db.cost_db import CostDb
from models.api_models.cost_schema import CostIn, CostOut


router = APIRouter(prefix="/api/costs", tags=["costs"])
cost_db = CostDb()
cost_db.create_cost_tables()


@router.get("/summery")
def get_cost_summery():
    costs_summery = cost_db.get_costs_summery()
    return {"summery": costs_summery}

@router.get("/monthly-range")
def filter_costs(start_year: int, end_year: int, start_month:int = None, end_month: int = None):
    try:
        if start_month and not end_month or not start_month and end_month:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start and end month both should be specified!")
        
        filtered_costs = cost_db.get_cost_within_year_month(start_year, end_year, start_month, end_month)
        
        if filtered_costs is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found!")
        return {"data": filtered_costs}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.get("/monthly-costs-avg")
def get_monthly_cost_avg(year: int, month: int):
    try:
        monthly_cost_avg = cost_db.get_avg_month_year(year, month)
        if monthly_cost_avg is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost not found")
        return {"data": monthly_cost_avg}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
    
    
@router.get("/")
def get_all_costs():
    try:
        costs = cost_db.get_all_costs()
        if len(costs) < 1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No cost found!")
        costs_out = [CostOut(**cost.to_dict()) for cost in costs]
        return {"costs": costs_out}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.get("/{cost_id}")
def get_one_user(cost_id: int):
    try:
        cost = cost_db.get_one_cost(cost_id)
        if cost == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no cost found")
        
        cost_out = CostOut(**cost.to_dict())
        return {"cost": cost_out}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/add-cost")
def add_new_cost(cost: CostIn):
    try:
        new_cost = cost_db.add_cost(cost.dict())
        cost_out = CostOut(**new_cost.to_dict())
        return {"cost": cost_out}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.delete("/delete-cost/{cost_id}")
def delete_cost(cost_id: int):
    try:
        deleted = cost_db.delete_cost(cost_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No cost found to delete!")
        return {"message": f"Cost with id {cost_id} is deleted!"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/update-cost/{cost_id}")
def update_cost(cost_id: int, cost: CostIn):
    print(cost.dict())
    try:
        updated = cost_db.update_cost(cost_id, cost.dict())
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found to update!")
        return {"message": f"Cost with id {cost_id} is updated!"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

    

    

