import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

from app.infrastructure.nocodb_client import NocoDbClient
from app.infrastructure.lecture_repository_nocodb import LectureRepositoryNocoDb
from app.services.lecture_service import LectureService

def aggregate_by_day(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["day", "count"])

    if "lecture_date" not in df.columns:
        return pd.DataFrame(columns=["day", "count"])

    df = df.copy()
    df["lecture_date"] = pd.to_datetime(df["lecture_date"], errors="coerce")
    df = df.dropna(subset=["lecture_date"])

    if df.empty:
        return pd.DataFrame(columns=["day", "count"])

    df["day"] = df["lecture_date"].dt.day

    grouped = df.groupby("day").size().reset_index(name="count")
    grouped = grouped.sort_values("day").reset_index(drop=True)
    return grouped


def build_figure(df_grouped: pd.DataFrame):
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
        client = NocoDbClient()
        repo = LectureRepositoryNocoDb(client)
        service = LectureService(repo)

        # Для диаграммы берём все лекции без фильтра по дате,
        # NocoDB‑репозиторий здесь можно расширить при необходимости.
        import os
        from datetime import datetime

        date_field = os.getenv("NOCODB_DATE_FIELD", "Дата проведения")

        # Получаем «сырые» записи напрямую, так как статистика работает только с датой.
        data = client.request(
            "GET",
            f"/tables/{os.getenv('NOCODB_LECTURES_TABLE_ID', '')}/records",
            params={"limit": 1000},
        )

        rows = data.get("list", []) if isinstance(data, dict) else []
        df = pd.DataFrame(rows)

        if date_field in df.columns:
            df["lecture_date"] = pd.to_datetime(df[date_field], errors="coerce")
        else:
            df["lecture_date"] = pd.NaT

        lessons_df = df
        grouped_df = aggregate_by_day(lessons_df)
        figure = build_figure(grouped_df)
    except Exception as exc:
        print(f"Ошибка при подготовке данных для диаграммы: {exc}")
        error_message = (
            "Произошла ошибка при загрузке данных из NocoDB. "
            "Проверьте настройки подключения и попробуйте снова."
        )
        figure = build_figure(pd.DataFrame(columns=["day", "count"]))

    children = [
        html.H1("Диаграмма занятий по дням месяца"),
        html.P(
            "График показывает количество занятий по дням месяца на основе данных из БД."
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

