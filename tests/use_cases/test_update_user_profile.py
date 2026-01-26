from app.use_cases.update_user_profile import UpdateUserProfile
from datetime import date

def test_update_due_date_only(db_session, user):
    uc = UpdateUserProfile(db_session)

    result = uc.execute(
        user=user,
        data=UserUpdate(due_date=date(2026, 9, 7)),
    )

    assert result.due_date == date(2026, 9, 7)
    assert result.pregnancy_start_date is not None
