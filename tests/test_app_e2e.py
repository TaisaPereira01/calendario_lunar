"""
E2E via `streamlit.testing.v1.AppTest` (sem browser).

Loga por bypass de sessão (o `st.form` do login não é dirigível por automação) e
exercita a aba **Hoje** **sem** a config `[diario]` — ou seja, com o checklist
indisponível. Prova o isolamento (T-010 / AC-CHECK): a aba Hoje ainda lista o
protocolo, com aviso, sem derrubar o app.
"""

from pathlib import Path

import streamlit_authenticator as stauth
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app" / "app.py")


def _logged_in_app():
    at = AppTest.from_file(APP)
    at.secrets["auth"] = {
        "usuario": "t",
        "nome": "T",
        "senha_hash": stauth.Hasher.hash("x"),
        "cookie_name": "c",
        "cookie_key": "chave_longa_de_teste_123",
        "cookie_expiry_days": 30,
    }
    # Sem [diario] de propósito: recursos de nuvem indisponíveis (degradação).
    at.run(timeout=30)
    at.session_state["authentication_status"] = True
    at.session_state["name"] = "T"
    at.run(timeout=30)
    return at


def test_app_loga_e_mostra_as_4_views():
    at = _logged_in_app()
    assert not at.exception
    assert list(at.radio[0].options) == [
        "🏠 Hoje", "📅 Semana", "🌙 Fase Lunar", "📓 Diário",
    ]


def test_hoje_isola_falha_do_checklist():
    """T-010 / AC-CHECK: checklist indisponível → aviso + protocolo ainda renderiza."""
    at = _logged_in_app()
    assert not at.exception
    warns = [w.value for w in at.warning]
    assert any("checklist" in w.lower() for w in warns), warns
    md = " ".join(m.value for m in at.markdown)
    assert any(x in md for x in ("Rotina", "Café", "Almoço", "💊", "🥗")), "protocolo não renderizou"
