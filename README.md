<h1 align="center">
  <img src="static/subdominator.png" alt="Subdominator" width="460px">
  <br>
</h1>

<div align="center">

**High-performance passive subdomain enumeration engine for effortless asset discovery and rapid reconnaissance**

</div>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#usage">Usage</a> •
  <a href="#examples">Examples</a> •
  <a href="#interactive-shell">Shell</a> •
  <a href="#providers">Providers</a> •
  <a href="#output-formats">Output</a> •
  <a href="#docker">Docker</a>
</p>

<div align="center">

[![PyPI version](https://img.shields.io/pypi/v/subdominator?color=brightgreen)](https://pypi.org/project/subdominator/)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/)
[![GitHub release](https://img.shields.io/github/v/release/RevoltSecurities/Subdominator)](https://github.com/RevoltSecurities/Subdominator/releases)
[![GitHub last commit](https://img.shields.io/github/last-commit/RevoltSecurities/Subdominator)](https://github.com/RevoltSecurities/Subdominator/commits/main)
[![License: MIT](https://img.shields.io/github/license/RevoltSecurities/Subdominator)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ghcr.io-blue?logo=docker)](https://github.com/RevoltSecurities/Subdominator/pkgs/container/subdominator)

</div>

---

Subdominator is a high-performance passive subdomain enumeration engine. It leverages **73 OSINT sources** — certificate transparency logs, search engines, threat intelligence feeds, DNS datasets, and more — to map your target's full attack surface in seconds.

Built on Python's async/await stack (`asyncio` + `aiohttp`), it handles 100K+ subdomains per run without memory spikes thanks to its disk-backed findings cache.

---

## Features

- **73 passive OSINT sources** — CT logs, search engines, threat intel, DNS archives, and more
- **Recursive enumeration** — automatically scan discovered subdomains to any depth
- **Disk-backed cache** — 100K+ subdomains per run with stable memory usage
- **Concurrent execution** — configurable parallelism with async-first architecture
- **Interactive audit shell** — search, filter, export, and manage historical findings
- **Multiple output formats** — plain text, JSONL stream, JSON report, HTML report
- **SQLite persistence** — save and query findings across sessions with `--save-db`
- **Health diagnostics** — verify connectivity and API key status before a run
- **Docker-ready** — pre-built images on GHCR, no local Python setup required

---

## Installation

### Recommended — uv tool (fastest)

```bash
uv tool install subdominator
```

### pip (traditional)

```bash
pip install --upgrade subdominator
```

### From source

```bash
git clone https://github.com/RevoltSecurities/Subdominator.git
cd Subdominator
uv sync
```

### With HTML report support

```bash
pip install "subdominator[reports]"
# or
uv tool install "subdominator[reports]"
```

> **Requires Python 3.13+**

---

## Configuration

Subdominator stores its API key config in a YAML file. On first run it creates the template automatically at:

```
~/.config/subdominator/provider-config.yaml
```

Open that file and add your keys under each provider. Each entry is a list so you can supply multiple keys — Subdominator will pick one at random per run:

```yaml
# ~/.config/subdominator/provider-config.yaml
shodan:
  - YOUR_SHODAN_KEY

censys:
  - YOUR_CENSYS_ID:YOUR_CENSYS_SECRET

github:
  - ghp_token1
  - ghp_token2

# Providers that share the same RapidAPI key:
# coderog, rapidfinder, rapidscan → rapidapi
rapidapi:
  - YOUR_RAPIDAPI_KEY

# Aliases: whoisxml → whoisxmlapi, zoomeyeapi → zoomeye
whoisxmlapi:
  - YOUR_WHOISXMLAPI_KEY
zoomeye:
  - YOUR_ZOOMEYE_KEY
```

Use a custom config path with `--config-path` / `-cp`:

```bash
subdominator -d example.com -cp /path/to/my-config.yaml
```

### Key aliases

| Config key | Used by providers |
|---|---|
| `rapidapi` | `coderog`, `rapidfinder`, `rapidscan` |
| `whoisxmlapi` | `whoisxml` |
| `zoomeye` | `zoomeyeapi` |

---

## Usage

```
subdominator [flags]
```

### Input

| Flag | Short | Description |
|---|---|---|
| `--domain` | `-d` | Single target domain |
| `--domain-list` | `-dL` | File with one domain per line (bulk mode) |

### Resource selection

| Flag | Short | Description |
|---|---|---|
| `--all` | | Use all 73 resources (includes disabled-by-default ones) |
| `--include-resources` | `-ir` | Comma-separated list of resources to use |
| `--exclude-resources` | `-er` | Comma-separated list of resources to skip |
| `--list-resources` | `-ls` | Print resource catalog with auth requirements |
| `--dork` | `-dk` | Custom search dork (Google and supported engines) |

> **Disabled by default:** `commoncrawl`, `github`, `virustotal`, `waybackarchive` — these are slow or rate-limited. Use `--all` or `-ir` to include them explicitly.

### Runtime

| Flag | Short | Description |
|---|---|---|
| `--recursive-depth` | `-rd` | Max recursion depth for discovered subdomains (default: 0) |
| `--concurrency` | `-c` | Parallel resource slots (default: 8) |
| `--timeout` | `-t` | HTTP timeout in seconds (default: 20.0) |
| `--retries` | `-rt` | Retries per failed request (default: 3) |
| `--config-path` | `-cp` | Path to custom provider config YAML |

### Output

| Flag | Short | Description |
|---|---|---|
| `--output` | `-o` | Write plain-text results to a file |
| `--output-directory` | `-oD` | Directory to save per-domain files (bulk mode) |
| `--html` | `-oh` | Generate an HTML report (requires `jinja2`) |
| `--json` | `-j` | Stream JSONL to stdout (`{"domain":...,"subdomain":...,"resource":...}`) |
| `--table` | `-tb` | Print findings as a formatted terminal table |
| `--show-summary` | `-ss` | Print a run summary after completion |

### Storage & diagnostics

| Flag | Short | Description |
|---|---|---|
| `--save-db` | `-sd` | Persist findings to the local SQLite database |
| `--shell` | `-sh` | Open the interactive audit shell |
| `--health-check` | `-hc` | Verify connectivity and API key status |
| `--update` | `-up` | Update Subdominator to the latest release |
| `--verbose` | `-v` | Enable debug logging |
| `--no-color` | `-nc` | Disable colored output |

---

## Examples

**Basic single-domain scan:**
```bash
subdominator -d example.com
```

**Save results to a file:**
```bash
subdominator -d example.com -o results.txt
```

**Recursive enumeration (depth 2):**
```bash
subdominator -d example.com -rd 2
```

**Stream JSON for pipeline integration:**
```bash
subdominator -d example.com -j | jq .subdomain
```

**Use only specific sources:**
```bash
subdominator -d example.com -ir shodan,censys,securitytrails
```

**Exclude slow sources:**
```bash
subdominator -d example.com -er commoncrawl,waybackarchive
```

**Bulk scan from a file, save per-domain results:**
```bash
subdominator -dL domains.txt -oD ./output/
```

**Full scan with all sources + HTML report + DB save:**
```bash
subdominator -d example.com --all -oh report.html -sd
```

**Custom Google dork:**
```bash
subdominator -d example.com -ir google -dk site:example.com -inurl:www
```

**Health check before a run:**
```bash
subdominator --health-check
```

**Pipe-safe output (no BrokenPipeError):**
```bash
subdominator -d example.com | head -20
subdominator -d example.com -j | grep "api\."
```

---

## Interactive Shell

Launch the audit shell with `--shell` or `-sh`:

```bash
subdominator --shell
```

The shell provides a persistent terminal interface for querying and managing historical findings stored in the SQLite database.

### Shell commands

| Command | Description |
|---|---|
| `domains` | List all stored root domains with finding counts |
| `domain <root>` | Show stats summary for a stored domain |
| `findings <root>` | Show all stored findings for a domain |
| `runs [root]` | Show recent stored runs |
| `add <root> <file>` | Import and merge findings from a text file |
| `add domain <root> <file>` | Legacy-style alias for the above |
| `export <root> <path> [txt\|json\|html]` | Export findings to a file |
| `delete <root>` | Delete a domain and all its findings |
| `resources` | List resource catalog with auth markers |
| `config` | Show active config and database paths |
| `update` | Update Subdominator to the latest version |
| `release` | Show release notes for the latest version |
| `clear` | Clear the terminal |
| `exit` / `quit` | Exit the shell |

**Resource auth markers in `resources` output:**
- `*` — API key required
- `~` — API key optional (works without, more results with)
- `-` — No auth needed

---

## Output Formats

### Plain text (default)

One subdomain per line. Pipe-safe. Use `-o results.txt` to save.

```
api.example.com
mail.example.com
dev.example.com
```

### JSONL stream (`-j`)

Newline-delimited JSON, one finding per line. Designed for `jq`, `grep`, and pipeline tools.

```json
{"domain":"example.com","subdomain":"api.example.com","resource":"shodan"}
{"domain":"example.com","subdomain":"mail.example.com","resource":"crtsh"}
```

### HTML report (`-oh report.html`)

A full standalone HTML report. Requires the `jinja2` optional dependency (`pip install "subdominator[reports]"`).

### Summary (`-ss`)

Prints a run summary table showing per-resource finding counts, duration, and errors.

### Database (`-sd`)

Saves all findings to SQLite at `~/.local/share/subdominator/subdominator.db`. Query and export from the `--shell`.

---

## Providers

73 sources total. Auth column: **`key`** = API key required, **`optional`** = works without a key (more results with one), **`free`** = no auth needed.

> Sources marked † are **disabled by default** (slow or heavily rate-limited). Include them with `--all` or `-ir <name>`.

### Free (no auth)

| Name | URL | Notes |
|---|---|---|
| `abuseipdb` | https://abuseipdb.com/ | |
| `anubis` | https://jldc.me/anubis | |
| `commoncrawl` † | https://index.commoncrawl.org/ | Slow, large dataset |
| `crtsh` | https://crt.sh | Certificate Transparency |
| `cyfare` | https://cyfare.net/ | |
| `digitorus` | https://www.digitorus.com/ | |
| `hackertarget` | https://hackertarget.com/ | |
| `hudsonrock` | https://cavalier.hudsonrock.com/ | |
| `myssl` | https://myssl.com | |
| `racent` | https://face.racent.com/ | |
| `rapiddns` | https://rapiddns.io/ | |
| `reconcloud` | https://recon.cloud/ | |
| `riddler` | https://riddler.io/ | |
| `shrewdeye` | https://shrewdeye.app/api | |
| `sitedossier` | https://www.sitedossier.com/ | |
| `shodanx` | https://github.com/RevoltSecurities/Shodanx | |
| `thc` | https://thc.org/ | |
| `threatcrowd` | https://threatcrowd.org/ | |
| `threatminer` | https://www.threatminer.org/ | |
| `waybackarchive` † | https://archive.org/wayback | Very slow |

### Optional API key

| Name | URL | Notes |
|---|---|---|
| `alienvault` | https://otx.alienvault.com | More results with key |
| `reconeer` | https://www.reconeer.com/ | More results with key |
| `submd` | https://api.sub.md/ | More results with key |

### Requires API key

| Name | URL | Auth notes |
|---|---|---|
| `argosdns` | https://www.argosdns.io | API key |
| `arpsyndicate` | https://www.arpsyndicate.io/pricing.html | API key |
| `bevigil` | https://bevigil.com/login | API key |
| `binaryedge` | https://binaryedge.io/ | API key |
| `bufferover` | https://tls.bufferover.run/ | API key |
| `builtwith` | https://api.builtwith.com/domain-api | API key |
| `c99` | https://subdomainfinder.c99.nl/ | API key |
| `censys` | https://censys.com/ | `id:secret` pair |
| `certspotter` | https://sslmate.com/certspotter/ | API key |
| `chaos` | https://chaos.projectdiscovery.io/ | API key |
| `chinaz` | http://my.chinaz.com/ChinazAPI/DataCenter/MyDataApi | API key |
| `coderog` | https://rapidapi.com/coderog-coderog-default/api/subdomain-finder5/pricing | RapidAPI key (alias: `rapidapi`) |
| `digitalyama` | https://digitalyama.com/ | API key |
| `dnsdb` | https://api.dnsdb.info | API key |
| `dnsdumpster` | https://dnsdumpster.com/ | API key |
| `domainsproject` | https://domainsproject.org/ | API key |
| `domscan` | https://domscan.net | API key |
| `dnsrepo` | https://dnsarchive.net/ | API key |
| `driftnet` | https://driftnet.io/ | API key |
| `facebook` | https://developers.facebook.com/ | App ID + Secret |
| `fofa` | https://en.fofa.info/ | `email:key` pair |
| `fullhunt` | https://fullhunt.io/ | API key |
| `github` † | https://github.com/ | Personal Access Token |
| `google` | https://programmablesearchengine.google.com/controlpanel/create | `cx:key` pair |
| `huntermap` | https://hunter.how/ | API key |
| `intelx` | https://intelx.io/ | API key |
| `leakix` | https://leakix.net/ | API key |
| `merklemap` | https://www.merklemap.com/ | API key |
| `netlas` | https://netlas.io/ | API key |
| `odin` | https://odin.io/ | API key |
| `onyphe` | https://www.onyphe.io/ | API key |
| `profundis` | https://api.profundis.io/ | API key |
| `pugrecon` | https://pugrecon.com/ | API key |
| `quake` | https://quake.360.cn/ | API key |
| `rapidapi` | https://rapidapi.com/hub | API key (shared by `coderog`, `rapidfinder`, `rapidscan`) |
| `rapidfinder` | https://rapidapi.com/Glavier/api/subdomain-finder3/pricing | RapidAPI key (alias: `rapidapi`) |
| `rapidscan` | https://rapidapi.com/sedrakpc/api/subdomain-scan1/pricing | RapidAPI key (alias: `rapidapi`) |
| `redhuntlabs` | https://devportal.redhuntlabs.com/ | API key |
| `robtex` | https://proapi.robtex.com/ | API key |
| `rsecloud` | https://rsecloud.com/search | API key |
| `securitytrails` | https://securitytrails.com/ | API key |
| `shodan` | https://shodan.io/ | API key |
| `threatbook` | https://threatbook.cn/ | API key |
| `trickest` | https://trickest.io/ | API key |
| `urlscan` | https://urlscan.io/ | API key |
| `virustotal` † | https://virustotal.com/ | API key |
| `whoisfreaks` | https://whoisfreaks.com/ | API key |
| `whoisxml` | https://whoisxmlapi.com/ | API key (alias: `whoisxmlapi`) |
| `windvane` | https://windvane.lichoin.com/ | API key |
| `zoomeyeapi` | https://www.zoomeye.hk/ | API key (alias: `zoomeye`) |

---

## Docker

Pre-built images are published to the GitHub Container Registry on every release.

**Pull and scan:**
```bash
docker run --rm -it ghcr.io/revoltsecurities/subdominator:latest -d example.com
```

**Save output to the current directory:**
```bash
docker run --rm -it \
  -v $(pwd):/output \
  ghcr.io/revoltsecurities/subdominator:latest \
  -d example.com -o /output/results.txt
```

**Use a custom provider config:**
```bash
docker run --rm -it \
  -v /path/to/config:/config \
  ghcr.io/revoltsecurities/subdominator:latest \
  -cp /config/provider-config.yaml -d example.com
```

**Build the image locally:**
```bash
docker build -t subdominator -f Docker/Dockerfile .
```

---

## Development

```bash
git clone https://github.com/RevoltSecurities/Subdominator.git
cd Subdominator
uv sync --group dev
python -m pytest tests/ -v
```

**Build a distribution:**
```bash
uv build
```

**Project structure:**
```
src/subdominator/
├── cli/          # app.py (entry point), shell.py (audit shell)
├── core/         # models, settings, constants, provider_config
├── http/         # retryable.py (aiohttp wrapper)
├── output/       # reports.py (HTML), writers
├── resources/
│   ├── base.py       # BaseResource
│   ├── catalog.py    # RESOURCE_CATALOG (73 entries)
│   ├── registry.py   # ResourceRegistry + DEFAULT_DISABLED_RESOURCES
│   └── providers/    # 73 individual provider modules
├── services/     # enumerator.py (async orchestration)
└── storage/      # database.py, repository.py (SQLite)
```

---

## Security

Subdominator performs **passive** reconnaissance only — it queries public APIs and datasets and does not send traffic directly to the target. No self-updates happen without explicit `--update` / shell `update` command. All HTTP interactions go through the `RetryableHttpClient` which logs requests at debug level.

---

## License

MIT © [RevoltSecurities](https://github.com/RevoltSecurities)

Built with care by the RevoltSecurities team. If Subdominator helps your work, a ⭐ on GitHub goes a long way.
