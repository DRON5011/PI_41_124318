from __future__ import annotations

from datetime import date

from app.infrastructure.sqlite_database import SqliteDatabase
from app.infrastructure.lecture_repository_sqlite import LectureRepositorySqlite
from app.services.lecture_service import LectureService


def main() -> None:
    # Путь к БД можно задать через переменную окружения APP_SQLITE_PATH
    # или явно передать в SqliteDatabase(db_path="path/to/db.sqlite3").
    with SqliteDatabase() as db:
        lecture_repo = LectureRepositorySqlite(db)
        service = LectureService(lecture_repo)

        # Пример: получить лекцию по идентификатору
        try:
            lecture = service.get_lecture(1)
            print(f"Лекция 1: {lecture.title}")
        except LookupError:
            print("Лекция с id=1 не найдена.")

        # Пример: список лекций по дате
        today = date.today()
        lectures_today = service.list_lectures_by_date(today)
        print(f"Лекций на {today.isoformat()}: {len(lectures_today)}")


if __name__ == "__main__":
    main()

