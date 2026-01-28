from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional

PREGNANCY_DURATION_DAYS = 280
ALLOWED_DELTA_DAYS = 7


@dataclass(frozen=True)
class PregnancyDates:
    pregnancy_start_date: Optional[date]
    due_date: Optional[date]

    @classmethod
    def normalize(
        cls,
        pregnancy_start_date: Optional[date],
        due_date: Optional[date],
    ) -> "PregnancyDates":

        if pregnancy_start_date and due_date:
            expected_due = pregnancy_start_date + timedelta(
                days=PREGNANCY_DURATION_DAYS
            )
            delta = abs((expected_due - due_date).days)

            if delta > ALLOWED_DELTA_DAYS:
                raise ValueError(
                    "pregnancy_start_date and due_date contradict each other"
                )

            return cls(pregnancy_start_date, due_date)

        if pregnancy_start_date:
            return cls(
                pregnancy_start_date,
                pregnancy_start_date + timedelta(days=PREGNANCY_DURATION_DAYS),
            )

        if due_date:
            return cls(
                due_date - timedelta(days=PREGNANCY_DURATION_DAYS),
                due_date,
            )

        return cls(None, None)


@dataclass(frozen=True)
class PregnancyProgress:
    current_phase: Optional[str]
    weeks_progress: Optional[int]
    weeks_total: int = 40

    @classmethod
    def from_dates(
        cls,
        pregnancy_start_date: Optional[date],
        due_date: Optional[date],
        today: Optional[date] = None
    ) -> "PregnancyProgress":
        from app.services.user_phase import calculate_phase

        today = today or date.today()
        phase = calculate_phase(
            pregnancy_start_date=pregnancy_start_date,
            due_date=due_date,
            today=today
        )

        if not pregnancy_start_date and not due_date:
            return cls(current_phase=None, weeks_progress=None)

        # calculate weeks since start
        if pregnancy_start_date:
            weeks = (today - pregnancy_start_date).days // 7
        else:
            weeks = 40 - ((due_date - today).days // 7)

        if weeks < 0:
            return cls(current_phase=None, weeks_progress=None)

        weeks_progress = min(weeks, 40)
        return cls(current_phase=phase, weeks_progress=weeks_progress)
