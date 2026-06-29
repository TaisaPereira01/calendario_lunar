-- ============================================================================
-- Protocolos Lunares
-- schema.sql
--
-- Versão : 1.0
-- SQLite : 3.x
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ============================================================================
-- TABLE: phase
-- ============================================================================

CREATE TABLE IF NOT EXISTS phase (

    id              INTEGER PRIMARY KEY AUTOINCREMENT,

    name            TEXT NOT NULL UNIQUE,

    objective       TEXT,

    nutrition       TEXT,

    color           TEXT,

    active          INTEGER NOT NULL DEFAULT 1
                    CHECK(active IN (0,1))

);

-- ============================================================================
-- TABLE: weekday
-- ============================================================================

CREATE TABLE IF NOT EXISTS weekday (

    id              INTEGER PRIMARY KEY,

    name            TEXT NOT NULL UNIQUE,

    display_order   INTEGER NOT NULL UNIQUE,

    active          INTEGER NOT NULL DEFAULT 1
                    CHECK(active IN (0,1))

);

-- ============================================================================
-- TABLE: period
-- ============================================================================

CREATE TABLE IF NOT EXISTS period (

    id              INTEGER PRIMARY KEY,

    name            TEXT NOT NULL UNIQUE,

    display_order   INTEGER NOT NULL UNIQUE,

    active          INTEGER NOT NULL DEFAULT 1
                    CHECK(active IN (0,1))

);

-- ============================================================================
-- TABLE: item_type
-- ============================================================================

CREATE TABLE IF NOT EXISTS item_type (

    id              INTEGER PRIMARY KEY,

    name            TEXT NOT NULL UNIQUE,

    icon            TEXT,

    active          INTEGER NOT NULL DEFAULT 1
                    CHECK(active IN (0,1))

);

-- ============================================================================
-- TABLE: item
-- ============================================================================

CREATE TABLE IF NOT EXISTS item (

    id                  INTEGER PRIMARY KEY AUTOINCREMENT,

    item_type_id        INTEGER NOT NULL,

    name                TEXT NOT NULL,

    description         TEXT,

    active              INTEGER NOT NULL DEFAULT 1
                        CHECK(active IN (0,1)),

    CONSTRAINT fk_item_type
        FOREIGN KEY(item_type_id)
        REFERENCES item_type(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT uq_item
        UNIQUE(item_type_id, name)

);

-- ============================================================================
-- TABLE: protocol_item
-- ============================================================================

CREATE TABLE IF NOT EXISTS protocol_item (

    id                  INTEGER PRIMARY KEY AUTOINCREMENT,

    phase_id            INTEGER NOT NULL,

    weekday_id          INTEGER NOT NULL,

    period_id           INTEGER NOT NULL,

    item_id             INTEGER NOT NULL,

    display_order       INTEGER NOT NULL,

    value               TEXT,

    notes               TEXT,

    CONSTRAINT fk_phase
        FOREIGN KEY(phase_id)
        REFERENCES phase(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_weekday
        FOREIGN KEY(weekday_id)
        REFERENCES weekday(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_period
        FOREIGN KEY(period_id)
        REFERENCES period(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_item
        FOREIGN KEY(item_id)
        REFERENCES item(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT

);

-- ============================================================================
-- TABLE: moon_calendar
-- ============================================================================

CREATE TABLE IF NOT EXISTS moon_calendar (

    date            TEXT PRIMARY KEY,

    phase_id        INTEGER NOT NULL,

    CONSTRAINT fk_calendar_phase
        FOREIGN KEY(phase_id)
        REFERENCES phase(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT

);

-- ============================================================================
-- INDEXES
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_protocol_phase
ON protocol_item (phase_id);

CREATE INDEX IF NOT EXISTS idx_protocol_weekday
ON protocol_item (weekday_id);

CREATE INDEX IF NOT EXISTS idx_protocol_period
ON protocol_item (period_id);

CREATE INDEX IF NOT EXISTS idx_protocol_item
ON protocol_item (item_id);

CREATE INDEX IF NOT EXISTS idx_protocol_lookup
ON protocol_item
(
    phase_id,
    weekday_id,
    period_id,
    display_order
);

CREATE INDEX IF NOT EXISTS idx_calendar_date
ON moon_calendar(date);

CREATE INDEX IF NOT EXISTS idx_calendar_phase
ON moon_calendar(phase_id);

CREATE INDEX IF NOT EXISTS idx_item_name
ON item(name);

CREATE INDEX IF NOT EXISTS idx_item_type
ON item(item_type_id);


CREATE UNIQUE INDEX idx_protocol_unique
ON protocol_item
(
    phase_id,
    weekday_id,
    period_id,
    item_id
);

-- ============================================================================
-- END
-- ============================================================================