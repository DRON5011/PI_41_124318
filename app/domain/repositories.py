from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List

from .models import Lecture


class LectureRepository(ABC):
    """Абстракция доступа к данным лекций, не зависящая от конкретной БД или NocoDB."""

    @abstractmethod
    def get_lecture(self, lecture_id: int) -> Lecture:
        raise NotImplementedError

    @abstractmethod
    def list_lectures_by_date(self, lecture_date: date) -> List[Lecture]:
        raise NotImplementedError

