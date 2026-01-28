from dataclasses import dataclass
from datetime import date
from typing import List, Optional

from app.domain.events import PregnancyPhaseChanged
from app.domain.pregnancy import PregnancyDates, PregnancyProgress
from app.models.enums import EquipmentEnum, ContraindicationEnum, TrainingGoalEnum


@dataclass
class UserProfile:
    user_id: int
    full_name: Optional[str] = None
    pregnancy_start_date: Optional[date] = None
    due_date: Optional[date] = None
    equipment: List[EquipmentEnum] = None
    contraindications: List[ContraindicationEnum] = None
    training_goals: List[TrainingGoalEnum] = None
    notes: Optional[str] = None

     _events: List[object] = field(default_factory=list, init=False, repr=False)

    def update_pregnancy_dates(
        self,
        pregnancy_start_date: Optional[date],
        due_date: Optional[date],
    ):
        old_phase = PregnancyProgress.from_dates(
            self.pregnancy_start_date,
            self.due_date
        ).current_phase

        pregnancy = PregnancyDates.normalize(pregnancy_start_date, due_date)

        self.pregnancy_start_date = pregnancy.pregnancy_start_date
        self.due_date = pregnancy.due_date

        new_phase = PregnancyProgress.from_dates(
            self.pregnancy_start_date,
            self.due_date
        ).current_phase

        if old_phase != new_phase:
            self._events.append(
                PregnancyPhaseChanged(
                    user_id=self.user_id,
                    old_phase=old_phase,
                    new_phase=new_phase,
                    effective_date=date.today(),
                )
            )

    def pop_events(self) -> List[object]:
        events, self._events = self._events, []
        return events

    def __post_init__(self):
        self.equipment = self.equipment or []
        self.contraindications = self.contraindications or []
        self.training_goals = self.training_goals or []
