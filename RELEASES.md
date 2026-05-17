# Release Notes

---

## v3.0.0 — The Precision Discovery Release

> **Release date:** 2026-05-17

Subdominator v3.0.0 is a complete ground-up rewrite. Every subsystem has been replaced or significantly hardened — from the async enumeration engine to the HTTP client, storage layer, CI/CD pipelines, and developer tooling. This release is focused on correctness, stability at scale, and a professional operator experience.

---

### New Features

#### Interactive Audit Shell
A full terminal interface for managing historical reconnaissance data without leaving the CLI. Launch with `--shell` / `-sh`.

| Command | Action |
|---|---|
| `domains` | List all stored root domains with finding counts |
| `domain <root>` | Stats summary for a stored domain |
| `findings <root>` | Show all stored subdomains for a domain |
| `add <root> <file>` | Import and merge findings from a text file |
| `export <root> <path> [txt\|json\|html]` | Export findings to a file |
| `delete <root>` | Remove a domain and all its findings |
| `resources` | List resource catalog with auth requirements |
| `update` / `release` | In-shell update and release notes |

#### Disk-Backed Findings Cache
High-volume enumeration runs (100K+ subdomains) no longer spike RAM. An `AsyncDiskCache` serialises the live deduplication set to disk during the run, keeping memory usage flat regardless of scale.

#### Recursive Subdomain Enumeration
`--recursive-depth` / `-rd` automatically feeds every newly discovered subdomain back through the full resource pipeline to any configured depth, uncovering hidden nested assets other tools miss.

#### Diagnostic Health Engine
`--health-check` / `-hc` verifies internet connectivity and API key status before committing to a long scan. Instantly surfaces misconfigured keys or network issues.

#### JSON Summary Report (`--report-json` / `-rj`)
Structured JSON output covering every resource execution: findings count, duration, errors, and run metadata — ready to pipe into dashboards or downstream automation.

#### Per-Resource Stats (`--show-resource-stats` / `-srs`)
Detailed table showing individual resource finding counts, total duration, and failure counts after a run. Combine with `--show-summary` for full run telemetry.

#### HTML Reports (`--html` / `-oh`)
Standalone HTML evidence reports rendered with Jinja2. Install the optional extra: `pip install "subdominator[reports]"`.

#### Global Container Registry
Official Docker images published to GHCR on every release:
```bash
docker run --rm -it ghcr.io/revoltsecurities/subdominator:latest -d example.com
```

#### Custom Database Path (`--db-path` / `-dp`)
Write the SQLite findings database to any path. Use `--no-db` / `-nd` to skip persistence entirely for a run.

---

### Providers

**73 passive OSINT sources** are integrated and verified for this release. New providers added in v3.0.0:

- **WhoisFreaks** — paginated subdomain API with active status filtering
- **Windvane** — paginated POST-based subdomain lookup
- **ArgosDNS** — paginated bearer-auth API with `has_more` cursor pagination
- **DigitalYama** — lightweight API key provider
- **DomScan** — subdomain API integration
- **RSECloud** — paginated POST API with total-pages tracking
- **Reconeer** — optional-key provider with enhanced results when authenticated
- **SubMD** — optional-key provider with Bearer auth upgrade path
- **Cyfare** — POST-based enumeration endpoint

**Default-disabled sources** (use `--all` or `-ir` to include):
`commoncrawl`, `github`, `virustotal`, `waybackarchive`

---

### Bug Fixes

#### Critical: Data loss in concurrent enumeration (`enumerator.py`)
The result-processing block was outside the `for task in done_tasks` loop. When multiple resources completed simultaneously, only the last task's findings were processed — all others were silently discarded. Fixed by correctly indenting the processing block inside the loop.

#### Critical: SSL/Proxy not propagated to all HTTP surfaces
Four separate gaps where `--insecure` and `--proxy` (and their env var equivalents) were silently ignored:

- **`app.py`** — `ssl_verify=not args.insecure` hard-coded `True` at construction time, overriding `SUBDOMINATOR_SSL_VERIFY` env var. Fixed: `False if args.insecure else defaults.ssl_verify`.
- **`app.py`** — `proxy=args.proxy` passed `None` explicitly when the flag was absent, overriding `SUBDOMINATOR_PROXY` env var. Fixed: `args.proxy or defaults.proxy`.
- **`crtsh.py`** — `asyncpg.connect()` had no `ssl=` parameter, causing `SSL: CERTIFICATE_VERIFY_FAILED` in certificate-inspection environments. Fixed: `ssl=False` (crt.sh port 5432 is plain TCP, no SSL needed).
- **`github.py`** — Direct `_session.request()` call did not forward `proxy=self.client.proxy`, silently bypassing `--proxy` for GitHub code-search API calls. Fixed.

#### `BrokenPipeError` crash on piped output (`app.py`)
Routing output through `revoltlogger` / colorama caused an unhandled `BrokenPipeError` when piping to tools like `head` or `grep`. Rewritten to write directly to `sys.stdout` with a `BrokenPipeError` guard.

#### `AttributeError` crash in Windvane provider (`windvane.py`)
Provider called `self.client.post_json()` which does not exist on `RetryableHttpClient`. Fixed to use the correct `self.client.request_json("POST", ...)` with `json_body=` kwarg.

#### `NameError` crash in ThreatBook provider (`threatbook.py`)
A previous partial fix removed `import logging` and `logger = logging.getLogger(...)` but left a bare `logger.debug(...)` call at line 33. Any API response with a non-zero `response_code` triggered a `NameError` crash. Fixed to use `self.client.logger.debug(...)`.

#### Robtex contradictory config flags (`robtex.py`)
`has_optional_config = True` and `requires_config = False` were set but the provider always returned empty results without a key. Corrected to `requires_config = True`.

#### Stray stdlib logging in three providers
`urlscan.py`, `threatbook.py`, and `threatminer.py` imported and used Python's stdlib `logging.getLogger()` instead of the project's `revoltlogger`. All replaced with `self.client.logger.debug(...)`.

#### Broken PyPI release workflow (`.github/workflows/python-publish.yml`)
Workflow called `python3 setup.py sdist bdist_wheel` — no `setup.py` exists (hatchling build backend). Completely rewritten to use `uv build && uv publish`.

#### Wrong Docker Buildx action (`.github/workflows/docker-publish.yml`)
`actions/setup-buildx-action@v3` does not exist. Fixed to `docker/setup-buildx-action@v3`.

#### Test suite hard-failure (`pyproject.toml`, `tests/test_shell.py`)
All 7 test files failed with `ModuleNotFoundError` due to missing `pythonpath = ["src"]` in `[tool.pytest.ini_options]`. Three shell tests also failed due to a missing `gitmanager=` kwarg added after the tests were written. Both fixed.

---

### Environment Variable Support

All runtime settings can now be driven by environment variables (prefix: `SUBDOMINATOR_`):

| Variable | Flag equivalent | Default |
|---|---|---|
| `SUBDOMINATOR_SSL_VERIFY=false` | `--insecure` / `-k` | `true` |
| `SUBDOMINATOR_PROXY=http://host:port` | `--proxy` / `-p` | _(none)_ |
| `SUBDOMINATOR_TIMEOUT=30` | `--timeout` / `-t` | `20.0` |
| `SUBDOMINATOR_CONCURRENCY=16` | `--concurrency` / `-c` | `8` |

Standard proxy env vars (`HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`) are also respected automatically. CLI flags always take priority over env vars.

---

### CI/CD & Packaging

- **PyPI**: `uv build` + `uv publish` on GitHub Release (replaces broken `setup.py` wheel)
- **GHCR Docker**: `docker/setup-buildx-action@v3`, multi-platform image on GitHub Release
- **Build backend**: `hatchling` (no `setup.py`)
- **Package manager**: `uv` with locked `uv.lock` for reproducible installs
- **Python**: requires 3.13+

---

### Developer Notes

- `pytest` config added: `pythonpath = ["src"]`, `asyncio_mode = "strict"`
- Dev dependency group: `pytest`, `pytest-asyncio`, `pytest-anyio`
- Run tests: `python -m pytest tests/ -v`
- Build: `uv build`

---

## Legacy Versions

### v2.1.1 — Stability Patch
- **Maintenance**: Provider catalog updates and installation reliability fixes.

### v2.1.0 — Branding & Docs
- **Identity**: Refined documentation and visual branding.

### v2.0.0 — Feature Expansion
- **Growth**: Significant provider catalog expansion and initial Docker support.

---

Powered by **RevoltSecurities**
