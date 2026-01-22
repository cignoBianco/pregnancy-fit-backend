from datetime import date
from pydantic import BaseModel

class PlanCreate(BaseModel):
    start_date: date
    weeks: int

class PlanResponse(BaseModel):
    plan_id: int
    workouts_count: int