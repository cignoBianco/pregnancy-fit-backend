from app.domain.pregnancy import PregnancyDates
from datetime import date

def test_due_date_only_recalculates_start():
    p = PregnancyDates.normalize(
        pregnancy_start_date=None,
        due_date=date(2026, 9, 7),
    )

    assert p.due_date == date(2026, 9, 7)
    assert p.pregnancy_start_date == date(2025, 11, 1)
