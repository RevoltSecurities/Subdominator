# Subdominator

Subdominator is a passive subdomain enumeration tool rebuilt around clean package boundaries, `aiohttp`, resource base classes, retryable HTTP, recursive enumeration, and database-backed result storage.

## Highlights

- `aiohttp` request layer with retry handling
- explicit resource base classes and registry
- recursive enumeration with configurable depth
- include and exclude resource selection
- per-resource provenance for each finding
- async SQLite persistence with Alembic migrations
- `richparser` CLI
- `revoltlogger` logging
- `revoltutils` config and file utility integration

## Quick Start

```bash
uv venv .venv --python 3.13 --seed --cache-dir .uv-cache
uv sync --cache-dir .uv-cache
. .venv/bin/activate
subdominator -d example.com --all
```

## Example

```bash
subdominator -d example.com --all --recursive-depth 1 --save-db --output results.txt
subdominator -d example.com --include-resources crtsh,certspotter,alienvault
subdominator --list-resources
subdominator --shell
```
