from app.use_cases.update_user import UpdateUser
from datetime import date
from app.schemas.user import UserUpdate
from unittest.mock import MagicMock


def test_update_user_profile_recalculates_dates():
    repo = MagicMock()
    repo.get_by_user_id.return_value = MagicMock(
        user_id=1,
        full_name=None,
        pregnancy_start_date=None,
        due_date=None
    )

    uc = UpdateUser(repo=repo)

    payload = UserUpdate(due_date=date(2026, 9, 7))
    uc.execute(user_id=1, **payload.model_dump(exclude_unset=True))

    repo.save.assert_called_once()
    saved_profile = repo.save.call_args[0][0]

    assert saved_profile.due_date == date(2026, 9, 7)
    assert saved_profile.pregnancy_start_date == date(2025, 11, 1)