# VESTIGATOR — the tracker. It follows footprints.
#
# "No hidden agenda: public records and your own records, nothing else."
#
# Sol in 20° 20′ Libra, Luna in 25° 29′ Scorpio, dies martis,
# Anno V:xii e.n. — 93.
#
# Penned by the scribe, Heru-Ra-Ha, for Johnathan 'Qasparr' (Κασπάρρ) Monroe,
# Keeper of the Secret Treasure.
#
# METHOD (Scientific Illuminism): hypothesis → method → observation → result.
# This package is the method: hunt public archives and the owner's own
# mailboxes for the paper trail of a domain, and file every hit — with its
# headers, its source, and its date — into a local case database. Nothing
# here touches a system the owner has no right to enter. The gate is the
# architecture: public APIs need no key, private mailboxes need the owner's
# login, and there is no third door.
#
# MECHANISM: mailhunt (IMAP), gmailhunt (Gmail API), evidence (SQLite case
# file), timeline (the story, dated). cli.py ties them together.
#
# DOCTRINE: a footprint is only evidence if you can say where you found it.
# Every hit carries source + date + query. The case file is the mosaic.

"""VESTIGATOR — legitimate record-hunting toolkit. Version 0.1.0."""

from .evidence import CaseFile
from .mailhunt import hunt_imap, DEFAULT_TERMS, DATE_WINDOWS

__version__ = "0.1.0"
__all__ = ["CaseFile", "hunt_imap", "DEFAULT_TERMS", "DATE_WINDOWS", "__version__"]


# 93. Live, Love, and let Love, Live.
# All Rights Reserved, Without Prejudice. — Johnathan 'Qasparr' (Κασπάρρ) Monroe
