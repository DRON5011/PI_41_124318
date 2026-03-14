from __future__ import annotations

from datetime import date
from typing import Any, Dict, List

from app.domain.models import Lecture
from app.domain.repositories import LectureRepository
from .db_interface import DatabaseInterface


class LectureRepositorySqlite(LectureRepository):
    """Реализация LectureRepository поверх таблицы lectures в SQLite."""

    def __init__(self, db: DatabaseInterface) -> None:
        self._db = db

    @staticmethod
    def _row_to_lecture(row: Dict[str, Any]) -> Lecture:
        """Преобразует строку БД (dict) в доменную модель Lecture."""
        return Lecture(
            id=int(row["id"]),
            title=str(row.get("title", "")),
            audio_record_url=row.get("audio_record_url"),
            text=row.get("text"),
            conspect_url=row.get("conspect_url"),
        )

    def get_lecture(self, lecture_id: int) -> Lecture:
        sql = """
        SELECT id, title, audio_record_url, text, conspect_url
        FROM lectures
        WHERE id = ?
        """
        row = self._db.fetch_one(sql, (lecture_id,))
        if row is None:
            raise LookupError(f"Лекция с id={lecture_id} не найдена.")
        return self._row_to_lecture(row)

    def list_lectures_by_date(self, lecture_date: date) -> List[Lecture]:
        sql = """
        SELECT id, title, audio_record_url, text, conspect_url
        FROM lectures
        WHERE lecture_date = ?
        ORDER BY id
        """
        rows = self._db.fetch_all(sql, (lecture_date.isoformat(),))
        return [self._row_to_lecture(r) for r in rows]

