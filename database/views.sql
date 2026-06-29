-- ============================================================================
-- Protocolos Lunares
-- views.sql
--
-- Versão : 1.0
-- SQLite : 3.x
-- ============================================================================

-- ============================================================================
-- VIEW: vw_protocol
--
-- Retorna o protocolo completo organizado por:
--
-- Fase
-- ↓
-- Dia da Semana
-- ↓
-- Período
-- ↓
-- Ordem de Exibição
-- ============================================================================

DROP VIEW IF EXISTS vw_protocol;

CREATE VIEW vw_protocol AS

SELECT

    p.id                AS phase_id,
    p.name              AS phase_name,
    p.objective,
    p.nutrition,
    p.color,

    w.id                AS weekday_id,
    w.name              AS weekday_name,
    w.display_order     AS weekday_order,

    pe.id               AS period_id,
    pe.name             AS period_name,
    pe.display_order    AS period_order,

    it.id               AS item_id,
    it.name             AS item_name,
    it.description,

    tp.id               AS item_type_id,
    tp.name             AS item_type,
    tp.icon,

    pi.value,
    pi.notes,
    pi.display_order

FROM protocol_item pi

INNER JOIN phase p
    ON p.id = pi.phase_id

INNER JOIN weekday w
    ON w.id = pi.weekday_id

INNER JOIN period pe
    ON pe.id = pi.period_id

INNER JOIN item it
    ON it.id = pi.item_id

INNER JOIN item_type tp
    ON tp.id = it.item_type_id

WHERE

    p.active = 1
AND
    w.active = 1
AND
    pe.active = 1
AND
    it.active = 1
AND
    tp.active = 1

ORDER BY

    p.id,
    w.display_order,
    pe.display_order,
    pi.display_order;



-- ============================================================================
-- VIEW: vw_calendar
--
-- Relaciona cada data com sua fase lunar.
-- ============================================================================

DROP VIEW IF EXISTS vw_calendar;

CREATE VIEW vw_calendar AS

SELECT

    mc.date,

    p.id            AS phase_id,

    p.name          AS phase_name,

    p.objective,

    p.nutrition,

    p.color

FROM moon_calendar mc

INNER JOIN phase p

    ON p.id = mc.phase_id

WHERE

    p.active = 1

ORDER BY

    mc.date;


-- ============================================================================
-- END
-- ============================================================================