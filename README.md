# 🌙 Planner Lunar Integrativo

Planejador diário baseado nos ciclos da Lua.

O projeto organiza protocolos de alimentação, suplementação, exercícios, terapias e rotinas conforme a fase lunar e o dia da semana.

Os protocolos são mantidos em uma planilha Excel e importados para um banco SQLite otimizado para consulta por uma aplicação Streamlit.

---

# Objetivos

* Centralizar protocolos integrativos.
* Facilitar a consulta diária.
* Organizar a rotina de acordo com o ciclo lunar.
* Manter uma única fonte de verdade (Excel).

---

# Arquitetura

```text
Calendario_Lunar_Integrativo.xlsx
                │
                ▼
      scripts/import_excel.py
                │
                ▼
      database/protocolos.db
                │
                ▼
          app/app.py
                │
                ▼
            Streamlit
```

---

# Estrutura do Projeto

```text
protocolos_lunares/

├── app/
│   └── app.py
│
├── database/
│   ├── protocolos.db
│   ├── schema.sql
│   └── views.sql
│
├── data/
│   ├── Calendario_Lunar_Integrativo.xlsx
│   └── moon_calendar.json
│
├── scripts/
│   ├── create_database.py
│   └── import_excel.py
│
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── DATABASE_SCHEMA.md
│   └── DECISIONS.md
│
├── requirements.txt
│
└── README.md
```

---

# Tecnologias

* Python 3.12+
* Streamlit
* SQLite
* OpenPyXL

---

# Instalação

Clone o repositório.

```bash
git clone https://github.com/SEU_USUARIO/protocolos_lunares.git
```

Entre na pasta.

```bash
cd protocolos_lunares
```

Crie um ambiente virtual.

```bash
python -m venv .venv
```

Ative o ambiente.

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Instale as dependências.

```bash
pip install -r requirements.txt
```

---

# Criando o banco

Execute apenas uma vez.

```bash
python scripts/create_database.py
```

---

# Atualizando os protocolos

Sempre que a planilha Excel for alterada:

```bash
python scripts/import_excel.py
```

O banco SQLite será atualizado automaticamente.

---

# Executando a aplicação

```bash
streamlit run app/app.py
```

A aplicação será aberta em:

```
http://localhost:8501
```

---

# Publicação no Streamlit Community Cloud

O projeto é compatível com o Streamlit Community Cloud.

Fluxo recomendado:

```text
Excel

↓

import_excel.py

↓

SQLite

↓

Git Commit

↓

Git Push

↓

Deploy Automático
```

---

# Funcionalidades

## V2.1

* Visualização diária
* Visualização semanal
* Consulta por fase lunar
* Objetivos da fase
* Nutrição da fase
* Protocolos por período

---

# Banco de Dados

Banco relacional SQLite.

Principais entidades:

* Phase
* Weekday
* Period
* Item
* ItemType
* ProtocolItem
* MoonCalendar

Consulte:

```
docs/DATABASE_SCHEMA.md
```

---

# Documentação

O projeto possui documentação completa.

* PRD.md
* ARCHITECTURE.md
* DATABASE_SCHEMA.md
* DECISIONS.md

---

# Fluxo de Atualização

```text
Editar Excel

↓

Executar import_excel.py

↓

SQLite atualizado

↓

Executar Streamlit
```

ou

```text
Git Push

↓

Deploy automático no Streamlit Cloud
```

---

# Roadmap

## V2

* ✅ Visualização diária
* ✅ Visualização semanal
* ✅ Visualização por fase lunar

## V3

* Biblioteca de protocolos
* Dashboard estatístico
* Histórico de alterações
* Exportação PDF

---

# Licença

Uso pessoal e educacional.
