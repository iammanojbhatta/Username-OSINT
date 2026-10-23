# MANOJ USERNAME OSINT v4.0.0

Independent, lightweight public username OSINT research tool.

## Scope

Checks configurable public username endpoints, classifies responses, stores bounded public evidence, hashes evidence with SHA-256, and generates interactive HTML plus JSON reports. It does not log in, guess passwords, bypass CAPTCHA/access controls, access private profiles, exploit sites, use leaked credentials, or evade security controls. A username match does not prove account ownership or identity.

## Install

Python 3.10+ recommended. No third-party runtime dependencies.

```bash
python3 -m unittest discover -s tests -v
python3 tools/validate_sites.py
```

## Usage

```bash
python3 main.py scan --username manojbhatta
python3 main.py scan --username manojbhatta --category developer
python3 main.py scan --username manojbhatta --workers 6 --timeout 10
python3 main.py scan --username manojbhatta --no-cache
python3 main.py validate-sites
python3 main.py test-site --site GitHub --username testuser
```

Reports are created under `cases/<username>/<case-id>/report.html` and `results.json`; SQLite is `cases/osint.sqlite3`.

## Site database

`data/sites.json` is external and data-driven. The architecture supports 1,000+ entries without changing Python source. This distribution ships 2,336 real public endpoints; most are marked `needs_validation` until individually confirmed, rather than presented as verified. Use `verified`, `needs_validation`, or `disabled`. Add only real public endpoints and run the validator.

## Design

Concurrent scanning, per-host rate limiting, retries/backoff, SQLite caching, bounded evidence snapshots, SHA-256, multi-state classification, HTML escaping, interactive filtering, and offline tests. HTTP 200 alone never means FOUND.

## Responsible use

Use only for lawful public OSINT, authorized security research, defensive research, journalism, or education. Respect applicable law, site terms, robots policies, and rate limits.

## License

MIT. See `LICENSE`.
