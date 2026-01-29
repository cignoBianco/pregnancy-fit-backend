from sqlmodel import Session, select
from app.domain.profile import UserProfile as DomainProfile
from app.models.user_profile import UserProfile as ORMProfile
from app.domain.pregnancy import PregnancyProgress


class SQLProfileRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_user_id(self, user_id: int) -> DomainProfile:
        orm_profile = self.session.exec(
            select(ORMProfile).where(ORMProfile.user_id == user_id)
        ).first()

        if not orm_profile:
            orm_profile = ORMProfile(user_id=user_id)
            self.session.add(orm_profile)
            self.session.commit()
            self.session.refresh(orm_profile)

        return DomainProfile(
            user_id=orm_profile.user_id,
            full_name=orm_profile.full_name,
            pregnancy_start_date=orm_profile.pregnancy_start_date,
            due_date=orm_profile.due_date,
            equipment=orm_profile.equipment,
            contraindications=orm_profile.contraindications,
            training_goals=orm_profile.training_goals,
            notes=orm_profile.notes,
        )

    def save(self, profile: DomainProfile) -> None:
        orm_profile = self.session.exec(
            select(ORMProfile).where(ORMProfile.user_id == profile.user_id)
        ).first()

        if not orm_profile:
            orm_profile = ORMProfile(user_id=profile.user_id)

        orm_profile.full_name = profile.full_name
        orm_profile.pregnancy_start_date = profile.pregnancy_start_date
        orm_profile.due_date = profile.due_date
        orm_profile.equipment = profile.equipment
        orm_profile.contraindications = profile.contraindications
        orm_profile.training_goals = profile.training_goals
        orm_profile.notes = profile.notes

        self.session.add(orm_profile)
        self.session.commit()
        self.session.refresh(orm_profile)


    def to_read_model(self, orm_profile: ORMProfile):
        progress = PregnancyProgress.from_dates(
            orm_profile.pregnancy_start_date,
            orm_profile.due_date
        )
        return {
            **orm_profile.model_dump(),
            "current_phase": progress.current_phase,
            "progress_weeks": progress.weeks_progress
        }

