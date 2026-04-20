## Subdominator - Unleash the Power of Subdomain Enumeration

<h1 align="center">
  <img src="static/subdominator-v2.png" alt="Subdominator" width="450px">
  <br>
</h1>

<div align="center">

**lightweight, fast and more than a passive subdomain enumeration tool**

</div>

<p align="center">
  <a href="#features">Features</a> |
  <a href="#usage">Usage</a> |
  <a href="#integrations">Integrations</a> |
  <a href="#installation">Installation</a> |
  <a href="https://subdominator-docs.streamlit.app/">Documentation</a>
</p>

<div align="center">
  
![GitHub last commit](https://img.shields.io/github/last-commit/RevoltSecurities/Subdominator) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/RevoltSecurities/Subdominator) [![GitHub license](https://img.shields.io/github/license/RevoltSecurities/Subdominator)](https://github.com/RevoltSecurities/Subdominator/blob/main/LICENSE)

</div>

Subdominator is a high-performance passive subdomain enumeration engine designed for precision threat hunting and massive-scale asset discovery. Rebuilt for modern security workflows, it leverages 73+ OSINT resources to map your target's attack surface in seconds.

### Features:
---

- **Massive-Scale Discovery**: Effortlessly handle 100K+ subdomains without system slowdowns. Our optimized architecture ensures massive scans remain fast and stable.
- **Recursive Subdomain Hunting**: Uncover hidden attack surfaces. Automatically scan newly discovered subdomains to find deep-seated assets other tools miss.
- **73+ Passive OSINT Sources**: Map your target using every major public data source—from Search Engines to Certificate Transparency logs.
- **Interactive Auditing Shell**: Manage your recon data like a pro. Search, filter, and audit historical findings within a powerful built-in terminal interface.
- **Professional Stakeholder Reporting**: Generate stunning, high-quality HTML reports for clients or stream structured JSONL data into your automation pipelines.
- **Instant Health Diagnostics**: No more guessing. Quickly verify your internet stability and API key status before launching complex enumeration runs.
- **Parallel High-Speed Execution**: Get comprehensive results in seconds. Subdominator is built from the ground up for speed, ensuring rapid feedback for your security audits.
- **Clean & Actionable Output**: Enjoy beautifully structured tables and clear logging that highlights exactly what matters most.

<h1 align="center">
        <img src="https://github.com/RevoltSecurities/Subdominator/assets/119435129/2a700962-6868-4a91-a8e8-2210189a4a23" width="700px">
        <br>
      </h1>

### Usage:
---

```bash
subdominator [flags]
```

```yaml
              |          |                   _)                |
  __|  |   |  __ \    _` |   _ \   __ `__ \   |  __ \    _` |  __|   _ \    __|
\__ \  |   |  |   |  (   |  (   |  |   |   |  |  |   |  (   |  |    (   |  |
____/ \__,_| _.__/  \__,_| \___/  _|  _|  _| _| _|  _| \__,_| \__| \___/  _|


                     @RevoltSecurities
```

#### **[INPUT CONFIGURATION]**:
| Flag | Short | Description |
|---|---|---|
| `--domain` | `-d` | Target domain for enumeration |
| `--domain-list` | `-dL` | File containing multiple domains for bulk enumeration |

#### **[RESOURCE CONFIGURATION]**:
| Flag | Short | Description |
|---|---|---|
| `--all` | | Use all available resources for enumeration |
| `--include-resources` | `-ir` | Specify sources to include (comma-separated) |
| `--exclude-resources` | `-er` | Specify sources to exclude (comma-separated) |
| `--list-resources` | `-ls` | List available subdomain enumeration sources |
| `--dork` | `-dk` | Custom search dork for supported resources (e.g., Google) |

#### **[RUNTIME CONFIGURATION]**:
| Flag | Short | Description |
|---|---|---|
| `--recursive-depth` | `-rd` | Recursively enumerate discovered subdomains (Default: 0) |
| `--concurrency` | `-c` | Number of concurrent resource executions (Default: 8) |
| `--timeout` | `-t` | Request timeout in seconds (Default: 20.0) |
| `--retries` | `-rt` | Number of retries for failed requests (Default: 3) |

#### **[OUTPUT CONFIGURATION]**:
| Flag | Short | Description |
|---|---|---|
| `--output` | `-o` | Save findings to a specific file |
| `--output-directory` | `-oD` | Directory to save bulk results (useful with -dL) |
| `--html` | `-oh` | Generate a high-quality HTML report |
| `--json` | `-j` | Write findings as a JSONL stream to stdout |
| `--table` | `-tb` | Print findings in a formatted terminal table |
| `--show-summary` | `-ss` | Print a detailed run summary after completion |

#### **[STORAGE & DIAGNOSTICS]**:
| Flag | Short | Description |
|---|---|---|
| `--shell` | `-sh` | Enable interactive shell mode for auditing and database management |
| `--save-db` | `-sd` | Persist findings to the SQLite database |
| `--health-check` | `-hc` | Verify internet connectivity and API status |
| `--update` | `-up` | Update Subdominator to the latest version |
| `--verbose` | `-v` | Enable verbose debug logging |
| `--no-color` | `-nc` | Disable colored output |

### Subdominator Integrations:
---

**The following API services are supported by Subdominator (73+ resources):**  

- **AbuseIPDB**, **AlienVault**, **Anubis**, **ArgosDNS**, **ArpSyndicate**, **BeVigil**, **BinaryEdge**, **BufferOver**, **BuiltWith**, **C99**, **Censys**, **CertSpotter**, **Chaos**, **ChinaZ**, **CodeRog**, **CommonCrawl**, **crt.sh**, **Cyfare**, **DigitalYama**, **Digitorus**, **DNSDB**, **DNSDumpster**, **DomScan**, **DNSRepo**, **DomainsProject**, **DriftNet**, **Fofa**, **Facebook**, **FullHunt**, **GitHub**, **Google**, **HackerTarget**, **HudsonRock**, **HunterMap**, **IntelX**, **LeakIX**, **MerkleMap**, **MySSL**, **Netlas**, **Odin**, **Onyphe**, **Profundis**, **PugRecon**, **Quake**, **Racent**, **RapidAPI**, **RapidFinder**, **RapidScan**, **RapidDNS**, **ReconCloud**, **Reconeer**, **RedHuntLabs**, **Riddler**, **Robtex**, **RSECloud**, **SecurityTrails**, **Shodan**, **ShodanX**, **ShrewdEye**, **SiteDossier**, **Submd**, **THC**, **ThreatBook**, **ThreatCrowd**, **ThreatMiner**, **Trickest**, **URLScan**, **VirusTotal**, **WaybackArchive**, **Windvane**, **WhoisFreaks**, **WhoisXML**, **ZoomEyeAPI**.


### Installation:
---

#### ✅ **🚀 Fast Global Install (Recommended)**  
The fastest way to install Subdominator as a global CLI tool is using `uv`:  

```bash
uv tool install subdominator
```  

#### ✅ **🐳 Docker Installation**  
The easiest way to use Subdominator in a container is by pulling the pre-built image from the **GitHub Container Registry (GHCR)**:  

**Pull & Run from GHCR:**  
```bash
# Scan a single domain
docker run --rm -it ghcr.io/revoltsecurities/subdominator:latest -d example.com

# Run and save output locally
docker run --rm -it -v $(pwd):/output ghcr.io/revoltsecurities/subdominator:latest -d example.com -o /output/results.txt
```  

**Build the Image Manually:**  
If you want to build the image yourself from the `Docker/Dockerfile`:  
```bash
docker build -t subdominator -f Docker/Dockerfile .
```  

**Usage with Custom Config:**  
```bash
docker run --rm -v /path/to/config:/config ghcr.io/revoltsecurities/subdominator:latest -cp /config/provider-config.yaml -d example.com
```  

#### ✅ **From PyPI**  
Traditional installation via `pip`:  

```bash
pip install --upgrade subdominator
```  

#### ✅ **From Source (Development)**  
```bash
git clone https://github.com/RevoltSecurities/Subdominator.git
cd Subdominator
uv sync  # or pip install -r requirements.txt
```  

### **Subdominator Documentation**  

For detailed configuration guides, shell interface tutorials, and advanced usage, visit our official documentation:  

🔗 **[Subdominator Documentation](https://subdominator-docs.streamlit.app/)**  

### Security:
---

Subdominator is a safe and transparent tool for security researchers. It does not perform any self-updates without user permission, and all network interactions are logged for auditing. We welcome contributions and issue reports from the community.

### License:
---
Subdominator is built by the [RevoltSecurities](https://github.com/RevoltSecurities) team with ❤️. If you find the tool useful, please support us by giving a ⭐ on GitHub!
