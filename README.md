## Subdominator - Unleash the Power of Subdomain Enumeration

<h1 align="center">
  <img src="img/subdominator-v2.png" alt="Subdominator" width="450px">
  <br>
</h1>

<div align="center">

**lightweight , fast and more than a passive subdomain enumeration tool**

</div>


<p align="center">
  <a href="https://github.com/RevoltSecurities/Subdominator/tree/main#features">Features</a> |
  <a href="https://github.com/RevoltSecurities/Subdominator/tree/main#usage">Usage</a> |
  <a href="https://github.com/RevoltSecurities/Subdominator/tree/main#installation">Installation</a> |
  <a href="https://github.com/RevoltSecurities/Subdominator/tree/main#subdominator-documentation">Documentation</a>
</p>

<div align="center">
  
![GitHub last commit](https://img.shields.io/github/last-commit/RevoltSecurities/Subdominator) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/RevoltSecurities/Subdominator) [![GitHub license](https://img.shields.io/github/license/RevoltSecurities/Subdominator)](https://github.com/RevoltSecurities/Subdominator/blob/main/LICENSE)

</div>


Subdominator is a powerful tool for passive subdomain enumeration during bug hunting and reconnaissance processes. It is designed to help researchers and cybersecurity professionals discover potential security vulnerabilities by efficiently enumerating subdomains some various free passive resources.

### Features:
---

<h1 align="center">
        <img src="https://github.com/RevoltSecurities/Subdominator/assets/119435129/2a700962-6868-4a91-a8e8-2210189a4a23" width="700px">
        <br>
      </h1>

   - fast and powerfull to enumerate subdomains.
   - 50+ passive results to enumerate subdomains.
   - configurable API keys setup
   - integrated notification system
   - local Database support to store data
   - supports multiple output format (txt|html|pdf|json)

### Yaml Updates:
We request existing user to update their config yaml file with new resources by opening the config file in : ```$HOME/.config/Subdominator/provider-config.yaml``` and add the below resources:

```yaml
builwith:
  - your-api-key1
  - your-api-key2

passivetotal:
  - user-mail1:api-key1
  - user-mail2:api-key2

trickest:
  - your-api-key1
  - your-api-key2
```
by these your config yaml file will get updated or else check your yaml file that matches the below mentioned resources with *, The new users will required to update in next version if any new resources added
in Subdominator.


### Usage:
---
```code
subdominator -h
```
```yaml
              |          |                   _)                |
  __|  |   |  __ \    _` |   _ \   __ `__ \   |  __ \    _` |  __|   _ \    __|
\__ \  |   |  |   |  (   |  (   |  |   |   |  |  |   |  (   |  |    (   |  |
____/ \__,_| _.__/  \__,_| \___/  _|  _|  _| _| _|  _| \__,_| \__| \___/  _|


                     @RevoltSecurities



[DESCRIPTION]: Subdominator a passive subdomain enumeration that discovers subdomains for your targets using with passive and open source resources

[USAGE]:

    subdominator [flags]

[FLAGS]:

    [INPUT]:
    
        -d,   --domain                :  Target domain name for subdomain enumeration.
        -dL,  --domain-list           :  File containing multiple domains for bulk enumeration.
        stdin/stdout                  :  Supports input/output redirection.

    [OUTPUT]:
    
        -o,   --output                :  Save results to a file.
        -oD,  --output-directory      :  Directory to save results (useful when -dL is specified).
        -json, --json                 :  Output results in JSON format.
        
    [MODE]:
    
        -shell, --shell               :  Enable interactive shell mode to work with subdominator Database,generate report and etc.

    [OPTIMIZATION]:
    
        -t,   --timeout               :  Set timeout value for API requests (default: 30s).
        -fw,  --filter-wildcards      :  Filter out wildcard subdomains.

    [CONFIGURATION]:
    
        -cp,  --config-path           :  Custom config file path for API keys (default: /home/sanjai/.config/Subdominator/provider-config.yaml).
        -cdp, --config-db-path        :  Custom database config path (default: /home/sanjai/.cache/SubdominatorDB/subdominator.db).
        -nt,  --notify                :  Send notifications for found subdomains via Slack, Pushbullet.
        -px,  --proxy                 :  Use an HTTP proxy for debugging requests.
        -dork, --dork                 :  Use a custom google dork for google resource (ex: -ir google --dork 'site:target.com -www -dev intext:secrets')

    [RESOURCE CONFIGURATION]:
    
        -ir,  --include-resources     :  Specify sources to include (comma-separated).
        -er,  --exclude-resources     :  Specify sources to exclude (comma-separated).
        -all, --all                   :  Use all available sources for enumeration.

    [UPDATE]:
    
        -up,  --update                :  Update Subdominator to the latest version (manual YAML update required).
        -duc, --disable-update-check  :  Disable automatic update checks.
        -sup, --show-updates          :  Show the latest update details.

    [DEBUGGING]:
    
        -h,   --help                  :  Show this help message and exit.
        -v,   --version               :  Show the current version and check for updates.
        -s,   --silent                :  Show only subdomains in output.
        -ski, --show-key-info         :  Show API key errors (e.g., out of credits).
        -sti, --show-timeout-info     :  Show timeout errors for sources.
        -nc,  --no-color              :  Disable colorized output.
        -ls,  --list-source           :  List available subdomain enumeration sources.
        -V,   --verbose               :  Enable verbose output.
```


### Subdominator Integrations:
---

**The following API services used by subdominator**:  

- **AbuseIPDB** → [abuseipdb.com](https://abuseipdb.com)  
- **AlienVault** → [otx.alienvault.com](https://otx.alienvault.com)  
- **Anubis** → [jldc.me/anubis](https://jldc.me/anubis)  
- **ARP Syndicate** → [arpsyndicate.io](https://www.arpsyndicate.io/pricing.html)  
- **BeVigil** → [bevigil.com](https://bevigil.com/login)  
- **BinaryEdge** → [binaryedge.io](https://binaryedge.io)  
- **BufferOver** → [tls.bufferover.run](https://tls.bufferover.run/)  
- **BuiltWith** → [api.builtwith.com](https://api.builtwith.com/domain-api)  
- **C99** → [subdomainfinder.c99.nl](https://subdomainfinder.c99.nl/)  
- **Censys** → [censys.com](https://censys.com/)  
- **CertSpotter** → [sslmate.com/certspotter](https://sslmate.com/certspotter/)  
- **Chaos** → [chaos.projectdiscovery.io](https://chaos.projectdiscovery.io/)  
- **CodeRog** → [rapidapi.com/coderog](https://rapidapi.com/coderog-coderog-default/api/subdomain-finder5/pricing)  
- **CommonCrawl** → [index.commoncrawl.org](https://index.commoncrawl.org/)  
- **crt.sh** → [crt.sh](https://crt.sh)  
- **Cyfare** → [cyfare.net](https://cyfare.net)  
- **Digitorus** → [digitorus.com](https://www.digitorus.com/)  
- **DigitalYama** → [digitalyama.com](https://digitalyama.com/)  
- **DNSDumpster** → [dnsdumpster.com](https://dnsdumpster.com/)  
- **DNSRepo** → [dnsarchive.net](https://dnsarchive.net/)  
- **Fofa** → [en.fofa.info](https://en.fofa.info/)  
- **Facebook** → [developers.facebook.com](https://developers.facebook.com/)  
- **FullHunt** → [fullhunt.io](https://fullhunt.io/)  
- **Google** → [programmablesearchengine.google.com](https://programmablesearchengine.google.com/controlpanel/create)  
- **HackerTarget** → [hackertarget.com](https://hackertarget.com/)  
- **HudsonRock** → [cavalier.hudsonrock.com](https://cavalier.hudsonrock.com)  
- **HunterMap** → [hunter.how](https://hunter.how/)  
- **IntelX** → [intelx.io](https://intelx.io/)  
- **LeakIX** → [leakix.net](https://leakix.net/)  
- **MerkleMap** → [merklemap.com](https://www.merklemap.com)  
- **MySSL** → [myssl.com](https://myssl.com)  
- **Netlas** → [netlas.io](https://netlas.io/)  
- **Odin** → [odin.io](https://odin.io/)  
- **Quake** → [quake.360.cn](https://quake.360.cn/)  
- **Racent** → [face.racent.com](https://face.racent.com)  
- **RapidAPI** → [rapidapi.com/hub](https://rapidapi.com/hub)  
- **RapidDNS** → [rapiddns.io](https://rapiddns.io/)  
- **RedHuntLabs** → [devportal.redhuntlabs.com](https://devportal.redhuntlabs.com/)  
- **RSECloud** → [rsecloud.com/search](https://rsecloud.com/search)  
- **SecurityTrails** → [securitytrails.com](http://securitytrails.com/)  
- **Shodan** → [shodan.io](https://shodan.io)  
- **ShodanX** → [github.com/RevoltSecurities/Shodanx](https://github.com/RevoltSecurities/Shodanx)  
- **ShrewdEye** → [shrewdeye.app](https://shrewdeye.app/api)  
- **SiteDossier** → [sitedossier.com](https://sitedossier.com/)  
- **ThreatCrowd** → [ci-www.threatcrowd.org](http://ci-www.threatcrowd.org/)  
- **Trickest** → [trickest.io](https://trickest.io/)  
- **URLScan** → [urlscan.io](https://urlscan.io/)  
- **VirusTotal** → [virustotal.com](https://virustotal.com/)  
- **WaybackArchive** → [archive.org/wayback](https://archive.org/wayback)  
- **WhoisXML** → [whoisxmlapi.com](https://whoisxmlapi.com)  
- **ZoomEyeAPI** → [www.zoomeye.hk](https://www.zoomeye.hk/)  


### Installation:
---

Ensure you have **Python 3.12 or later** installed before proceeding with the installation. You can verify your Python version using:  

```bash
python3 --version
```

Subdominator core modules doesn't include PDF generation dependency, if you fancy a PDF report, use PDF extra tags when installing:
```bash
pipx install 'subdominator[PDF]'
```

#### ✅ **Install Subdominator from PyPI** (Recommended)  
The easiest way to install Subdominator is via PyPI:  

```bash
pip install --upgrade 'subdominator[PDF]'
```  

#### ✅ **Install the Latest Version from GitHub**  
To install the latest development version directly from GitHub:  

```bash
pip install --upgrade git+https://github.com/RevoltSecurities/Subdominator
```  

#### ✅ **Install Using PIPX** (For Isolated Environments)  
To avoid dependency conflicts, you can install Subdominator using `pipx`:  

```bash
pipx install 'subdominator[PDF]'
```  

To install the latest version from GitHub with `pipx`:  

```bash
pipx install 'subdominator[PDF] @ git+https://github.com/RevoltSecurities/Subdominator'
```  

#### ✅ **Install from Git Source** (For Development)  
For users who want to contribute or modify the tool, clone and install directly from source:  

```bash
git clone https://github.com/RevoltSecurities/Subdominator.git
cd Subdominator
pip install --upgrade pip
pip install -e . # or pip install -e ".[PDF]" to support PDF report generation
```  

After installation, you can verify if Subdominator is installed correctly by running:  

```bash
subdominator --help
```
### **SubDominator Documentation**  

For complete **post-installation configuration**, **shell interface tutorials**, and **detailed usage instructions**, please refer to the official SubDominator documentation:  

🔗 **[SubDominator Docs](https://subdominator-docs.streamlit.app/)**  

### **What You’ll Find in the Documentation:**  
✅ **Post Installation Setup** – Configure dependencies, API keys, and environment variables.  
✅ **Shell Interface Tutorial** – Learn how to use `subdominator -shell` for managing subdomains interactively.  
✅ **Enumeration Techniques** – Understand how to efficiently discover subdomains.  
✅ **Exporting & Reporting** – Generate reports in TXT, JSON, HTML, or PDF formats.  
✅ **Advanced Features & Flags** – Explore additional functionalities to enhance subdomain enumeration.  

For the best experience, ensure you follow the latest updates in the documentation! 🚀

### Security:
---

Subdominator is a promising tool that will never cause any threats to users or security researcher and its safe to use. Even without
Users permissions subdominator will not update itself and I welcome everyone who are intrested  contribute for Subdominator can create
their issues and report it.



### License:
---
Subdominator is built by [RevoltSecurities](https://github.com/RevoltSecurities) Team with ❤️ and your support will encourage us to improve the `subdominator` more and Community contributors are
Welcome  to contribute for subdominator and If you love the `subdominator` support it by giving a ⭐ .
