# Subdominator

Subdominator is a high-performance passive subdomain enumeration engine designed for precision threat hunting and massive-scale asset discovery. Rebuilt for modern security workflows, it leverages 70+ OSINT resources to map your target's attack surface in seconds.

## 🚀 Version 3 Highlights

- **Massive-Scale Scaling**: New disk-backed findings cache allows for 100k+ results with near-zero RAM usage.
- **Deep Reconnaissance**: Advanced recursive enumeration with configurable depth and concurrency.
- **Diagnostic Intelligence**: Integrated health-check engine to verify network connectivity and API status.
- **Rich Experience**: Powered by `RichParser` for beautiful CLI grouping and `RevoltLogger` for structured tracking.
- **Resilient Layer**: Custom `aiohttp` request engine with intelligent retries and session management.

## 🛠️ Installation

```bash
uv venv .venv --python 3.13
uv sync
. .venv/bin/activate
```

## 📖 Usage Examples

### Standard Enumeration
```bash
subdominator -d example.com --all
```

### Deep Recursive Scan
```bash
subdominator -d example.com -rd 2 --save-db -o results.txt
```

### Targeted Recon
```bash
subdominator -d example.com -ir crtsh,censys,shodan
```

### Health Diagnostics
```bash
subdominator --health-check
```

## ⌨️ Shorthand Flag Guide

| Flag | Description |
|---|---|
| `-d` / `-dL` | Target Domain / Domain List |
| `-sh` | Launch interactive shell |
| `-hc` | Run connectivity health check |
| `-rd` | Set recursion depth |
| `-ir` / `-er` | Include / Exclude specific resources |
| `-up` | Update to latest version |
| `-release` | Show latest release notes |
| `-nc` | Disable colored output |

## 📦 Features

- 73+ Passive OSINT Resource Adapters
- Multi-threaded Async Execution
- SQLite persistence (legacy compatible)
- JSON and Table-based Reporting
- Automatic Version Updates

---
Powered by **RevoltSecurities**
