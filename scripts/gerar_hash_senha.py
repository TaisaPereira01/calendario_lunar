"""
Gera o hash bcrypt de uma senha, para colar em `.streamlit/secrets.toml`.

Uso:
    python scripts/gerar_hash_senha.py

A senha é digitada de forma OCULTA e nunca é gravada em lugar nenhum —
só o hash (irreversível) é impresso na tela.
"""

from getpass import getpass

import streamlit_authenticator as stauth


def main():

    senha = getpass("Digite a senha para o Planner Lunar: ")

    if not senha:

        print("Senha vazia não é permitida.")

        return

    if senha != getpass("Confirme a senha: "):

        print("As senhas não conferem. Rode de novo.")

        return

    print()
    print("Cole esta linha na seção [auth] de .streamlit/secrets.toml:")
    print()
    print(f'senha_hash = "{stauth.Hasher.hash(senha)}"')


if __name__ == "__main__":

    main()
