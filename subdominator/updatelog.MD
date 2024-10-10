# Subdominator V1.0.9 Update Log

## What's New?

### Bug Fixes & Enhancements

We’re excited to introduce **Subdominator V1.0.9**, featuring enhanced API passive resources and crucial bug fixes. This update resolves a false positive bug that affected users during recursive enumeration of subdomains. The root cause was traced to the **AbuseIPDB** and **ShodanX** sources. In this version, these sources will be excluded during recursive enumeration to ensure a smoother and more accurate experience.

### Key Updates:

- **Passive Resources:** 
  - Over **50 passive resources** available for asset discovery, with **6 new additions**.
  
- **Improved Asynchronous Performance:** 
  - Optimized to save time and enhance accuracy in results.

- **New Flags for Enhanced Functionality:**
  - **`-fw`, `--filter-wildcards`**: Filter out wildcard subdomains for cleaner output.
  - **`-s`, `--silent`**: Limit output to essential results without overriding `-ski` or `-sti` flags.
  - **`-oJ`, `--output-json`**: Output found subdomains in a JSON format to a specified file.

- **Stdin/Stdout Support:** 
  - Subdominator now supports reading from stdin and piping outputs to other tools, facilitating streamlined bug bounty workflows.

### Example Command:

Here's a sample command to enumerate subdomains, identify alive subdomains, and crawl them:

```bash
echo hackerone.com | subdominator -s | subprober -s -nc -c 75 | spideyx crawler -c 50 -pl 5 -ar -o crawler.txt -dept 10
```

### New Passive Resources:

We have added 6 new passive resources, bringing the total to over 50. The new resources are:

- [Builtwith](https://api.builtwith.com/domain-api)
- [Common Crawl](https://index.commoncrawl.org/)
- [Cyfare](https://cyfare.net)
- [Merklemap](https://www.merklemap.com)
- [PassiveTotal](https://api.riskiq.net/api/pdns_pt/#/)
- [Trickest](https://trickest.io/)
