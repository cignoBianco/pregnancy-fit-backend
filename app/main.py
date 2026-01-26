from fastapi import FastAPI
from app.api import plans, workouts, auth, exercises, user, user_profile

app = FastAPI(title="Pregnancy Fit API")

app.include_router(plans.router)
app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(user_profile.router)
