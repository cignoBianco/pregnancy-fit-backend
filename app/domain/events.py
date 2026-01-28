from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class PregnancyPhaseChanged:
    user_id: int
    old_phase: Optional[str]
    new_phase: Optional[str]
    effective_date: date
