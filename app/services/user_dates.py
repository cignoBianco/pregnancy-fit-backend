from datetime import timedelta, date
from typing import Optional


def normalize_pregnancy_dates(
    *,
    pregnancy_start_date:Optional[date],
    due_date: Optional[date],
) -> tuple[Optional[date], Optional[date]]:

    if pregnancy_start_date and not due_date:
        due_date = pregnancy_start_date + timedelta(weeks=40)

    if due_date and not pregnancy_start_date:
        pregnancy_start_date = due_date - timedelta(weeks=40)

    return pregnancy_start_date, due_date
