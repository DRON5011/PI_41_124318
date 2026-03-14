from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, Iterable, Iterator, List, Optional

from .db_interface import DatabaseInterface


class SqliteDatabase(DatabaseInterface):
    """Реализация DatabaseInterface поверх sqlite3."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        resolved_path = (db_path or os.getenv("APP_SQLITE_PATH", "")).strip()
        if not resolved_path:
            raise RuntimeError(
                "Не задан путь к SQLite БД. "
                "Передайте db_path в SqliteDatabase или задайте переменную окружения APP_SQLITE_PATH."
            )

        self._db_path = resolved_path
        self._conn = sqlite3.connect(self._db_path)
        self._conn.row_factory = sqlite3.Row

    def close(self) -> None:
        if self._conn:
            self._conn.close()

    def execute(self, sql: str, params: Optional[Iterable[Any]] = None) -> None:
        try:
            with self._conn:
                self._conn.execute(sql, tuple(params) if params is not None else ())
        except sqlite3.Error as exc:  # pragma: no cover - обёртка над sqlite3
            raise RuntimeError(f"SQLite execute error: {exc}") from exc

    def fetch_one(
        self, sql: str, params: Optional[Iterable[Any]] = None
    ) -> Optional[Dict[str, Any]]:
        try:
            cur = self._conn.execute(sql, tuple(params) if params is not None else ())
            row = cur.fetchone()
        except sqlite3.Error as exc:  # pragma: no cover
            raise RuntimeError(f"SQLite fetch_one error: {exc}") from exc

        if row is None:
            return None
        return dict(row)

    def fetch_all(
        self, sql: str, params: Optional[Iterable[Any]] = None
    ) -> List[Dict[str, Any]]:
        try:
            cur = self._conn.execute(sql, tuple(params) if params is not None else ())
            rows = cur.fetchall()
        except sqlite3.Error as exc:  # pragma: no cover
            raise RuntimeError(f"SQLite fetch_all error: {exc}") from exc

        return [dict(r) for r in rows]

    @contextmanager
    def transaction(self) -> Iterator[None]:
        try:
            self._conn.execute("BEGIN")
            yield
            self._conn.execute("COMMIT")
        except sqlite3.Error as exc:  # pragma: no cover
            self._conn.execute("ROLLBACK")
            raise RuntimeError(f"SQLite transaction error: {exc}") from exc

    def __enter__(self) -> "SqliteDatabase":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

