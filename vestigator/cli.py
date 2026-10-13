# VESTIGATOR · cli.py — the command line.
#
# "No hidden agenda: public records and your own records, nothing else."
#
# Sol in 20° 20′ Libra, Luna in 25° 29′ Scorpio, dies martis,
# Anno V:xii e.n. — 93.
#
# Penned by the scribe, Heru-Ra-Ha, for Johnathan 'Qasparr' (Κασπάρρ) Monroe,
# Keeper of the Secret Treasure.
#
# MECHANISM: `vestigator dry-run` proves the machinery on fixtures.
# `vestigator hunt --case case.db` runs the IMAP hunt against the owner's
# mailbox (prompts for the login; nothing stored). `vestigator timeline
# --case case.db` seeds and prints the dated story.

"""Command line: dry-run, hunt, timeline."""

import argparse
import sys

from .evidence import CaseFile
from .mailhunt import hunt_imap
from .gmailhunt import hunt_gmail
from .timeline import seed_axoneme_case, show


def cmd_dryrun(_args):
    case = CaseFile(":memory:")
    folders, hits = hunt_imap(case, dry_run=True)
    ghits = hunt_gmail(case, dry_run=True)
    seed_axoneme_case(case)
    print("dry-run: %d folder(s), %d imap hit(s), %d gmail hit(s) filed"
          % (folders, hits, ghits))
    print("timeline events: %d" % len(case.timeline()))
    show(case)
    return 0


def cmd_hunt(args):
    case = CaseFile(args.case)
    folders, hits = hunt_imap(case, host=args.host, user=args.user)
    print("hunt: %d folder(s) searched, %d hit(s) filed in %s"
          % (folders, hits, args.case))
    return 0


def cmd_timeline(args):
    case = CaseFile(args.case)
    seed_axoneme_case(case)
    show(case)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="vestigator",
                                 description="Legitimate record-hunting toolkit.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dry-run", help="prove the machinery on fixtures")
    d.set_defaults(fn=cmd_dryrun)
    h = sub.add_parser("hunt", help="IMAP hunt over your own mailbox")
    h.add_argument("--case", default="case.db")
    h.add_argument("--host", default="imap.mail.com")
    h.add_argument("--user", default=None)
    h.set_defaults(fn=cmd_hunt)
    t = sub.add_parser("timeline", help="seed and print the domain timeline")
    t.add_argument("--case", default="case.db")
    t.set_defaults(fn=cmd_timeline)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())


# 93. Live, Love, and let Love, Live.
# All Rights Reserved, Without Prejudice. — Johnathan 'Qasparr' (Κασπάρρ) Monroe
