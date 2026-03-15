from __future__ import annotations

from datetime import datetime

from app.infrastructure.sqlite_database import SqliteDatabase
from app.infrastructure.lecture_repository_sqlite import LectureRepositorySqlite
from app.services.lecture_service import LectureService


def _print_lecture_short(lecture) -> None:
    print(f"[{lecture.id}] {lecture.title}")


def _print_lecture_full(lecture) -> None:
    print(f"ID: {lecture.id}")
    print(f"Тема: {lecture.title}")
    if lecture.text:
        print(f"Текст:\n{lecture.text}")
    if lecture.audio_record_url:
        print(f"Аудиозапись: {lecture.audio_record_url}")
    if lecture.conspect_url:
        print(f"Конспект: {lecture.conspect_url}")


def main() -> None:
    # Используем файл noco.db в текущей директории проекта.
    # При необходимости путь можно поменять здесь.
    with SqliteDatabase(db_path="noco.db") as db:
        service = LectureService(LectureRepositorySqlite(db))

        while True:
            print("\n=== Меню работы с БД лекций ===")
            print("1. Показать лекцию по ID")
            print("2. Показать лекции по дате")
            print("0. Выход")

            choice = input("Ваш выбор: ").strip()

            if choice == "0":
                print("Выход.")
                break

            if choice == "1":
                raw_id = input("Введите ID лекции: ").strip()
                if not raw_id.isdigit():
                    print("ID должен быть целым числом.")
                    continue
                lecture_id = int(raw_id)
                try:
                    lecture = service.get_lecture(lecture_id)
                    _print_lecture_full(lecture)
                except LookupError as exc:
                    print(str(exc))
                continue

            if choice == "2":
                raw_date = input("Введите дату лекции (ГГГГ-ММ-ДД): ").strip()
                try:
                    dt = datetime.strptime(raw_date, "%Y-%m-%d").date()
                except ValueError:
                    print("Некорректный формат даты, ожидалось ГГГГ-ММ-ДД.")
                    continue

                lectures = service.list_lectures_by_date(dt)
                if not lectures:
                    print("Лекций на эту дату не найдено.")
                else:
                    print(f"Найдено лекций: {len(lectures)}")
                    for lec in lectures:
                        _print_lecture_short(lec)
                continue

            print("Неизвестный пункт меню, попробуйте ещё раз.")


if __name__ == "__main__":
    main()

