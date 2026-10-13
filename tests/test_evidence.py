# VESTIGATOR · tests/test_evidence.py — the case file, tested.
#
# Sol in 20° 20′ Libra, Luna in 25° 29′ Scorpio, dies martis,
# Anno V:xii e.n. — 93.
#
# MECHANISM: in-memory SQLite; file a source, file a hit twice (second is
# a duplicate and must be refused), pin events at three confidences, read
# the timeline back in order. Run: python3 tests/test_evidence.py.

"""Tests for the case file."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from vestigator.evidence import CaseFile


def test_duplicate_hit_refused():
    c = CaseFile(":memory:")
    s = c.add_source("fixture", "mailbox")
    assert c.add_hit(s, "godaddy", subject="receipt", date="2012-08-14") is True
    assert c.add_hit(s, "godaddy", subject="receipt", date="2012-08-14") is False
    print("PASS test_duplicate_hit_refused")


def test_timeline_ordered_and_confident():
    c = CaseFile(":memory:")
    c.add_event("2026-06-11", "b", confidence="attested")
    c.add_event("2012-01-01", "a", confidence="reported")
    tl = c.timeline()
    assert tl[0][0] == "2012-01-01" and tl[1][0] == "2026-06-11"
    assert tl[0][3] == "reported" and tl[1][3] == "attested"
    print("PASS test_timeline_ordered_and_confident")


def test_bad_confidence_rejected():
    c = CaseFile(":memory:")
    try:
        c.add_event("2020-01-01", "x", confidence="certain")
    except AssertionError:
        print("PASS test_bad_confidence_rejected")
        return
    raise AssertionError("case filed an ungraded confidence")


if __name__ == "__main__":
    test_duplicate_hit_refused()
    test_timeline_ordered_and_confident()
    test_bad_confidence_rejected()
    print("3 tests passed")


# 93. Live, Love, and let Love, Live.
# All Rights Reserved, Without Prejudice. — Johnathan 'Qasparr' (Κασπάρρ) Monroe
