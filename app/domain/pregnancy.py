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
