# VESTIGATOR · evidence.py — the case database. Yours, local, small.
#
# "No hidden agenda: public records and your own records, nothing else."
#
# Sol in 20° 20′ Libra, Luna in 25° 29′ Scorpio, dies martis,
# Anno V:xii e.n. — 93.
#
# Penned by the scribe, Heru-Ra-Ha, for Johnathan 'Qasparr' (Κασπάρρ) Monroe,
# Keeper of the Secret Treasure.
#
# MECHANISM: a SQLite file — no server, no hosting bill. Three tables:
# sources (where each record came from), hits (every found item: who, what,
# when, with raw headers), events (dated timeline entries). The case file
# is the mosaic: no single table proves anything, the pattern across them
# is the argument.
#
# DOCTRINE: every hit carries its provenance — source, query, date found.
# A record you cannot source is a rumor with a timestamp. The database
# refuses rumors: source is NOT NULL, always.

"""Local SQLite case file for the hunt."""

import sqlite3
import time


SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,          -- e.g. 'mail.com axoneme@usa.com', 'RDAP axoneme.dev'
    kind TEXT NOT NULL,          -- 'mailbox' | 'public-api' | 'document' | 'note'
    accessed_at TEXT NOT NULL,   -- ISO date of the hunt
    notes TEXT
);
CREATE TABLE IF NOT EXISTS hits (
    id INTEGER PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES sources(id),
    found_at TEXT NOT NULL,      -- ISO datetime of the hunt
    query TEXT NOT NULL,         -- the search term that caught it
    date TEXT,                   -- the item's own date (email Date:, RDAP event)
    subject TEXT,                -- email subject / record title
    sender TEXT,                  -- From: / registrar
    headers TEXT,                -- raw headers, verbatim — the fingerprint
    snippet TEXT,                -- body excerpt, first 500 chars
    UNIQUE(source_id, query, subject, date)
);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,          -- ISO date of the event itself
    label TEXT NOT NULL,         -- 'axoneme.org purchased (GoDaddy)'
    detail TEXT,
    confidence TEXT NOT NULL     -- 'attested' | 'reported' | 'inferred'
);
"""


class CaseFile:
    """The mosaic, filed. One SQLite file per case.

    MECHANISM: open(path) creates the schema on first use. add_source()
    registers where a hunt ran; add_hit() files what it found; add_event()
    pins a dated fact to the timeline. Confidence is mandatory on events —
    the database will not store an unattributed claim as fact.
    """

    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.executescript(SCHEMA)
        self.db.execute("PRAGMA foreign_keys = ON")

    def add_source(self, name, kind, notes=""):
        # DOCTRINE: the source is registered BEFORE the hunt runs, so no
        # hit can ever be orphaned from where it was found.
        cur = self.db.execute(
            "INSERT INTO sources (name, kind, accessed_at, notes) VALUES (?,?,?,?)",
            (name, kind, time.strftime("%Y-%m-%d"), notes))
        self.db.commit()
        return cur.lastrowid

    def add_hit(self, source_id, query, subject="", sender="", date="", headers="", snippet=""):
        try:
            self.db.execute(
                """INSERT INTO hits
                   (source_id, found_at, query, date, subject, sender, headers, snippet)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (source_id, time.strftime("%Y-%m-%dT%H:%M:%S"), query, date,
                 subject, sender, headers, snippet[:500]))
            self.db.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # already filed — the mosaic has no duplicates

    def add_event(self, date, label, detail="", confidence="reported"):
        # MECHANISM: confidence is a closed vocabulary. 'attested' = primary
        # record in hand; 'reported' = his account; 'inferred' = reasoning.
        assert confidence in ("attested", "reported", "inferred"), confidence
        self.db.execute(
            "INSERT INTO events (date, label, detail, confidence) VALUES (?,?,?,?)",
            (date, label, detail, confidence))
        self.db.commit()

    def timeline(self):
        # The story, dated, with every claim wearing its confidence.
        return self.db.execute(
            "SELECT date, label, detail, confidence FROM events ORDER BY date").fetchall()

    def hits(self):
        return self.db.execute(
            """SELECT h.date, h.query, h.subject, h.sender, s.name
               FROM hits h JOIN sources s ON h.source_id = s.id
               ORDER BY h.date""").fetchall()

    def close(self):
        self.db.close()


# 93. Live, Love, and let Love, Live.
# All Rights Reserved, Without Prejudice. — Johnathan 'Qasparr' (Κασπάρρ) Monroe
