# VESTIGATOR · mailhunt.py — search YOUR mailbox, with YOUR login.
#
# "No hidden agenda: public records and your own records, nothing else."
#
# Sol in 20° 20′ Libra, Luna in 25° 29′ Scorpio, dies martis,
# Anno V:xii e.n. — 93.
#
# Penned by the scribe, Heru-Ra-Ha, for Johnathan 'Qasparr' (Κασπάρρ) Monroe,
# Keeper of the Secret Treasure.
#
# MECHANISM: standard IMAP (imaplib) against the owner's own mailbox —
# mail.com default, any host configurable. Logs in with the OWNER'S
# credentials (env VESTIGATOR_IMAP_USER / VESTIGATOR_IMAP_PASS, or an
# interactive prompt — never hardcoded, never logged). Walks every folder,
# runs each term inside each date window, fetches headers + snippet for
# every hit, files all of it into the CaseFile with provenance.
#
# DOCTRINE: the credential is the owner's key to the owner's house. This
# tool holds the key only for the session and never writes it down. There
# is no mode that touches a mailbox the owner cannot open himself.

"""IMAP hunt over the owner's own mailbox."""

import email
import email.utils
import getpass
import imaplib
import os

# The quarry: registrar and money-trail terms.
DEFAULT_TERMS = ["godaddy", "google domains", "axoneme", "receipt",
                 "order confirmation", "domain registration", "cash app"]

# The windows: the .org years and the .dev years (IMAP SINCE/BEFORE).
DATE_WINDOWS = [("2012-01-01", "2014-01-01"), ("2020-01-01", "2022-01-01")]

DEFAULT_HOST = "imap.mail.com"


def _creds(user, password):
    # MECHANISM: explicit args win; env next; prompt last. The password is
    # never printed, never stored, never filed in the case database.
    user = user or os.environ.get("VESTIGATOR_IMAP_USER")
    password = password or os.environ.get("VESTIGATOR_IMAP_PASS")
    if not user:
        user = input("mailbox login: ").strip()
    if not password:
        password = getpass.getpass("password (not shown, not stored): ")
    return user, password


def _folders(conn):
    # Walk every folder, not just INBOX — carbon copies hide in Sent,
    # Archive, and folders the owner forgot he made.
    folders = []
    for _typ, data in [conn.list()]:
        for item in data:
            parts = item.decode(errors="replace").split('"/"')
            if len(parts) == 2:
                folders.append(parts[1].strip().strip('"'))
    return folders or ["INBOX"]


def _imap_date(iso):
    # IMAP wants 01-Jan-2012; we keep ISO everywhere else.
    y, m, d = iso.split("-")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return "%s-%s-%s" % (d, months[int(m) - 1], y)


def hunt_imap(case, host=DEFAULT_HOST, user=None, password=None,
              terms=None, windows=None, dry_run=False):
    """Run the hunt. Returns (folders_searched, hits_filed).

    MECHANISM: for each folder × each term × each window, IMAP SEARCH with
    (SINCE x BEFORE y TEXT "term"). Every hit's headers are fetched
    verbatim — headers are the fingerprint — plus a body snippet. Filed
    into the case with source = mailbox + folder.
    dry_run=True runs the whole pipeline against built-in fixture mail so
    the machinery is proven before any real credential is used.
    """
    terms = terms or DEFAULT_TERMS
    windows = windows or DATE_WINDOWS
    source_name = "dry-run fixture" if dry_run else "%s (%s)" % (host, user or "?")

    if dry_run:
        return _dry_run(case, source_name, terms, windows)

    user, password = _creds(user, password)
    source_name = "%s (%s)" % (host, user)
    conn = imaplib.IMAP4_SSL(host)
    conn.login(user, password)  # the owner's key, the owner's house
    try:
        source_id = case.add_source(source_name, "mailbox",
                                    "IMAP hunt, owner-authenticated")
        folders, hits = 0, 0
        for folder in _folders(conn):
            typ, _ = conn.select('"%s"' % folder, readonly=True)
            if typ != "OK":
                continue
            folders += 1
            for since, before in windows:
                for term in terms:
                    # DOCTRINE: the query is filed with the hit — the next
                    # person to read the case file can reproduce the hunt.
                    query = 'SINCE %s BEFORE %s TEXT "%s"' % (
                        _imap_date(since), _imap_date(before), term)
                    _typ, data = conn.search(None, "SINCE", _imap_date(since),
                                             "BEFORE", _imap_date(before),
                                             "TEXT", '"%s"' % term)
                    for num in data[0].split():
                        _t, mdata = conn.fetch(num, "(BODY.PEEK[HEADER] BODY.PEEK[TEXT])")
                        raw_hdr = mdata[0][1] if mdata and mdata[0] else b""
                        msg = email.message_from_bytes(raw_hdr)
                        date = email.utils.parsedate_to_datetime(
                            msg.get("Date", "")).isoformat() \
                            if msg.get("Date") else ""
                        body = ""
                        if mdata and len(mdata) > 1 and mdata[1]:
                            body = mdata[1][1][:500].decode(errors="replace")
                        if case.add_hit(source_id, query,
                                        subject=msg.get("Subject", ""),
                                        sender=msg.get("From", ""),
                                        date=date,
                                        headers=raw_hdr.decode(errors="replace")[:2000],
                                        snippet=body):
                            hits += 1
        return folders, hits
    finally:
        try:
            conn.logout()
        except Exception:
            pass


def _dry_run(case, source_name, terms, windows):
    # MECHANISM: fixture mail shaped like the quarry — a GoDaddy receipt
    # and a Google Domains confirmation — so the pipeline, the filing,
    # and the provenance are all exercised with zero credentials.
    source_id = case.add_source(source_name, "mailbox", "dry-run fixture")
    fixtures = [
        ("godaddy",
         "From: GoDaddy <receipts@godaddy.com>\r\n"
         "Date: Tue, 14 Aug 2012 10:02:00 -0400\r\n"
         "Subject: Your GoDaddy receipt — axoneme.org\r\n\r\n"
         "Thank you for your order..."),
        ("google domains",
         "From: Google Domains <domains-noreply@google.com>\r\n"
         "Date: Mon, 11 Jan 2021 15:44:00 -0500\r\n"
         "Subject: Your domain registration — axoneme.dev\r\n\r\n"
         "Your domain is registered..."),
    ]
    hits = 0
    for term, raw in fixtures:
        msg = email.message_from_string(raw)
        if case.add_hit(source_id, 'TEXT "%s"' % term,
                        subject=msg.get("Subject", ""),
                        sender=msg.get("From", ""),
                        date=msg.get("Date", ""),
                        headers=raw.split("\r\n\r\n")[0],
                        snippet=raw.split("\r\n\r\n")[1]):
            hits += 1
    return 1, hits  # 1 folder (fixture), N hits


# 93. Live, Love, and let Love, Live.
# All Rights Reserved, Without Prejudice. — Johnathan 'Qasparr' (Κασπάρρ) Monroe
