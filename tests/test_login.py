"""
Testes do contrato de autenticação (login local — RF-010, DEC-015/DEC-016).

Não dirige a UI (o `st.form` do Streamlit não é testável por automação de browser).
Valida o contrato de que o app depende: credenciais montadas como em
`app.build_authenticator` (senha em **hash**, `auto_hash=False`) autenticam a senha
correta e rejeitam a errada. Trava regressão de upgrade da lib (pino `>=0.4,<0.5`).
"""

import streamlit_authenticator as stauth


def _authenticator(usuario, nome, senha_plana):
    """Espelha `app.build_authenticator`: monta credenciais com a senha em HASH."""

    credentials = {
        "usernames": {
            usuario: {
                "name": nome,
                "password": stauth.Hasher.hash(senha_plana),
            }
        }
    }

    return stauth.Authenticate(
        credentials,
        "cookie_teste",
        "chave_teste",
        30,
        auto_hash=False,
    )


def _check(auth, usuario, senha):
    return (
        auth.authentication_controller
        .authentication_model
        .check_credentials(usuario, senha)
    )


def test_senha_correta_autentica():
    auth = _authenticator("taisa", "Taisa", "minha_senha_forte")
    assert _check(auth, "taisa", "minha_senha_forte") is True


def test_senha_errada_rejeita():
    auth = _authenticator("taisa", "Taisa", "minha_senha_forte")
    assert _check(auth, "taisa", "outra_coisa") is False


def test_usuario_inexistente_rejeita():
    auth = _authenticator("taisa", "Taisa", "minha_senha_forte")
    assert _check(auth, "fulano", "minha_senha_forte") is False


def test_hash_nunca_guarda_a_senha_em_texto():
    h = stauth.Hasher.hash("senha123")
    assert h != "senha123"
    assert h.startswith("$2")  # bcrypt
    assert stauth.Hasher.check_pw("senha123", h) is True
