from datetime import timedelta, date
from app.domain.profile import UserProfile
from app.infrastructure.repositories.plan_repository_sql import SQLPlanRepository
from app.services.plan_generator import generate_training_plan, build_workout_exercises
from app.models.exercise import Exercise
from app.domain.pregnancy import PregnancyProgress
from app.models.plan import TrainingPlan, PlannedWorkout


class GenerateTrainingPlanUseCase:
    def __init__(
        self,
        plan_repo: SQLPlanRepository,
        exercises: list[Exercise],
    ):
        self.plan_repo = plan_repo
        self.exercises = exercises

    def execute(self, user_profile: UserProfile):

        progress = PregnancyProgress.from_dates(
            user_profile.pregnancy_start_date,
            user_profile.due_date,
        )

        phase = progress.current_phase or "postpartum_0_6"
        weeks = progress.weeks_progress or 4
        start_date = date.today()

        plan = self.plan_repo.add_or_commit_plan(
            user_id=user_profile.user_id,
            start_date=start_date,
            weeks=weeks,
            phase=phase,
        )

        workouts_data = generate_training_plan(
            phase=phase,
            start_date=start_date,
            weeks=weeks,
        )

        planned_workouts: list[PlannedWorkout] = []

        for w in workouts_data:
            workout = PlannedWorkout(
                plan_id=plan.id,
                date=w["date"],
                workout_type=w["workout_type"],
                duration=w["duration"],
            )

            workout = self.plan_repo.save_workout(workout)

            exercises = build_workout_exercises(
                exercises=self.exercises,
                phase=phase,
                equipment=[e.value for e in user_profile.equipment],
            )

            workout_exercises = [
                PlannedWorkoutExercise(
                    planned_workout_id=workout.id,
                    **ex,
                )
                for ex in exercises
            ]

            self.plan_repo.save_workout_exercises(workout_exercises)

            planned_workouts.append(workout)

        return planned_workouts