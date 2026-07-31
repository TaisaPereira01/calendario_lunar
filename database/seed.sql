-- ============================================================================
-- Protocolos Lunares
-- seed.sql
--
-- Versão : 1.0
-- SQLite : 3.x
--
-- Carga inicial das tabelas de referência (dados estáveis, não vêm do Excel).
--
-- Estas tabelas precisam existir ANTES de rodar scripts/import_excel.py,
-- pois o import resolve os nomes (fase, dia, período, tipo) para os ids
-- definidos aqui. Sem este seed, o import falha ao procurar as chaves.
--
-- Ordem de carga:
--     1. schema.sql   (cria as tabelas)
--     2. seed.sql     (popula as tabelas de referência)  <- este arquivo
--     3. views.sql    (cria as views)
--     4. import_excel.py  (popula item / protocol_item / moon_calendar)
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ============================================================================
-- phase
--
-- Os ids são fixos porque moon_calendar e protocol_item os referenciam.
-- ============================================================================

INSERT INTO phase (id, name, objective, nutrition, color, active) VALUES
    (1, 'Lua Nova',      'intestino • inflamação • eixo hormonal', 'FODMAP + anti-inflamatória + digestibilidade máxima', '#6A1B9A', 1),
    (2, 'Lua Crescente', 'energia • cabelo • massa magra',         'mais proteína + minerais',                           '#2E7D32', 1),
    (3, 'Lua Cheia',     'circulação • drenagem • prazer',         'leve + hidratante',                                  '#F9A825', 1),
    (4, 'Lua Minguante', 'articulações • recuperação',             'caldos + anti-inflamatório',                         '#1565C0', 1);

-- ============================================================================
-- weekday
--
-- Segunda = 1 ... Domingo = 7 (mesma convenção de get_weekday_id no app).
-- ============================================================================

INSERT INTO weekday (id, name, display_order, active) VALUES
    (1, 'segunda', 1, 1),
    (2, 'terça',   2, 1),
    (3, 'quarta',  3, 1),
    (4, 'quinta',  4, 1),
    (5, 'sexta',   5, 1),
    (6, 'sábado',  6, 1),
    (7, 'domingo', 7, 1);

-- ============================================================================
-- period
--
-- Ordem em que os períodos aparecem no dia.
-- ============================================================================

INSERT INTO period (id, name, display_order, active) VALUES
    (1,  'Rotina Matinal',    1,  1),
    (2,  'Café da Manhã',     2,  1),
    (3,  'Suplementos Manhã', 3,  1),
    (4,  'Almoço',            4,  1),
    (5,  'Suplementos Tarde', 5,  1),
    (6,  'Lanche',            6,  1),
    (7,  'Jantar',            7,  1),
    (8,  'Antes de Dormir',   8,  1),
    (9,  'Exercício',         9,  1),
    (10, 'Terapias',          10, 1);

-- ============================================================================
-- item_type
--
-- O nome (ROUTINE, FOOD, ...) é a chave usada por PERIODS em import_excel.py.
-- O icon é o emoji exibido ao lado de cada item no app.
-- ============================================================================

INSERT INTO item_type (id, name, icon, active) VALUES
    (1,  'ROUTINE',     '☀️', 1),
    (2,  'FOOD',        '🥗', 1),
    (3,  'DRINK',       '🥤', 1),
    (4,  'SUPPLEMENT',  '💊', 1),
    (5,  'EXERCISE',    '🏃', 1),
    (6,  'THERAPY',     '♨️', 1),
    (7,  'BREATHING',   '🫁', 1),
    (8,  'HABIT',       '🌱', 1),
    (9,  'SKINCARE',    '✨', 1),
    (10, 'OBSERVATION', '📝', 1);

-- ============================================================================
-- END
-- ============================================================================
