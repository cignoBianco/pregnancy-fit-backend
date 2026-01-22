from sqlmodel import Session
from app.core.database import engine
from app.models.exercise import Exercise
from app.seed.exercises import EXERCISES

def run():
    with Session(engine) as session:
        for ex in EXERCISES:
            session.add(Exercise(**ex))
        session.commit()

if __name__ == "__main__":
    run()