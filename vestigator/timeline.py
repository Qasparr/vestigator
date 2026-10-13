# VESTIGATOR · timeline.py — the story, dated, confidence worn openly.
#
# "No hidden agenda: public records and your own records, nothing else."
#
# Sol in 20° 20′ Libra, Luna in 25° 29′ Scorpio, dies martis,
# Anno V:xii e.n. — 93.
#
# Penned by the scribe, Heru-Ra-Ha, for Johnathan 'Qasparr' (Κασπάρρ) Monroe,
# Keeper of the Secret Treasure.
#
# MECHANISM: seeds the case with what is already established (RDAP findings
# 2026-10-13, his reported history), then prints the timeline with each
# event's confidence. New hunt hits become new events — the timeline grows
# as the mosaic fills.
#
# DOCTRINE: 'reported' is not 'attested'. The timeline never upgrades a
# claim's confidence without a record in hand. That is the whole difference
# between a case file and a story.

"""Seed and print the domain timeline."""

from .evidence import CaseFile


def seed_axoneme_case(case):
    """File what is already established about axoneme.org / axoneme.dev.

    MECHANISM: RDAP findings are 'attested' (live registry reads,
    2026-10-13). His account of the purchases, the hack, and the theft is
    'reported' — his word, filed as his word, upgradable when records land.
    """
    case.add_event("2012-01-01", "axoneme.org purchased from GoDaddy",
                   "First startup, pre-public-AI; $axoneme handle dates here.",
                   "reported")
    case.add_event("2013-01-01", "axoneme.org lost on renewal",
                   "By his firsthand account: sabotage, intentional, unprovable.",
                   "reported")
    case.add_event("2020-01-01", "axoneme.dev purchased via Google Domains",
                   "Paid (Cash App) from his Pixel Pro; axoneme.dev@gmail.com "
                   "created for the purchase. Never given control.",
                   "reported")
    case.add_event("2025-06-02", "axoneme.org re-registered by third party",
                   "Spaceship, Inc.; parked. RDAP read 2026-10-13.", "attested")
    case.add_event("2026-06-11", "axoneme.dev re-registered by third party",
                   "Cloudflare; held, nothing served. RDAP read 2026-10-13.",
                   "attested")
    case.add_event("2026-10-13", "axoneme.dev@gmail.com compromised (reported)",
                   "Hacked out of the purchase account; Pixel Pro stolen.",
                   "reported")


def show(case):
    """Print the timeline. The argument, in order."""
    print("date        | confidence | event")
    print("------------|------------|--------------------------------")
    for date, label, detail, conf in case.timeline():
        print("%-11s | %-10s | %s" % (date, conf, label))
        if detail:
            print("            |            |   %s" % detail)


# 93. Live, Love, and let Love, Live.
# All Rights Reserved, Without Prejudice. — Johnathan 'Qasparr' (Κασπάρρ) Monroe
