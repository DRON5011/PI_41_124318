from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Dict, Iterable, Iterator, List, Optional, Protocol, runtime_checkable


@runtime_checkable
class SupportsDbConnection(Protocol):
    """Протокол для объектов, умеющих закрывать соединение с БД."""

    def close(self) -> None:  # pragma: no cover - простой протокол
        ...


class DatabaseInterface(ABC):
    """Минимальный интерфейс низкоуровневого клиента БД.

    Интерфейс ориентирован на SQLite, но остаётся достаточно общим,
    чтобы при необходимости можно было реализовать его для другой СУБД.
    """

    @abstractmethod
    def execute(self, sql: str, params: Optional[Iterable[Any]] = None) -> None:
        """Выполняет SQL‑команду без ожидания результата (INSERT/UPDATE/DELETE/DDL)."""
        raise NotImplementedError

    @abstractmethod
    def fetch_one(
        self, sql: str, params: Optional[Iterable[Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Выполняет запрос и возвращает одну строку в виде словаря или None."""
        raise NotImplementedError

    @abstractmethod
    def fetch_all(
        self, sql: str, params: Optional[Iterable[Any]] = None
    ) -> List[Dict[str, Any]]:
        """Выполняет запрос и возвращает список строк в виде словарей."""
        raise NotImplementedError

    @abstractmethod
    @contextmanager
    def transaction(self) -> Iterator[None]:
        """Контекстный менеджер для выполнения нескольких операций в одной транзакции."""
        raise NotImplementedError

