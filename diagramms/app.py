import os
import sys
import traceback
from typing import Optional, Dict, Any, List

import requests
import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px


# =========================
# Конфигурация из переменных окружения
# =========================

NOCODB_URL: str = os.getenv("NOCODB_URL", "http://host.docker.internal:8080").rstrip('/')
NOCODB_TOKEN: Optional[str] = os.getenv("NOCODB_TOKEN", "")
NOCODB_TABLE: str = os.getenv("NOCODB_TABLE", "Lections")
DATE_FIELD: str = os.getenv("DATE_FIELD", "lection_date")
TABLE_ID: Optional[str] = os.getenv("TABLE_ID", "m4i2yylgaqvy4m5")  # Правильный ID
API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
PAGE_SIZE: int = int(os.getenv("PAGE_SIZE", "100"))
DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"
PORT: int = int(os.getenv("PORT", "8050"))
HOST: str = os.getenv("HOST", "0.0.0.0")


def log_error(error_msg: str, exc_info: bool = True):
    """Функция для логирования ошибок"""
    print(f"❌ {error_msg}", file=sys.stderr)
    if exc_info:
        traceback.print_exc(file=sys.stderr)


def _build_nocodb_headers() -> Dict[str, str]:
    """Формирует заголовки для запроса к NocoDB API."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if NOCODB_TOKEN:
        headers["xc-token"] = NOCODB_TOKEN
    return headers


def fetch_lessons_from_nocodb() -> pd.DataFrame:
    """Получает данные о занятиях из NocoDB через API."""
    
    print("\n" + "=" * 50)
    print("📥 ЗАГРУЗКА ДАННЫХ ИЗ NOCODB")
    print("=" * 50)
    
    if not TABLE_ID:
        raise RuntimeError("TABLE_ID не указан!")
    
    url = f"{NOCODB_URL}/api/v2/tables/{TABLE_ID}/records"
    headers = _build_nocodb_headers()
    
    params = {
        "limit": PAGE_SIZE,
        "fields": DATE_FIELD,
    }
    
    print(f"🔍 Подключение к NocoDB API:")
    print(f"  URL: {url}")
    print(f"  Token: {'✓' if NOCODB_TOKEN else '✗'}")
    print(f"  Table ID: {TABLE_ID}")
    
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=API_TIMEOUT
        )
        
        print(f"  Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            records = []
            if isinstance(data, dict):
                if "list" in data:
                    records = data["list"]
                elif "data" in data:
                    records = data["data"]
            elif isinstance(data, list):
                records = data
            
            print(f"✅ Загружено записей: {len(records)}")
            
            if records:
                df = pd.DataFrame(records)
                print(f"📊 Колонки: {list(df.columns)}")
                return df
            else:
                print("⚠️ Нет записей в таблице")
                return pd.DataFrame()
        else:
            error_msg = f"Ошибка API: {response.status_code} - {response.text}"
            print(f"❌ {error_msg}")
            raise RuntimeError(error_msg)
            
    except Exception as e:
        log_error(f"Ошибка при загрузке данных: {e}")
        raise


def aggregate_by_day(df: pd.DataFrame) -> pd.DataFrame:
    """Агрегирует количество занятий по дням месяца."""
    print("\n📊 Агрегация данных...")
    
    if df.empty:
        print("  ⚠️ DataFrame пуст")
        return pd.DataFrame(columns=["day", "count"])

    # Определяем поле с датой
    date_field_to_use = DATE_FIELD
    
    if date_field_to_use not in df.columns:
        possible_fields = [col for col in df.columns if 'date' in col.lower()]
        if possible_fields:
            date_field_to_use = possible_fields[0]
            print(f"  ⚠️ Используем поле '{date_field_to_use}' как дату")
        else:
            error_msg = f"В данных отсутствует поле даты. Доступны: {list(df.columns)}"
            print(f"  ❌ {error_msg}")
            raise KeyError(error_msg)

    df = df.copy()
    print(f"  Конвертируем поле '{date_field_to_use}' в datetime...")
    
    try:
        df[date_field_to_use] = pd.to_datetime(df[date_field_to_use], errors="coerce")
        original_len = len(df)
        df = df.dropna(subset=[date_field_to_use])
        valid_dates = len(df)
        print(f"  ✅ Валидных дат: {valid_dates} из {original_len}")
    except Exception as e:
        log_error(f"Ошибка при конвертации дат: {e}")
        raise

    if df.empty:
        print("  ⚠️ Нет записей с валидными датами")
        return pd.DataFrame(columns=["day", "count"])

    # Извлекаем день месяца
    df["day"] = df[date_field_to_use].dt.day
    unique_days = sorted(df['day'].unique())
    print(f"  Дни месяца с занятиями: {unique_days}")
    
    grouped = df.groupby("day").size().reset_index(name="count")
    
    all_days = pd.DataFrame({"day": range(1, 32)})
    grouped = all_days.merge(grouped, on="day", how="left").fillna(0)
    grouped["count"] = grouped["count"].astype(int)
    
    days_with_data = len(grouped[grouped["count"] > 0])
    total_lectures = grouped['count'].sum()
    print(f"  📈 Дней с занятиями: {days_with_data}")
    print(f"  📊 Всего занятий: {total_lectures}")
    
    return grouped


def build_figure(df_grouped: pd.DataFrame):
    """Строит график Plotly."""
    print("\n📈 Построение графика...")
    
    try:
        if df_grouped.empty or df_grouped["count"].sum() == 0:
            print("  ⚠️ Нет данных для графика")
            empty_df = pd.DataFrame({"day": [], "count": []})
            fig = px.bar(
                empty_df,
                x="day",
                y="count",
                labels={"day": "День месяца", "count": "Количество занятий"},
                title="Нет данных для отображения",
            )
            return fig

        fig = px.bar(
            df_grouped,
            x="day",
            y="count",
            labels={"day": "День месяца", "count": "Количество занятий"},
            title="Количество занятий по дням месяца",
            color_discrete_sequence=["#2E86AB"],
            text="count"
        )

        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis=dict(
                dtick=1,
                tickvals=list(range(1, 32)),
                title="День месяца"
            ),
            yaxis=dict(
                dtick=1,
                title="Количество занятий"
            ),
            plot_bgcolor='rgba(240, 240, 240, 0.5)',
        )
        
        print("  ✅ График построен успешно")
        return fig
        
    except Exception as e:
        log_error(f"Ошибка при построении графика: {e}")
        raise


# =========================
# Dash-приложение
# =========================

app = dash.Dash(__name__)


def create_layout():
    """Создает layout приложения."""
    print("\n" + "=" * 50)
    print("🚀 ЗАПУСК ПРИЛОЖЕНИЯ")
    print("=" * 50)
    
    error_message = None
    warning_message = None
    figure = None

    try:
        # Загружаем данные
        lessons_df = fetch_lessons_from_nocodb()
        
        # Агрегируем
        grouped_df = aggregate_by_day(lessons_df)
        
        # Строим график
        figure = build_figure(grouped_df)
        
        if lessons_df.empty:
            warning_message = "⚠️ Таблица пуста. Добавьте данные в NocoDB."
        else:
            print("\n✅ Приложение готово к работе!")
            print(f"📊 Всего записей: {len(lessons_df)}")
            
    except Exception as exc:
        log_error(f"Критическая ошибка в create_layout: {exc}")
        error_message = f"❌ Ошибка: {str(exc)}"
        figure = build_figure(pd.DataFrame(columns=["day", "count"]))

    # Создаем layout
    children = [
        html.H1("📊 Количество занятий по дням месяца", 
                style={"textAlign": "center", "color": "#2E86AB"}),
        html.P(
            f"Данные из таблицы: {NOCODB_TABLE}",
            style={"textAlign": "center", "color": "#666", "fontSize": "14px"}
        )
    ]

    if warning_message:
        children.append(html.Div(
            warning_message, 
            style={
                "color": "#856404",
                "backgroundColor": "#fff3cd",
                "border": "1px solid #ffeeba",
                "borderRadius": "4px",
                "padding": "12px",
                "margin": "20px",
                "textAlign": "center"
            }
        ))

    if error_message:
        children.append(html.Div(
            error_message, 
            style={
                "color": "#721c24",
                "backgroundColor": "#f8d7da",
                "border": "1px solid #f5c6cb",
                "borderRadius": "4px",
                "padding": "16px",
                "margin": "20px",
                "whiteSpace": "pre-line",
                "fontFamily": "monospace"
            }
        ))

    children.append(dcc.Graph(id="lessons-per-day-graph", figure=figure))
    
    return html.Div(children, style={
        "maxWidth": "960px", 
        "margin": "0 auto", 
        "padding": "20px",
        "fontFamily": "Arial, sans-serif"
    })


app.layout = create_layout

application = app.server

if __name__ == "__main__":
    print(f"\n🌐 Запуск сервера на {HOST}:{PORT}")
    app.run_server(debug=DEBUG_MODE, host=HOST, port=PORT)