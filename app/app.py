"""
Planner Lunar Integrativo
Versão 2.1

Aplicação Streamlit
"""

from pathlib import Path
from datetime import date
import sqlite3
import sys

import streamlit as st
import streamlit_authenticator as stauth

# Garante que app/ esteja no sys.path para importar o módulo local `diario` —
# tanto sob `streamlit run app/app.py` quanto sob testes, em qualquer CWD.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import diario  # noqa: E402  — módulo local (app/diario.py); import após ajustar sys.path


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
# AUTENTICAÇÃO
# =============================================================================

LOGIN_FIELDS = {

    "Form name": "🌙 Planner Lunar — Acesso",

    "Username": "Usuário",

    "Password": "Senha",

    "Login": "Entrar",

}


def build_authenticator():
    """
    Monta o autenticador a partir de .streamlit/secrets.toml (seção [auth]).

    A senha vive em hash (auto_hash=False) — nada de senha em texto no código
    nem no git. Retorna None se os segredos não estiverem configurados.
    """

    try:

        cfg = st.secrets["auth"]

    except Exception:

        # Sem .streamlit/secrets.toml (ou sem a seção [auth]).
        return None

    credentials = {

        "usernames": {

            cfg["usuario"]: {

                "name": cfg.get("nome", cfg["usuario"]),

                "password": cfg["senha_hash"],

            }

        }

    }

    return stauth.Authenticate(

        credentials,

        cfg["cookie_name"],

        cfg["cookie_key"],

        cfg.get("cookie_expiry_days", 30),

        auto_hash=False,

    )


# =============================================================================
# MODOS DE VISUALIZAÇÃO
# =============================================================================

VIEW_TODAY = "🏠 Hoje"

VIEW_WEEK = "📅 Semana"

VIEW_PHASE = "🌙 Fase Lunar"

VIEW_DIARY = "📓 Diário"


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


def get_phases():
    """
    Todas as fases ativas (para a view Fase Lunar — RF-014).
    """

    return db.execute(

        "SELECT id, name, objective, nutrition, color "
        "FROM phase WHERE active = 1 ORDER BY id"

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
            VIEW_DIARY,
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

def render_week_days(rows, expanded_weekday):
    """
    Renderiza os 7 dias da semana em seções expansíveis, abrindo `expanded_weekday`.
    Reutilizado pela view Semana e pela view Fase Lunar.
    """

    if not rows:

        st.info("Nenhum protocolo encontrado.")

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

    for weekday in range(1, 8):

        title, day_rows = days[weekday]

        with st.expander(

            title,

            expanded=(weekday == expanded_weekday),

        ):

            render_day(day_rows)


# =============================================================================

def view_week(
    phase,
    selected_date,
):
    """
    Exibe todos os dias da semana.
    """

    rows = get_protocol_week(phase["phase_id"])

    render_week_days(rows, get_weekday_id(selected_date))


# =============================================================================

def view_phase(selected_date):
    """
    View Fase Lunar (RF-014): escolher uma das 4 fases e ver o protocolo completo
    dela (os 7 dias), sem depender de uma data. Leitura pura sobre o SQLite.
    """

    phases = get_phases()

    if not phases:

        st.info("Nenhuma fase cadastrada.")

        return

    names = [p["name"] for p in phases]

    # Default: a fase da data selecionada, se houver; senão a primeira.
    default_idx = 0

    atual = get_phase(selected_date)

    if atual is not None:

        for i, p in enumerate(phases):

            if p["name"] == atual["phase_name"]:

                default_idx = i

                break

    escolhida_nome = st.selectbox(
        "Escolha a fase",
        names,
        index=default_idx,
    )

    escolhida = next(p for p in phases if p["name"] == escolhida_nome)

    load_css(escolhida["color"])

    st.title(f"🌙 {escolhida['name']}")

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("🎯 Objetivo")

            st.write(escolhida["objective"] or "-")

        with col2:

            st.subheader("🥗 Nutrição")

            st.write(escolhida["nutrition"] or "-")

    st.write("")

    rows = get_protocol_week(escolhida["id"])

    render_week_days(rows, get_weekday_id(selected_date))


# =============================================================================

def view_diario(selected_date):
    """
    View Diário: escreve/edita a anotação de texto livre da data (RF-012).

    Isolada dos protocolos: uma falha do diário (rede/credencial/config) vira
    mensagem clara e NÃO derruba o app — os wrappers read_note_safe/
    write_note_safe nunca deixam exceção subir (T-007, ARCHITECTURE §6).
    """

    st.title("📓 Diário")

    st.caption(format_date(selected_date))

    atual, erro = diario.read_note_safe(st.secrets, selected_date)

    if erro is not None:

        st.error(
            "Não consegui acessar o diário agora. Verifique a configuração do "
            "Google Sheets (seção [diario] dos secrets — veja o README)."
        )

        st.caption(f"Detalhe técnico: {erro}")

        return

    texto = st.text_area(
        "Anotação do dia",
        value=atual,
        height=320,
        key=f"diario_{selected_date.isoformat()}",
        placeholder="Escreva aqui suas anotações do dia...",
    )

    if st.button("💾 Salvar", type="primary"):

        erro_save = diario.write_note_safe(
            st.secrets,
            selected_date,
            texto,
        )

        if erro_save is None:

            st.success("Anotação salva.")

        else:

            st.error("Não consegui salvar agora. Tente de novo em instantes.")

            st.caption(f"Detalhe técnico: {erro_save}")


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


# =============================================================================
# MAIN
# =============================================================================

def main():

    authenticator = build_authenticator()

    if authenticator is None:

        st.title("🌙 Planner Lunar Integrativo")

        st.error("Login ainda não configurado.")

        st.markdown(
            "Crie `.streamlit/secrets.toml` a partir de "
            "`.streamlit/secrets.toml.example` e gere sua senha com "
            "`python scripts/gerar_hash_senha.py`. Veja o README."
        )

        return

    authenticator.login(

        location="main",

        fields=LOGIN_FIELDS,

    )

    status = st.session_state.get("authentication_status")

    if status is False:

        st.error("Usuário ou senha incorretos.")

        return

    if status is None:

        st.info("Digite seu usuário e senha para entrar.")

        return

    # --- autenticada a partir daqui ---

    selected_date, view = render_sidebar()

    st.sidebar.divider()

    st.sidebar.caption(
        f"Logada como {st.session_state.get('name', '')}"
    )

    authenticator.logout(
        "Sair",
        location="sidebar",
    )

    # Diário é domínio próprio (não precisa de fase lunar): funciona em qualquer
    # data, inclusive fora do calendário carregado.
    if view == VIEW_DIARY:

        view_diario(selected_date)

        render_footer()

        return

    # Fase Lunar também é independente da data (a fase é escolhida manualmente).
    if view == VIEW_PHASE:

        view_phase(selected_date)

        render_footer()

        return

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

