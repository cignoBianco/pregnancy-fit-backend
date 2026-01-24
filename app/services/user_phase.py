from datetime import date
from typing import Optional
from app.models.enums import PregnancyPhase

def calculate_phase(
     *,
    pregnancy_start_date: Optional[date] = None,
    due_date: Optional[date] = None
) -> Optional[str]:
    today = date.today()

    if pregnancy_start_date:
        weeks = (today - pregnancy_start_date).days // 7
    elif due_date:
        weeks = 40 - ((due_date - today).days // 7)
    else:
        return None

    if weeks < 0:
        return None
    elif weeks < 13:
        return PregnancyPhase.pregnancy_t1
    elif weeks < 28:
        return PregnancyPhase.pregnancy_t2
    elif weeks <= 40:
        return PregnancyPhase.pregnancy_t3
    return PregnancyPhase.postpartum_0_6
