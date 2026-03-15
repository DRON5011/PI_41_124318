from __future__ import annotations

from datetime import datetime
from pathlib import Path
from tkinter import (
    BOTH,
    END,
    LEFT,
    RIGHT,
    X,
    Y,
    Button,
    Entry,
    Frame,
    Label,
    Listbox,
    Scrollbar,
    StringVar,
    Text,
    Tk,
    messagebox,
)

from app.infrastructure.lecture_repository_sqlite import LectureRepositorySqlite
from app.infrastructure.sqlite_database import SqliteDatabase
from app.services.lecture_service import LectureService


def _default_db_path() -> str:
    """
    Возвращает путь к файлу БД по умолчанию.

    Ожидается, что файл `nocodb.db` лежит в корне проекта
    `PI_41_124318`, то есть на один уровень выше папки `app`.
    """
    base_dir = Path(__file__).resolve().parents[1]
    return str(base_dir / "nocodb.db")


class LectureApp:
    def __init__(self, master: Tk, db_path: str | None = None) -> None:
        self.master = master
        self.master.title("Лекции (SQLite)")

        resolved_db_path = db_path or _default_db_path()

        self._db = SqliteDatabase(db_path=resolved_db_path)
        self._service = LectureService(LectureRepositorySqlite(self._db))

        # Верхняя панель для поиска по ID
        top_frame = Frame(master)
        top_frame.pack(fill=X, padx=10, pady=5)

        Label(top_frame, text="ID лекции:").pack(side=LEFT)
        self.lecture_id_var = StringVar()
        self.entry_id = Entry(top_frame, textvariable=self.lecture_id_var, width=10)
        self.entry_id.pack(side=LEFT, padx=5)
        Button(top_frame, text="Показать", command=self.show_by_id).pack(side=LEFT, padx=5)

        # Панель для поиска по дате
        date_frame = Frame(master)
        date_frame.pack(fill=X, padx=10, pady=5)

        Label(date_frame, text="Дата (ГГГГ-ММ-ДД):").pack(side=LEFT)
        self.date_var = StringVar()
        self.entry_date = Entry(date_frame, textvariable=self.date_var, width=12)
        self.entry_date.pack(side=LEFT, padx=5)
        Button(date_frame, text="Найти лекции по дате", command=self.search_by_date).pack(
            side=LEFT, padx=5
        )

        # Основная область: список лекций + подробности
        main_frame = Frame(master)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Список лекций
        list_frame = Frame(main_frame)
        list_frame.pack(side=LEFT, fill=Y)

        Label(list_frame, text="Лекции:").pack(anchor="w")
        self.listbox = Listbox(list_frame, width=30)
        self.listbox.pack(side=LEFT, fill=Y)
        scrollbar = Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind("<<ListboxSelect>>", self.on_select_lecture)

        # Подробности лекции
        details_frame = Frame(main_frame)
        details_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))

        Label(details_frame, text="Подробности:").pack(anchor="w")
        self.details = Text(details_frame, wrap="word")
        self.details.pack(fill=BOTH, expand=True)

        # Нижняя панель
        bottom_frame = Frame(master)
        bottom_frame.pack(fill=X, padx=10, pady=5)

        Button(bottom_frame, text="Обновить по дате", command=self.search_by_date).pack(
            side=LEFT
        )
        Button(bottom_frame, text="Выход", command=self.on_close).pack(side=RIGHT)

        # Хранилище текущих лекций, отображаемых в списке
        self._current_lectures = []

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_by_id(self) -> None:
        raw_id = self.lecture_id_var.get().strip()
        if not raw_id.isdigit():
            messagebox.showerror("Ошибка", "ID должен быть целым числом.")
            return
        lecture_id = int(raw_id)
        try:
            lecture = self._service.get_lecture(lecture_id)
        except LookupError as exc:
            messagebox.showinfo("Не найдено", str(exc))
            return

        # Показать лекцию в подробностях
        self._current_lectures = [lecture]
        self.listbox.delete(0, END)
        self.listbox.insert(END, f"[{lecture.id}] {lecture.title}")
        self._show_details(lecture)

    def search_by_date(self) -> None:
        raw_date = self.date_var.get().strip()
        if not raw_date:
            messagebox.showerror("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД.")
            return
        try:
            dt = datetime.strptime(raw_date, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты, ожидалось ГГГГ-ММ-ДД.")
            return

        lectures = self._service.list_lectures_by_date(dt)
        self._current_lectures = lectures
        self.listbox.delete(0, END)
        if not lectures:
            messagebox.showinfo("Результат", "Лекций на эту дату не найдено.")
            self.details.delete("1.0", END)
            return

        for lec in lectures:
            self.listbox.insert(END, f"[{lec.id}] {lec.title}")

        # Показать первую лекцию по умолчанию
        self.listbox.select_set(0)
        self._show_details(lectures[0])

    def on_select_lecture(self, event=None) -> None:  # type: ignore[override]
        if not self._current_lectures:
            return
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        if 0 <= idx < len(self._current_lectures):
            self._show_details(self._current_lectures[idx])

    def _show_details(self, lecture) -> None:
        self.details.delete("1.0", END)
        lines = [
            f"ID: {lecture.id}",
            f"Тема: {lecture.title}",
        ]
        if lecture.text:
            lines.append("")
            lines.append("Текст:")
            lines.append(lecture.text)
        if lecture.audio_record_url:
            lines.append("")
            lines.append(f"Аудиозапись: {lecture.audio_record_url}")
        if lecture.conspect_url:
            lines.append(f"Конспект: {lecture.conspect_url}")

        self.details.insert("1.0", "\n".join(lines))

    def on_close(self) -> None:
        try:
            self._db.close()
        except Exception:
            pass
        self.master.destroy()


def main() -> None:
    root = Tk()
    LectureApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

