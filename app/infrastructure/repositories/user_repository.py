from sqlmodel import Session
from app.models.user import User


class SQLUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_user_id(self, user_id: int) -> UserProfile:
        user = self.session.get(User, user_id)

        return UserProfile(
            full_name=user.full_name,
            pregnancy_start_date=user.pregnancy_start_date,
            due_date=user.due_date,
        )

    def save(self, user_id: int, profile: UserProfile):
        user = self.session.get(User, user_id)

        user.full_name = profile.full_name
        user.pregnancy_start_date = profile.pregnancy_start_date
        user.due_date = profile.due_date

        self.session.add(user)
