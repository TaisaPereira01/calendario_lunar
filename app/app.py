"""
Planner Lunar Integrativo
Versão 2.1

Aplicação Streamlit
"""

from pathlib import Path
from datetime import date
import sqlite3

import streamlit as st


# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

ROOT = Path(__file__).resolve().parents[1]

DATABASE = ROOT / "database" / "protocolos.db"


st.set_page_config(
    page_title="Planner Lunar Integrativo",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# SQLITE
# =============================================================================

@st.cache_resource
def get_connection():

    conn = sqlite3.connect(
        DATABASE,
        check_same_thread=False,
    )

    conn.row_factory = sqlite3.Row

    return conn


db = get_connection()


# =============================================================================
# MODOS DE VISUALIZAÇÃO
# =============================================================================

VIEW_TODAY = "🏠 Hoje"

VIEW_WEEK = "📅 Semana"

VIEW_PHASE = "🌙 Fase Lunar"


# =============================================================================
# ÍCONES
# =============================================================================

PERIOD_ICONS = {

    "Rotina Matinal": "☀️",

    "Café da Manhã": "🥣",

    "Suplementos Manhã": "💊",

    "Almoço": "🥗",

    "Suplementos Tarde": "💊",

    "Lanche": "🍎",

    "Jantar": "🍲",

    "Antes de Dormir": "🌙",

    "Exercício": "🏃",

    "Terapias": "♨️",

}


# =============================================================================
# CSS
# =============================================================================

def load_css(color):

    st.markdown(
f"""
<style>

.block-container{{

    max-width:1050px;

    padding-top:1.5rem;

    padding-bottom:3rem;

}}

.period-card{{

    background:#1E1F25;

    border:1px solid #31333F;

    border-left:6px solid {color};

    border-radius:12px;

    padding:18px;

    margin-bottom:18px;

}}

.protocol-line{{

    padding:8px 0;

    border-bottom:1px solid #31333F;

}}

.protocol-line:last-child{{

    border-bottom:none;

}}

.protocol-note{{

    color:#AAAAAA;

    margin-left:28px;

    font-size:.85rem;

}}

.footer{{

    color:#888888;

    text-align:center;

}}

</style>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# SQL
# =============================================================================

SQL_PHASE = """

SELECT

    phase_id,

    phase_name,

    objective,

    nutrition,

    color

FROM vw_calendar

WHERE date = ?

"""


SQL_PROTOCOL_DAY = """

SELECT

    weekday_id,

    weekday_name,

    period_name,

    item_name,

    icon,

    value,

    notes,

    period_order,

    display_order

FROM vw_protocol

WHERE

    phase_id = ?

AND

    weekday_id = ?

ORDER BY

    period_order,

    display_order

"""


SQL_PROTOCOL_WEEK = """

SELECT

    weekday_id,

    weekday_name,

    period_name,

    item_name,

    icon,

    value,

    notes,

    period_order,

    display_order

FROM vw_protocol

WHERE

    phase_id = ?

ORDER BY

    weekday_id,

    period_order,

    display_order

"""


# =============================================================================
# BANCO
# =============================================================================

def get_phase(selected_date):

    return db.execute(

        SQL_PHASE,

        (

            selected_date.isoformat(),

        ),

    ).fetchone()


def get_protocol_day(

    phase_id,

    weekday_id,

):

    return db.execute(

        SQL_PROTOCOL_DAY,

        (

            phase_id,

            weekday_id,

        ),

    ).fetchall()


def get_protocol_week(

    phase_id,

):

    return db.execute(

        SQL_PROTOCOL_WEEK,

        (

            phase_id,

        ),

    ).fetchall()


# =============================================================================
# HELPERS
# =============================================================================

def format_date(d):

    months = [

        "Janeiro",

        "Fevereiro",

        "Março",

        "Abril",

        "Maio",

        "Junho",

        "Julho",

        "Agosto",

        "Setembro",

        "Outubro",

        "Novembro",

        "Dezembro",

    ]

    return f"{d.day} de {months[d.month-1]} de {d.year}"


def get_weekday_id(selected_date):

    """
    Segunda = 1
    Domingo = 7
    """

    return selected_date.weekday() + 1


def group_by_period(rows):

    periods = {}

    for row in rows:

        periods.setdefault(

            row["period_name"],

            []

        ).append(row)

    return periods

# =============================================================================
# COMPONENTES
# =============================================================================

def render_sidebar():
    """
    Sidebar principal.
    """

    st.sidebar.title("🌙 Planner Lunar")

    selected_date = st.sidebar.date_input(
        "Selecione a data",
        value=date.today(),
        format="DD/MM/YYYY",
    )

    st.sidebar.divider()

    view = st.sidebar.radio(
        "Visualização",
        (
            VIEW_TODAY,
            VIEW_WEEK,
            VIEW_PHASE,
        ),
    )

    st.sidebar.divider()

    st.sidebar.markdown("### Legenda")

    for period, icon in PERIOD_ICONS.items():

        st.sidebar.markdown(
            f"{icon} {period}"
        )

    st.sidebar.divider()

    st.sidebar.caption(
        "Planner Lunar Integrativo"
    )

    return selected_date, view


# =============================================================================

def render_header(
    phase,
    selected_date,
):
    """
    Cabeçalho da página.
    """

    load_css(
        phase["color"]
    )

    st.title(
        f"🌙 {phase['phase_name']}"
    )

    st.caption(
        format_date(
            selected_date
        )
    )

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("🎯 Objetivo")

            st.write(
                phase["objective"] or "-"
            )

        with col2:

            st.subheader("🥗 Nutrição")

            st.write(
                phase["nutrition"] or "-"
            )

    st.write("")


# =============================================================================

def render_period_card(
    period_name,
    items,
):
    """
    Exibe um período completo.
    """

    icon = PERIOD_ICONS.get(
        period_name,
        "📌",
    )

    html = []

    html.append(
        '<div class="period-card">'
    )

    html.append(
        f"<h3>{icon} {period_name}</h3>"
    )

    for row in items:

        line = f"{row['icon']} {row['item_name']}"

        if row["value"]:

            line += f" ({row['value']})"

        html.append(
            f'<div class="protocol-line">{line}</div>'
        )

        if row["notes"]:

            html.append(

                f'<div class="protocol-note">{row["notes"]}</div>'

            )

    html.append("</div>")

    st.markdown(

        "".join(html),

        unsafe_allow_html=True,

    )


# =============================================================================

def render_day(rows):
    """
    Exibe todos os períodos do dia.
    """

    if not rows:

        st.info(
            "Nenhum protocolo encontrado."
        )

        return

    grouped = group_by_period(rows)

    for period_name, items in grouped.items():

        render_period_card(

            period_name,

            items,

        )


# =============================================================================

def render_footer():

    st.divider()

    st.caption(

        "🌙 Planner Lunar Integrativo • Streamlit • SQLite"

    )

# =============================================================================
# VIEWS
# =============================================================================

def view_today(
    phase,
    selected_date,
):
    """
    Exibe o protocolo do dia selecionado.
    """

    rows = get_protocol_day(

        phase["phase_id"],

        get_weekday_id(selected_date),

    )

    render_day(rows)


# =============================================================================

def view_week(
    phase,
    selected_date,
):
    """
    Exibe todos os dias da semana.
    """

    rows = get_protocol_week(

        phase["phase_id"]

    )

    if not rows:

        st.info(
            "Nenhum protocolo encontrado."
        )

        return

    days = {

        1: ("Segunda-feira", []),

        2: ("Terça-feira", []),

        3: ("Quarta-feira", []),

        4: ("Quinta-feira", []),

        5: ("Sexta-feira", []),

        6: ("Sábado", []),

        7: ("Domingo", []),

    }

    for row in rows:

        days[row["weekday_id"]][1].append(row)

    today = get_weekday_id(

        selected_date

    )

    for weekday in range(1, 8):

        title, day_rows = days[weekday]

        with st.expander(

            title,

            expanded=(weekday == today),

        ):

            render_day(day_rows)


# =============================================================================

def view_phase(
    phase,
    selected_date,
):
    """
    Placeholder da V2.2
    """

    st.info(

        "Visualização por Fase Lunar será implementada na V2.2."

    )


# =============================================================================
# DISPATCHER
# =============================================================================

def show_view(

    view,

    phase,

    selected_date,

):

    if view == VIEW_TODAY:

        view_today(

            phase,

            selected_date,

        )

        return

    if view == VIEW_WEEK:

        view_week(

            phase,

            selected_date,

        )

        return

    if view == VIEW_PHASE:

        view_phase(

            phase,

            selected_date,

        )

        return


# =============================================================================
# MAIN
# =============================================================================

def main():

    selected_date, view = render_sidebar()

    phase = get_phase(

        selected_date

    )

    if phase is None:

        st.error(

            "Nenhuma fase lunar encontrada para esta data."

        )

        return

    render_header(

        phase,

        selected_date,

    )

    show_view(

        view,

        phase,

        selected_date,

    )

    render_footer()


# =============================================================================

if __name__ == "__main__":

    main()

