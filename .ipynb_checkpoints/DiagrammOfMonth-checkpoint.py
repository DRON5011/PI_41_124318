import os
from typing import Optional

import requests
import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px


# =========================
# Конфигурация подключения к NocoDB
# =========================

NOCODB_BASE_URL: str = os.getenv("localhost:8080/dashboard", "").rstrip("/")
NOCODB_PROJECT: str = os.getenv("noco.db", "")
NOCODB_TABLE: str = os.getenv("Лекции", "")
NOCODB_TOKEN: Optional[str] = os.getenv("h070wPAEcnvRUrqeXswZu-LP7HZqnqZCo5PQudOg")

# Имя поля даты в таблице NocoDB.
# Можно переопределить через переменную окружения NOCODB_DATE_FIELD.
DATE_FIELD: str = os.getenv("Дата проведения", "lesson_date")


def _build_nocodb_url() -> str:
    """
    Формирует URL для получения строк таблицы из NocoDB.

    При необходимости вы можете адаптировать этот шаблон под свою инстанцию NocoDB.
    Примеры путей в NocoDB v2:
    - /api/v2/projects/{project}/tables/{table}/rows
    """
    if not NOCODB_BASE_URL or not NOCODB_PROJECT or not NOCODB_TABLE:
        raise RuntimeError(
            "Не заданы переменные окружения NOCODB_BASE_URL, NOCODB_PROJECT или NOCODB_TABLE."
        )

    return f"{NOCODB_BASE_URL}/projects/{NOCODB_PROJECT}/tables/{NOCODB_TABLE}/rows"


def _build_nocodb_headers() -> dict:
    """
    Формирует заголовки для запроса к NocoDB.

    По умолчанию используется заголовок `xc-token`, который типичен для NocoDB.
    При необходимости можно заменить на `Authorization: Bearer ...`.
    """
    headers: dict = {}
    if NOCODB_TOKEN:
        headers["xc-token"] = NOCODB_TOKEN
    return headers


def fetch_lessons() -> pd.DataFrame:
    """
    Получает данные о занятиях из NocoDB и возвращает их в виде pandas.DataFrame.
    Ожидается, что в данных есть поле с датой занятий (DATE_FIELD).
    """
    url = _build_nocodb_url()
    headers = _build_nocodb_headers()

    # Можно настроить параметры, например pageSize, фильтры по месяцу и т.д.
    params = {
        "limit": 1000,
    }

    response = requests.get(url, headers=headers, params=params, timeout=15)
    if response.status_code != 200:
        raise RuntimeError(
            f"Ошибка при обращении к NocoDB API: {response.status_code} {response.text}"
        )

    data = response.json()

    # В NocoDB ответ обычно содержит ключ 'list' со списком записей.
    # Если структура отличается, адаптируйте извлечение здесь.
    if isinstance(data, dict) and "list" in data:
        rows = data.get("list", [])
    elif isinstance(data, list):
        rows = data
    else:
        rows = []

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows)


def aggregate_by_day(df: pd.DataFrame) -> pd.DataFrame:
    """
    Агрегирует количество занятий по дням месяца.
    Ожидает, что в df есть колонка DATE_FIELD с датой занятия.
    """
    if df.empty:
        return pd.DataFrame(columns=["day", "count"])

    if DATE_FIELD not in df.columns:
        raise KeyError(
            f"В данных отсутствует поле даты '{DATE_FIELD}'. "
            f"Проверьте имя поля или задайте переменную окружения NOCODB_DATE_FIELD."
        )

    df = df.copy()
    df[DATE_FIELD] = pd.to_datetime(df[DATE_FIELD], errors="coerce")
    df = df.dropna(subset=[DATE_FIELD])

    if df.empty:
        return pd.DataFrame(columns=["day", "count"])

    df["day"] = df[DATE_FIELD].dt.day

    grouped = df.groupby("day").size().reset_index(name="count")
    grouped = grouped.sort_values("day").reset_index(drop=True)
    return grouped


def build_figure(df_grouped: pd.DataFrame):
    """
    Строит график Plotly (столбчатая диаграмма) зависимости количества занятий от дня месяца.
    """
    if df_grouped.empty:
        fig = px.bar(
            x=[],
            y=[],
            labels={"x": "День месяца", "y": "Количество занятий"},
            title="Нет данных для отображения",
        )
        fig.update_layout(xaxis=dict(dtick=1))
        return fig

    fig = px.bar(
        df_grouped,
        x="day",
        y="count",
        labels={"day": "День месяца", "count": "Количество занятий"},
        title="Количество занятий по дням месяца",
    )

    fig.update_layout(
        xaxis=dict(
            dtick=1,
        )
    )

    return fig


# =========================
# Dash-приложение
# =========================

app = dash.Dash(__name__)


def _create_layout():
    """
    Создает layout приложения, загружая данные из NocoDB и строя график.
    """
    error_message = None
    figure = None

    try:
        lessons_df = fetch_lessons()
        grouped_df = aggregate_by_day(lessons_df)
        figure = build_figure(grouped_df)
    except Exception as exc:  # pylint: disable=broad-except
        # Сообщение выводим в консоль, а пользователю показываем общее уведомление.
        print(f"Ошибка при подготовке данных для диаграммы: {exc}")
        error_message = (
            "Произошла ошибка при загрузке данных из NocoDB. "
            "Проверьте настройки подключения и попробуйте снова."
        )
        figure = build_figure(pd.DataFrame(columns=["day", "count"]))

    children = [
        html.H1("Диаграмма занятий по дням месяца"),
        html.P(
            "График показывает количество занятий по дням месяца на основе данных из NocoDB."
        ),
        dcc.Graph(id="lessons-per-day-graph", figure=figure),
    ]

    if error_message:
        children.insert(
            1,
            html.Div(
                error_message,
                style={"color": "red", "marginBottom": "16px"},
            ),
        )

    return html.Div(children, style={"maxWidth": "960px", "margin": "0 auto"})


app.layout = _create_layout


if __name__ == "__main__":
    # Запускаем сервер Dash. При необходимости измените host/port.
    app.run_server(debug=True)

