# app/domain/events.py
from dataclasses import dataclass

@dataclass(frozen=True)
class PregnancyPhaseChanged:
    user_id: int
    old_phase: str
    new_phase: str
