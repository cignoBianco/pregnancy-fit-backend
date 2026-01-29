from app.use_cases.update_user_profile import UpdateUserProfile
from datetime import date
from app.schemas.user import UserUpdate
from unittest.mock import MagicMock

from app.domain.profile import UserProfile


def test_update_user_profile_recalculates_dates():
    repo = MagicMock()
    # repo.get_by_user_id.return_value = MagicMock(
    #     user_id=1,
    #     full_name=None,
    #     pregnancy_start_date=None,
    #     due_date=None
    # )
    profile = UserProfile(
        user_id=1,
        full_name=None,
        pregnancy_start_date=None,
        due_date=None,
    )
    repo.get_by_user_id.return_value = profile

    uc = UpdateUserProfile(repo=repo)

    uc.execute(user_id=1, due_date=date(2026, 9, 7),)

    repo.save.assert_called_once()
    saved_profile = repo.save.call_args[0][0]

    assert saved_profile.due_date == date(2026, 9, 7)
    assert saved_profile.pregnancy_start_date is not None