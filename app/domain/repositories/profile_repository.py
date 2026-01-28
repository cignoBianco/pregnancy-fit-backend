from abc import ABC, abstractmethod
from app.domain.profile import UserProfile


class ProfileRepository(ABC):

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> UserProfile:
        ...

    @abstractmethod
    def save(self, profile: UserProfile) -> None:
        ...
