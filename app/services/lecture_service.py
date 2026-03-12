from __future__ import annotations

from datetime import date
from typing import List

from app.domain.models import Lecture
from app.domain.repositories import LectureRepository


class LectureService:
    """Прикладной сервис работы с лекциями, опирающийся на абстрактный репозиторий."""

    def __init__(self, repository: LectureRepository) -> None:
        self._repository = repository

    def get_lecture(self, lecture_id: int) -> Lecture:
        return self._repository.get_lecture(lecture_id)

    def list_lectures_by_date(self, lecture_date: date) -> List[Lecture]:
        return self._repository.list_lectures_by_date(lecture_date)

