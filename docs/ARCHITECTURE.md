# VESTIGATOR — Architecture: where the data lives, and how access works

## The three kinds of data

| Kind | Examples | Access |
|---|---|---|
| **Public records** | Wayback CDX, Certificate Transparency (crt.sh), RDAP/WHOIS, Common Crawl | No key needed. Query the API. |
| **Your records** | Your mailboxes (IMAP), Gmail API, Cash App history export, bank statements | Your login. This kit's `mailhunt`/`gmailhunt` hold it for the session only. |
| **Their internal databases** | Google's / Block's / GoDaddy's user stores | **Not reachable.** No application exists — not for sale, not for request — outside legal process (subpoena). |

## The pipeline

```
Public (no auth):  Wayback · crt.sh · RDAP · Common Crawl
                        \ 
Your (your login):  mail.com IMAP · Gmail API (readonly) · exports
                        \
                         → VESTIGATOR → INDAGATOR hunts, SCRIBA files
                                          → local SQLite case file
                                          → timeline + evidence
```

## The case file

SQLite, local, no server. `sources` (where each hunt ran), `hits` (what it
found — query, headers, snippet, date), `events` (dated facts, each wearing
`attested` / `reported` / `inferred`). The mosaic is the argument: no single
table proves anything; the pattern across them does.

## What this kit will not do

Touch a system the owner has no right to enter. There is no bypass mode, no
credential replay, no third door. The architecture is the gate.
