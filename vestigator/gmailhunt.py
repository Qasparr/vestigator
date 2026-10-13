# VESTIGATOR · gmailhunt.py — the Gmail side, when the account comes home.
#
# "No hidden agenda: public records and your own records, nothing else."
#
# Sol in 20° 20′ Libra, Luna in 25° 29′ Scorpio, dies martis,
# Anno V:xii e.n. — 93.
#
# Penned by the scribe, Heru-Ra-Ha, for Johnathan 'Qasparr' (Κασπάρρ) Monroe,
# Keeper of the Secret Treasure.
#
# MECHANISM: same hunt as mailhunt, via the Gmail API — which needs the
# owner's OAuth consent on the owner's account. This module is complete
# but DORMANT: it runs only in dry-run until real credentials exist. The
# day axoneme.dev@gmail.com comes home (recovery or legal process), the
# same terms and windows run here and the hits file into the same case.
#
# DOCTRINE: dormant code is honest code — it says what it will do and
# waits for the key, instead of pretending the door is open.

"""Gmail API hunt. Dormant until the owner's OAuth consent exists."""

from .mailhunt import DEFAULT_TERMS, DATE_WINDOWS

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
# DOCTRINE: readonly. The hunt reads; it never sends, deletes, or labels.
# A tracker that can write is a weapon wearing a tracker's coat.


def hunt_gmail(case, credentials=None, terms=None, windows=None, dry_run=True):
    """Mirror of hunt_imap for Gmail. Currently dry-run only.

    MECHANISM: when credentials (a google.oauth2 Credentials with the
    readonly scope, granted by the owner) are supplied and dry_run=False,
    this lists messages matching each term+window via users.messages.list
    (q='term after:YYYY/M/D before:YYYY/M/D'), fetches full headers, and
    files them like mailhunt. Until then, dry_run exercises the filing.
    """
    terms = terms or DEFAULT_TERMS
    windows = windows or DATE_WINDOWS
    if dry_run or credentials is None:
        source_id = case.add_source("gmail (dry-run fixture)", "mailbox",
                                    "dormant — awaiting owner's OAuth")
        hits = 0
        for term in terms[:2]:
            if case.add_hit(source_id, "gmail q: %s" % term,
                            subject="[fixture] domain receipt",
                            sender="domains-noreply@google.com",
                            date="2021-01-11",
                            headers="From: domains-noreply@google.com",
                            snippet="fixture — the real hunt runs on recovery"):
                hits += 1
        return hits

    # Live path — owner-authenticated only.
    from googleapiclient.discovery import build
    svc = build("gmail", "v1", credentials=credentials)
    source_id = case.add_source("gmail (owner OAuth)", "mailbox",
                                "Gmail API, readonly scope")
    hits = 0
    for since, before in windows:
        after = since.replace("-", "/")
        bef = before.replace("-", "/")
        for term in terms:
            q = "%s after:%s before:%s" % (term, after, bef)
            msgs = svc.users().messages().list(
                userId="me", q=q, maxResults=100).execute().get("messages", [])
            for m in msgs:
                full = svc.users().messages().get(
                    userId="me", id=m["id"], format="full").execute()
                hdrs = {h["name"]: h["value"]
                        for h in full["payload"].get("headers", [])}
                if case.add_hit(source_id, q,
                                subject=hdrs.get("Subject", ""),
                                sender=hdrs.get("From", ""),
                                date=hdrs.get("Date", ""),
                                headers=str(hdrs)[:2000]):
                    hits += 1
    return hits


# 93. Live, Love, and let Love, Live.
# All Rights Reserved, Without Prejudice. — Johnathan 'Qasparr' (Κασπάρρ) Monroe
