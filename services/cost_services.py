from db.cost_db import CostDb
from models.costs import Cost
from fastapi import HTTPException, status

cost_db = CostDb()
cost_db.create_cost_tables()


def get_all_cost_service():
    all_costs = []
    try:
        rows = cost_db.get_all_costs()
        for row in rows:
            cost = Cost(description=row["description"], amount=row["amount"], id=row["cost_id"])
            all_costs.append(cost)
        return all_costs
    
    except Exception as e:
        raise RuntimeError(f"error in fetching all costs from db: {e}")
    
def add_cost_service(cost: Cost):
    try:
        return cost_db.add_cost(cost)

    except Exception as e:
        raise RuntimeError(f"error in adding cost to db: {e}")
    
def delete_cost_service(cost_id: int):
    if cost_db.get_one_cost(cost_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not cost found to delete!")
    try: 
        cost_db.delete_cost(cost_id)
        return True
    except Exception as e:
        raise RuntimeError(f"error in deleting cost to db: {e}")

def update_cost_service(cost_id: int, cost: Cost):
    if cost_db.get_one_cost(cost_id) is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no cost found to update!")
    try:
        cost.id = cost_id
        cost_db.update_cost(cost)
        return True
    except Exception as e:
        raise RuntimeError(f"error in updating cost: {e}")

