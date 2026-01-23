from fastapi import FastAPI
from app.api import plans, workouts, auth, exercises

app = FastAPI(title="Pregnancy Fit API")

app.include_router(plans.router)
app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(auth.router)