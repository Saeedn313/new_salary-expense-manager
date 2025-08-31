from fastapi import APIRouter, HTTPException, status
from services import cost_services
from models.costs import Cost

router = APIRouter(prefix="/costs", tags=["costs"])


@router.get("/")
def get_all_costs():
    try:
        costs = cost_services.get_all_cost_service()
        return {"costs": costs}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    
@router.post("/add-cost")
def add_new_cost(cost: Cost):
    try:
        new_cost = cost_services.add_cost_service(cost)
        return {"cost": new_cost}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")

@router.delete("/delete-cost/{cost_id}")
def delete_cost(cost_id: int):
    try:
        if cost_services.delete_cost_service(cost_id):
            return {"detail": f"cost with id: {cost_id} is deleted!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/update-cost/{cost_id}")
def update_cost(cost_id: int, cost: Cost):
    try:
        if cost_services.update_cost_service(cost_id, cost):
            return {f"detail": f"cost with id: {cost_id} is updated!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    

