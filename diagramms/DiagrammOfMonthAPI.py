import os
from typing import Optional, Dict, Any, List

import requests
import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px
from datetime import datetime

NOCODB_URL: str = os.getenv("NOCODB_URL", "http://localhost:8080").rstrip('/')
NOCODB_TOKEN: Optional[str] = os.getenv("NOCODB_TOKEN", "h070wPAEcnvRUrqeXswZu-LP7HZqnqZCo5PQudOg")
NOCODB_TABLE: str = os.getenv("NOCODB_TABLE", "Lections") 
DATE_FIELD: str = os.getenv("DATE_FIELD", "lection_date")
TABLE_ID: Optional[str] = os.getenv("TABLE_ID", "m4i2yylgaqvy4m5")

API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
PAGE_SIZE: int = int(os.getenv("PAGE_SIZE", "100"))


def _build_nocodb_headers() -> Dict[str, str]:
    """
    Формирует заголовки для запроса к NocoDB API v2.
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    if NOCODB_TOKEN:
        headers["xc-token"] = NOCODB_TOKEN
    
    return headers


def _build_api_url(endpoint: str) -> str:
    """
    Формирует полный URL для API запроса.
    """
    return f"{NOCODB_URL}/api/v2/{endpoint.lstrip('/')}"


def get_table_id() -> Optional[str]:
    """
    Получает ID таблицы по её названию.
    """
    if TABLE_ID:
        return TABLE_ID
    
    try:
        url = _build_api_url("meta/tables")
        headers = _build_nocodb_headers()
        
        response = requests.get(url, headers=headers, timeout=API_TIMEOUT)
        
        if response.status_code == 200:
            tables = response.json()
            
            if isinstance(tables, list):
                for table in tables:
                    if table.get('title') == NOCODB_TABLE or table.get('table_name') == NOCODB_TABLE:
                        return table.get('id')
            
            # Если пришёл объект со списком
            if isinstance(tables, dict) and 'list' in tables:
                for table in tables['list']:
                    if table.get('title') == NOCODB_TABLE or table.get('table_name') == NOCODB_TABLE:
                        return table.get('id')
        
        print(f"⚠️ Таблица '{NOCODB_TABLE}' не найдена. Используем название как ID.")
        return NOCODB_TABLE
        
    except Exception as e:
        print(f"⚠️ Ошибка при получении ID таблицы: {e}")
        return NOCODB_TABLE


def fetch_lessons_from_nocodb() -> pd.DataFrame:
    """
    Получает данные о занятиях из NocoDB через API v2.
    
    Использует формат из примера:
    {
      "list": [...],
      "pageInfo": {...}
    }
    """
    
    table_id = get_table_id()
    
    url = _build_api_url(f"tables/{table_id}/records")
    
    headers = _build_nocodb_headers()
    
    params = {
        "limit": PAGE_SIZE,
        "fields": DATE_FIELD, 
        "sort": DATE_FIELD,      
    }
    
    print(f"\nПодключение к NocoDB API v2:")
    print(f"  URL: {url}")
    print(f"  Token: {'✓ установлен' if NOCODB_TOKEN else '✗ не установлен'}")
    print(f"  Table ID/Name: {table_id}")
    print(f"  Date field: {DATE_FIELD}")
    
    all_records = []
    page = 1
    
    try:
        while True:
            params["page"] = page
            params["offset"] = (page - 1) * PAGE_SIZE
            
            print(f"  Загрузка страницы {page}...")
            
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=API_TIMEOUT
            )
            
            if response.status_code == 401:
                raise RuntimeError("Ошибка авторизации. Проверьте API токен.")
            
            if response.status_code == 404:
                raise RuntimeError(f"Таблица '{table_id}' не найдена. Проверьте название таблицы.")
            
            if response.status_code != 200:
                raise RuntimeError(f"Ошибка API: {response.status_code} - {response.text[:200]}")
            
            data = response.json()
            
            if isinstance(data, dict):
                if "list" in data and isinstance(data["list"], list):
                    records = data["list"]
                    all_records.extend(records)
                    
                    page_info = data.get("pageInfo", {})
                    if not page_info.get("isLastPage", True):
                        page += 1
                        continue
                    else:
                        break
                elif isinstance(data, list):
                    all_records = data
                    break
                else:
                    all_records = [data]
                    break
            else:
                all_records = []
                break
            
    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"Не удалось подключиться к NocoDB по адресу {NOCODB_URL}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке данных: {e}")
    
    print(f" Всего загружено записей: {len(all_records)}")
    
    if not all_records:
        return pd.DataFrame()
    
    df = pd.DataFrame(all_records)
    print(f"  📊 Колонки в данных: {list(df.columns)}")
    
    return df


def aggregate_by_day(df: pd.DataFrame, date_field: str) -> pd.DataFrame:
    """
    Агрегирует количество занятий по дням месяца.
    
    Parameters:
    df: DataFrame с данными
    date_field: название поля с датой
    """
    if df.empty:
        return pd.DataFrame(columns=["day", "count"])

    if date_field not in df.columns:
        possible_fields = [col for col in df.columns if 'date' in col.lower()]
        if possible_fields:
            date_field_to_use = possible_fields[0]
            print(f"Поле '{date_field}' не найдено. Используем '{date_field_to_use}'")
        else:
            available_fields = list(df.columns)
            if 'created_at' in df.columns:
                print(f"Используем поле 'created_at' как дату")
                date_field_to_use = 'created_at'
            else:
                raise KeyError(
                    f"В данных отсутствует поле даты.\n"
                    f"Доступные поля: {available_fields}\n"
                    f"Укажите правильное имя поля"
                )
    else:
        date_field_to_use = date_field

    df = df.copy()
    
    try:
        df[date_field_to_use] = pd.to_datetime(df[date_field_to_use], errors="coerce")
    except Exception as e:
        print(f"Ошибка при конвертации дат: {e}")
        df[date_field_to_use] = pd.NaT
    
    df = df.dropna(subset=[date_field_to_use])
    print(f"Записей с корректными датами: {len(df)}")

    if df.empty:
        return pd.DataFrame(columns=["day", "count"])
    df["day"] = df[date_field_to_use].dt.day
    grouped = df.groupby("day").size().reset_index(name="count")
    grouped = grouped.sort_values("day").reset_index(drop=True)
    all_days = pd.DataFrame({"day": range(1, 32)})
    grouped = all_days.merge(grouped, on="day", how="left").fillna(0)
    grouped["count"] = grouped["count"].astype(int)
    days_with_data = len(grouped[grouped["count"] > 0])
    print(f"  📈 Дней с занятиями: {days_with_data}")
    print(f"  📊 Всего занятий: {grouped['count'].sum()}")
    
    return grouped


def build_figure(df_grouped: pd.DataFrame):
    """
    Строит график Plotly.
    """
    if df_grouped.empty or df_grouped["count"].sum() == 0:
        empty_df = pd.DataFrame({"day": [], "count": []})
        fig = px.bar(
            empty_df,
            x="day",
            y="count",
            labels={"day": "День месяца", "count": "Количество занятий"},
            title="Нет данных для отображения",
        )
        fig.update_layout(
            xaxis=dict(dtick=1, range=[0.5, 31.5]),
            yaxis=dict(range=[0, 1])
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

    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        textfont_size=10
    )

    fig.update_layout(
        xaxis=dict(
            dtick=1,
            title="День месяца",
            tickmode='linear',
            tick0=1,
            tickvals=list(range(1, 32))
        ),
        yaxis=dict(
            title="Количество занятий",
            tickmode='linear',
            tick0=0,
            dtick=1,
        ),
        hovermode='x unified',
        showlegend=False,
        plot_bgcolor='rgba(240, 240, 240, 0.5)',
    )

    return fig

app = dash.Dash(__name__)


def _create_layout():
    """
    Создает layout приложения.
    """
    error_message = None
    warning_message = None
    figure = None

    try:
        print("\n" + "=" * 60)
        print("🚀 ЗАПУСК ПРИЛОЖЕНИЯ С NocoDB API v2")
        print("=" * 60)
        lessons_df = fetch_lessons_from_nocodb()
        grouped_df = aggregate_by_day(lessons_df, DATE_FIELD)
        figure = build_figure(grouped_df)
        
        if lessons_df.empty:
            warning_message = "Таблица пуста. Добавьте данные в NocoDB."
        elif len(lessons_df) < 5:
            warning_message = "В таблице мало записей. Добавьте больше данных для статистики."
        else:
            print("График успешно построен!")
            
    except Exception as exc:
        print(f"Ошибка: {exc}")
        import traceback
        traceback.print_exc()
        
        error_message = (
            "Произошла ошибка при загрузке данных из NocoDB.\n\n"
            f"Детали: {str(exc)}\n\n"
            "Проверьте:\n"
            f"• Доступен ли NocoDB по адресу {NOCODB_URL}\n"
            f"• Правильно ли указан API токен\n"
            f"• Существует ли таблица '{NOCODB_TABLE}'\n"
            f"• Есть ли поле '{DATE_FIELD}' в таблице\n"
            f"• Доступные поля можно посмотреть в ответе API"
        )
        figure = build_figure(pd.DataFrame(columns=["day", "count"]))

    children = [
        html.H1("Количество занятий по дням месяца", 
                style={"textAlign": "center", "color": "#2E86AB", "marginBottom": "10px"}),
        html.P(
            "График показывает количество занятий по дням месяца на основе данных из NocoDB.",
            style={"textAlign": "center", "marginBottom": "30px", "color": "#666"}
        ),
    ]

    if warning_message:
        children.append(
            html.Div(
                warning_message,
                style={
                    "color": "#856404",
                    "backgroundColor": "#fff3cd",
                    "border": "1px solid #ffeeba",
                    "borderRadius": "4px",
                    "padding": "12px",
                    "marginBottom": "16px",
                    "textAlign": "center"
                },
            )
        )

    if error_message:
        children.append(
            html.Div(
                error_message,
                style={
                    "color": "#721c24",
                    "backgroundColor": "#f8d7da",
                    "border": "1px solid #f5c6cb",
                    "borderRadius": "4px",
                    "padding": "16px",
                    "marginBottom": "20px",
                    "whiteSpace": "pre-line",
                    "fontFamily": "monospace"
                },
            )
        )

    children.append(dcc.Graph(id="lessons-per-day-graph", figure=figure))
    
    children.append(
        html.Div(
            [
                html.Hr(),
                html.Details([
                    html.Summary("Информация о подключении к NocoDB", 
                               style={"cursor": "pointer", "color": "#666"}),
                    html.Div([
                        html.P(f"URL: {NOCODB_URL}"),
                        html.P(f"Table: {NOCODB_TABLE}"),
                        html.P(f"Date field: {DATE_FIELD}"),
                        html.P(f"Token: {'Установлен' if NOCODB_TOKEN else 'Не установлен'}"),
                    ], style={
                        "backgroundColor": "#f8f9fa", 
                        "padding": "15px", 
                        "borderRadius": "4px",
                        "marginTop": "10px",
                        "fontFamily": "monospace"
                    })
                ])
            ],
            style={"marginTop": "30px"}
        )
    )

    return html.Div(children, style={
        "maxWidth": "960px", 
        "margin": "0 auto", 
        "padding": "20px",
        "fontFamily": "Arial, sans-serif"
    })


app.layout = _create_layout

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 Запуск Dash приложения с NocoDB API v2")
    print("=" * 60)
    if not NOCODB_TOKEN:
        print("\nAPI токен не установлен!")
        print("   Укажите NOCODB_TOKEN в переменных окружения или в коде")
        print("   Получить токен: Account Settings → API Tokens\n")
    
    print("\nНастройки:")
    print(f"   URL: {NOCODB_URL}")
    print(f"   Таблица: {NOCODB_TABLE}")
    print(f"   Поле даты: {DATE_FIELD}")
    print("=" * 60 + "\n")
    app.run_server(debug=True, host="0.0.0.0", port=8050)