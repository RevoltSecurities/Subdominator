# Subdominator Rewrite Todo

## Current Legacy Context

- Current entrypoint is `subdominator/subdominator.py`, which forwards into `subdominator/modules/handler.py`.
- `handler.py` is the main coupling point for CLI parsing, config bootstrap, update checks, source registration, async execution, output writing, and DB persistence.
- Source integrations live in `subdominator/modules/subscraper/*` as one module per provider with inconsistent interfaces and duplicated request logic.
- Persistence is split between raw SQLite setup in `config.py` and SQLAlchemy async models in `models.py` / `crud.py`.
- The DB layer imports runtime state from `handler.py`, which creates circular design pressure and makes testing difficult.
- Output, notifications, help text, shell UX, and utility functions are spread across unrelated modules under `subdominator/modules`.

## Rewrite Goals

- Replace the legacy layout with a coherent package and module structure.
- Move to `aiohttp` for HTTP operations and introduce a reusable retry-aware HTTP client.
- Introduce explicit base classes for resources and enumerators.
- Reuse upstream RevoltSecurities packages where they fit instead of rebuilding equivalent layers locally.
- Support:
  - recursive enumeration
  - specific comma-separated resource selection
  - per-resource result tracking
  - unique result storage
  - database integration
  - migrations
- Preserve the tool’s core purpose: passive subdomain enumeration across many providers.

## Execution Plan

- [x] Pull the latest remote state from `origin/main`.
- [x] Remove the legacy package layout and replace it with a new architecture.
- [x] Create a modern package skeleton for CLI, config, core, HTTP, resources, services, storage, and migrations.
- [x] Integrate `RichParser` for CLI help rendering and argument grouping.
- [x] Integrate `Revoltlogger` for structured terminal logging and output severity control.
- [x] Integrate selected `Revoltutils` modules for config, file, folder, and YAML-adjacent workflows.
- [x] Implement shared domain models and settings.
- [x] Implement `RetryableHttpClient` with `aiohttp`, timeouts, retry policy, and session lifecycle management.
- [x] Implement base resource classes and a resource registry.
- [x] Implement initial resource adapters that prove the new architecture end-to-end.
- [x] Implement enumeration service with support for:
- [x] single domain enumeration
- [x] domain list enumeration
- [x] recursive enumeration
- [x] include/exclude resource lists
- [x] result deduplication
- [x] per-resource provenance
- [x] persistence to DB and output files
- [x] Add migrations and initialize schema management.
- [x] Update packaging and dependency metadata.
- [x] Resolve the Python compatibility decision introduced by upstream dependencies:
- [x] bump Subdominator to `>=3.13`
- [x] Run validation checks for imports and CLI bootstrap.

## Verified State

- `uv` virtual environment created at `.venv`
- dependencies installed with `uv sync`
- `subdominator --list-resources` works
- `python -m compileall src` works
- live CLI smoke test works through the enumeration path and exits cleanly
- DB repository smoke test works with SQLite
- output file writing works without hanging shutdown

## Remaining Work

- [x] Add all legacy provider adapters into the new resource registry.
- [x] Add provider-config aware authenticated resources.
- [x] Add richer result reporting and JSON report output.
- [ ] Add shell/report subcommands on top of the new run summary model.
- [ ] Add notification integrations.
- [x] Add test coverage beyond smoke validation.
- [ ] Add resource-specific pagination and structured parsing hardening.
- [ ] Decide whether DB initialization should rely entirely on Alembic instead of `create_all` bootstrap.

## New Coverage Added

- authenticated providers added:
- `chaos`
- `fullhunt`
- `securitytrails`
- `virustotal`
- additional providers added:
- `bufferover`
- `dnsrepo`
- `leakix`
- `sitedossier`
- richer providers added:
- `binaryedge`
- `censys`
- `hudsonrock`
- `shodan`
- newly added coverage:
- `abuseipdb`
- `facebook`
- `zoomeyeapi`
- paginated provider support expanded in `fofa`, `netlas`, `binaryedge`, and `censys`
- config-aware resource listing now marks providers that require keys with `*`
- tests added for provider config loading and registry metadata
- run summaries now include:
- total duration
- targets scanned
- per-resource execution stats
- success/failure counts
- optional JSON summary reports
- rich table rendering now includes:
- colored overview summary table
- aggregate resource statistics table
- detailed per-resource execution table

## Current Coverage Snapshot

- current implemented resource count: `53`
- current resource coverage matches the legacy inventory exactly
- explicit comparison check result:
- `missing_from_current = []`
- `extra_in_current = []`

## Known Legacy Risks To Avoid

- Avoid runtime-global mutable result containers shared across invocations.
- Avoid handler-driven import cycles.
- Avoid mixing sync and async persistence setup.
- Avoid putting business logic inside CLI argument parsing or help flows.
- Avoid hard-coding source orchestration in one file.

## Upstream Package Research Notes

- `RichParser`
- package name: `richparser`
- current version observed: `1.0.1`
- declared Python requirement: `>=3.13`
- actual usable API from examples:
- `RichParser(description=...)`
- `add_argument(section, *flags, **kwargs)`
- `add_subcommand(name, description)`
- `add_subcommand_argument(command, section, *flags, **kwargs)`
- `parse_args()`
- fit for rewrite:
- use for grouped help sections and future subcommand expansion

- `Revoltutils`
- package name: `revoltutils`
- current version observed: `1.0.2`
- declared Python requirement: `>=3.13`
- directly relevant modules inspected:
- `Config`
- `FileUtils`
- `FolderUtils`
- `OSUtils`
- `YamlUtils`
- fit for rewrite:
- use for config bootstrap, file IO, folder management, environment and OS access, and YAML provider config handling
- do not use `HttpUtils` for the main request layer because the rewrite requirement is `aiohttp` with a dedicated retryable client

- `Revoltlogger`
- package name: `revoltlogger`
- current version observed: `1.0.1`
- declared Python requirement: `>=3.7`
- actual usable API from examples:
- `Logger(name=..., level=LogLevel.INFO, colored=True)`
- methods: `trace/debug/verbose/info/success/warn/error/critical/custom/output/bannerlog/stdinlog`
- fit for rewrite:
- use as the primary runtime logger for CLI and service messages
