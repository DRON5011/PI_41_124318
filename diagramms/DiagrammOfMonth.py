import os
from typing import Optional

import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine 

PG_HOST: str = os.getenv("PG_HOST", "localhost")  
PG_PORT: str = os.getenv("PG_PORT", "5432")       
PG_DATABASE: str = os.getenv("PG_DATABASE", "VKR_Database")   
PG_USER: str = os.getenv("PG_USER", "postgres")          
PG_PASSWORD: str = os.getenv("PG_PASSWORD", "22082004")   

TABLE_NAME: str = os.getenv("PG_TABLE", "Lections")

DATE_FIELD: str = os.getenv("PG_DATE_FIELD", "lection_date")

FILTER_CONDITION: Optional[str] = os.getenv("PG_FILTER", None) 


def _build_connection_string() -> str:
    """
    Формирует строку подключения к PostgreSQL.
    """
    if not all([PG_DATABASE, PG_USER, PG_PASSWORD]):
        raise RuntimeError(
            "Не заданы обязательные переменные окружения: "
            "PG_DATABASE, PG_USER, PG_PASSWORD"
        )
    
    return f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"


def get_db_connection():
    """
    Создает и возвращает подключение к PostgreSQL.
    """
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            database=PG_DATABASE,
            user=PG_USER,
            password=PG_PASSWORD,
            cursor_factory=RealDictCursor 
        )
        return conn
    except Exception as e:
        raise RuntimeError(f"Ошибка подключения к PostgreSQL: {e}")


def fetch_lessons() -> pd.DataFrame:
    """
    Получает данные о занятиях из PostgreSQL и возвращает их в виде pandas.DataFrame.
    """
    connection_string = _build_connection_string()
    
    try:
        engine = create_engine(connection_string)
        
        base_query = f'''
        SELECT 
            "{DATE_FIELD}"
        FROM 
            "{TABLE_NAME}"
        '''
        
        if FILTER_CONDITION:
            base_query += f" WHERE {FILTER_CONDITION}"
        
        base_query += f' ORDER BY "{DATE_FIELD}"'
        
        print(f"Выполняется запрос:\n{base_query}") 
        
        df = pd.read_sql_query(base_query, engine)
        
        engine.dispose()
        print(f"Загружено записей: {len(df)}")  
        return df
        
    except Exception as e:
        raise RuntimeError(f"Ошибка при получении данных из PostgreSQL: {e}")


def fetch_lessons_with_cursor() -> pd.DataFrame:
    """
    Альтернативный метод получения данных с использованием psycopg2 cursor.
    Может быть полезен, если SQLAlchemy не подходит.
    """
    conn = get_db_connection()
    
    try:
        query = f"""
        SELECT 
            {DATE_FIELD}
        FROM 
            {TABLE_NAME}
        """
        
        if FILTER_CONDITION:
            query += f" WHERE {FILTER_CONDITION}"
        
        query += f" ORDER BY {DATE_FIELD}"
        
        df = pd.read_sql_query(query, conn)
        return df
        
    finally:
        conn.close()


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
            f"Проверьте имя поля или задайте переменную окружения PG_DATE_FIELD."
        )

    df = df.copy()
    df[DATE_FIELD] = pd.to_datetime(df[DATE_FIELD], errors="coerce")
    df = df.dropna(subset=[DATE_FIELD])

    if df.empty:
        return pd.DataFrame(columns=["day", "count"])

    df["day"] = df[DATE_FIELD].dt.day

    grouped = df.groupby("day").size().reset_index(name="count")
    grouped = grouped.sort_values("day").reset_index(drop=True)
    
    all_days = pd.DataFrame({"day": range(1, 32)})
    grouped = all_days.merge(grouped, on="day", how="left").fillna(0)
    grouped["count"] = grouped["count"].astype(int)
    
    return grouped


def build_figure(df_grouped: pd.DataFrame):
    """
    Строит график Plotly (столбчатая диаграмма) зависимости количества занятий от дня месяца.
    ИСПРАВЛЕНО: корректная обработка пустого DataFrame
    """
    if df_grouped.empty or df_grouped["count"].sum() == 0:
        empty_df = pd.DataFrame({
            "day": [],
            "count": []
        })
        fig = px.bar(
            empty_df,
            x="day",
            y="count",
            labels={"day": "День месяца", "count": "Количество занятий"},
            title="Нет данных для отображения",
        )
        fig.update_layout(
            xaxis=dict(
                dtick=1,
                range=[0.5, 31.5] 
            ),
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
    )

    fig.update_traces(
        texttemplate='%{y}', 
        textposition='outside',
        textfont_size=10
    )

    fig.update_layout(
        xaxis=dict(
            dtick=1,
            title="День месяца",
            tickmode='linear',
            tick0=1,
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


def get_database_info() -> dict:
    """
    Получает информацию о базе данных (для отладки и информации).
    """
    conn = get_db_connection()
    info = {}
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            info["version"] = cur.fetchone()["version"]
            
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = cur.fetchall()
            info["tables"] = [t["table_name"] for t in tables]
            
            info["target_table_exists"] = TABLE_NAME in info["tables"]
            
            if info["target_table_exists"]:
                cur.execute(f"""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = '{TABLE_NAME}'
                """)
                columns = cur.fetchall()
                info["table_columns"] = {c["column_name"]: c["data_type"] for c in columns}
                
                info["date_field_exists"] = DATE_FIELD in info["table_columns"]
    
    finally:
        conn.close()
    
    return info

app = dash.Dash(__name__)


def _create_layout():
    """
    Создает layout приложения, загружая данные из PostgreSQL и строя график.
    """
    error_message = None
    warning_message = None
    figure = None
    db_info = None

    try:
        lessons_df = fetch_lessons()
        print(f"Загружено записей: {len(lessons_df)}") 
        
        grouped_df = aggregate_by_day(lessons_df)
        print(f"Сгруппировано по дням: {len(grouped_df)}") 
        
        figure = build_figure(grouped_df)
        
        if not lessons_df.empty and len(lessons_df) < 5:
            warning_message = "Найдено мало записей. Убедитесь, что в таблице достаточно данных."
            
    except Exception as exc:
        print(f"Ошибка при подготовке данных для диаграммы: {exc}")
        import traceback
        traceback.print_exc() 
        
        error_message = (
            "Произошла ошибка при загрузке данных из PostgreSQL.\n"
            f"Детали: {str(exc)}\n\n"
            "Проверьте:\n"
            "• Запущен ли контейнер с PostgreSQL\n"
            "• Правильность параметров подключения (host, port, database, user, password)\n"
            f"• Существует ли таблица '{TABLE_NAME}'\n"
            f"• Есть ли поле '{DATE_FIELD}' в таблице\n"
            "• Установлены ли все зависимости: pip install sqlalchemy psycopg2-binary"
        )
        figure = build_figure(pd.DataFrame(columns=["day", "count"]))

    children = [
        html.H1("Диаграмма занятий по дням месяца", style={"textAlign": "center"}),
        html.P(
            "График показывает количество занятий по дням месяца на основе данных из PostgreSQL.",
            style={"textAlign": "center", "marginBottom": "30px"}
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
                    html.Summary("Информация о подключении", style={"cursor": "pointer"}),
                    html.Div([
                        html.P(f"Хост: {PG_HOST}:{PG_PORT}"),
                        html.P(f"База данных: {PG_DATABASE}"),
                        html.P(f"Таблица: {TABLE_NAME}"),
                        html.P(f"Поле даты: {DATE_FIELD}"),
                    ], style={"backgroundColor": "#f5f5f5", "padding": "10px", "borderRadius": "4px"})
                ])
            ],
            style={"marginTop": "30px"}
        )
    )

    return html.Div(children, style={"maxWidth": "960px", "margin": "0 auto", "padding": "20px"})


app.layout = _create_layout

if __name__ == "__main__":
    print("=" * 50)
    print("Запуск Dash приложения с подключением к PostgreSQL")
    print("=" * 50)
    print(f"Параметры подключения:")
    print(f"  Хост: {PG_HOST}:{PG_PORT}")
    print(f"  База данных: {PG_DATABASE}")
    print(f"  Таблица: {TABLE_NAME}")
    print(f"  Поле даты: {DATE_FIELD}")
    print("=" * 50)
    
    try:
        import sqlalchemy
        print(f"SQLAlchemy установлен (версия {sqlalchemy.__version__})")
    except ImportError:
        print("SQLAlchemy не установлен! Установите: pip install sqlalchemy")
    
    if not all([PG_DATABASE, PG_USER, PG_PASSWORD]):
        print("\nВНИМАНИЕ: Не все обязательные параметры заданы!")
        print("Установите переменные окружения или отредактируйте код:")
        print("  PG_DATABASE - название базы данных")
        print("  PG_USER - имя пользователя")
        print("  PG_PASSWORD - пароль")
        print("=" * 50)
    
    app.run_server(debug=True, host="0.0.0.0", port=8050)