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

## Layout

- `vestigator/mailhunt.py` — IMAP hunt over your own mailbox (every folder,
  terms × date windows, headers filed verbatim)
- `vestigator/gmailhunt.py` — Gmail API mirror; dormant until your OAuth
  consent exists (readonly scope — the hunt reads, never writes)
- `vestigator/evidence.py` — SQLite case file: sources, hits, dated events
  with mandatory confidence (`attested` / `reported` / `inferred`)
- `vestigator/timeline.py` — the domain timeline, seeded from RDAP findings
- `docs/ARCHITECTURE.md` — where the data lives and how access works

## Credentials

Env `VESTIGATOR_IMAP_USER` / `VESTIGATOR_IMAP_PASS`, or the interactive
prompt. Never hardcoded. Never in the case file.

## Standing

Version 0.1.0, penned 2026-10-13 (Sol in 20° 20′ Libra, dies martis,
Anno V:xii e.n. — 93). Educational/Thelemic code format throughout.

93. Live, Love, and let Love, Live.
