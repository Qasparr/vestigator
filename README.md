# VESTIGATOR

**The tracker — it follows footprints.**

*Authorship: Johnathan 'Qasparr' (Κασπάρρ) Monroe, Keeper of the Secret Treasure —
All Rights Reserved, Without Prejudice.*

A legitimate record-hunting toolkit in Python: hunt public archives and
**your own** mailboxes for the paper trail of a domain (or anything else),
and file every hit — headers, source, date — into a local SQLite case file.
No hidden agenda: public records and your own records, nothing else.

## The line

This tool holds the owner's key to the owner's house, for the session, and
never writes it down. There is no mode that touches a system the owner has
no right to enter. FOIA covers government records; private companies answer
to their own export tools, privacy-law requests, and subpoenas — this kit
works the first of those, and files toward the others.

## Quickstart

```bash
python -m vestigator.cli dry-run        # prove the machinery on fixtures
python -m vestigator.cli timeline       # the axoneme domain story, dated
python -m vestigator.cli hunt --case case.db --host imap.mail.com
# prompts for YOUR mailbox login; password never stored, never logged
```

## The duo

VESTIGATOR houses a detective duo, in Latin:

- **INDAGATOR** (*the investigator* — Holmes): the hunt engine —
  `indagator.py` holds both the IMAP hunt and the (dormant) Gmail hunt.
  The one who follows footprints.
- **SCRIBA** (*the scribe, the chronicler* — Watson): the case file —
  `scriba.py`, the SQLite mosaic. The one who writes it all down,
  faithful as ever.

The logo: a magnifying glass framing a footprint (*vestigium*), the quill
crossed behind it — gold on purple. `assets/vestigator-duo-logo.png`.

## Layout

- `vestigator/indagator.py` — INDAGATOR: IMAP + Gmail hunts over your own
  mailboxes (every folder, terms × date windows, headers filed verbatim)
- `vestigator/scriba.py` — SCRIBA: SQLite case file (sources, hits, dated
  events with mandatory confidence)
- `vestigator/timeline.py` — the domain timeline, seeded from RDAP findings
- `vestigator/cli.py` — `dry-run` / `hunt` / `timeline`
- `docs/` — `ARCHITECTURE.md` (where the data lives and how access works)
- `assets/` — the duo logo (purple and gold)
- `tests/` — the case file, tested

## Credentials

Env `VESTIGATOR_IMAP_USER` / `VESTIGATOR_IMAP_PASS`, or the interactive
prompt. Never hardcoded. Never in the case file.

## Standing

Version 0.1.0, penned 2026-10-13 (Sol in 20° 20′ Libra, dies martis,
Anno V:xii e.n. — 93). Educational/Thelemic code format throughout.

93. Live, Love, and let Love, Live.
