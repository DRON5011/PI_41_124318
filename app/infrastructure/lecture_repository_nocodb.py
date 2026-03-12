from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List

from app.domain.models import Lecture
from app.domain.repositories import LectureRepository
from .nocodb_client import NocoDbClient


class LectureRepositoryNocoDb(LectureRepository):
    """Реализация LectureRepository поверх таблицы лекций в NocoDB."""

    def __init__(self, client: NocoDbClient, lectures_table_id: str | None = None) -> None:
        self._client = client
        self._table_id = lectures_table_id or self._get_table_id_from_env()

    @staticmethod
    def _get_table_id_from_env() -> str:
        import os

        table_id = os.getenv("NOCODB_LECTURES_TABLE_ID", "")
        if not table_id:
            raise RuntimeError(
                "Не задан NOCODB_LECTURES_TABLE_ID для LectureRepositoryNocoDb."
            )
        return table_id

    def _build_records_path(self) -> str:
        return f"/tables/{self._table_id}/records"

    def _map_record_to_lecture(self, record: Dict[str, Any]) -> Lecture:
        """Преобразует JSON‑запись NocoDB в доменную модель Lecture."""
        lecture_id = int(record.get("Id"))
        title = str(record.get("Тема лекции", ""))
        audio_record_url = None  # можно вытянуть из связанной сущности Аудиозаписи при необходимости
        conspect_url = None

        return Lecture(
            id=lecture_id,
            title=title,
            audio_record_url=audio_record_url,
            text=None,
            conspect_url=conspect_url,
        )

    def get_lecture(self, lecture_id: int) -> Lecture:
        params = {"where": f"(Id,eq,{lecture_id})", "limit": 1}
        data = self._client.request(
            "GET", self._build_records_path(), params=params
        )

        rows = data.get("list", []) if isinstance(data, dict) else []
        if not rows:
            raise LookupError(f"Лекция с Id={lecture_id} не найдена.")

        return self._map_record_to_lecture(rows[0])

    def list_lectures_by_date(self, lecture_date: date) -> List[Lecture]:
        # Имя поля даты в таблице NocoDB
        import os

        date_field = os.getenv("NOCODB_DATE_FIELD", "Дата проведения")
        iso_date = lecture_date.isoformat()

        params = {
            "where": f"({date_field},eq,{iso_date})",
            "limit": 1000,
        }
        data = self._client.request(
            "GET", self._build_records_path(), params=params
        )

        rows = data.get("list", []) if isinstance(data, dict) else []
        return [self._map_record_to_lecture(row) for row in rows]

