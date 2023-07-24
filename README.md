## Subdominator - Passive Subdomain Enumeration Tool

Subdominator is an open-source and powerful tool for passive subdomain enumeration during bug hunting and reconnaissance processes. It is designed to help researchers and cybersecurity professionals discover potential security vulnerabilities by efficiently enumerating subdomains.

### Features

- Passive subdomain enumeration using multiple APIs
- Fast and comprehensive results for efficient bug hunting
- Easy-to-use with simple command-line options
- Config mode for loading API keys and custom configurations
- Automatic non-config mode if no custom configuration is provided

### API Integrations and Credits

Subdominator integrates with various APIs to gather valuable subdomain information. We would like to give credit to the following websites for providing free-to-obtain API keys for subdomain enumeration:

- **VirusTotal**: [VirusTotal Website](https://www.virustotal.com)
- **Chaos**: [Chaos Website](https://chaos.projectdiscovery.io)
- **Dnsdumpter**: [Dnsdumpster Website](https://dnsdumpster.com)
- **Whoisxml**: [WhoisXML API Website](https://whois.whoisxmlapi.com)
- **SecurityTrails**: [SecurityTrails Website](https://securitytrails.com)
- **Bevigil**: [Bevigil Website](https://www.bevigil.com)
- **Binaryedge**: [BinaryEdge Website](https://binaryedge.io)
- **Fullhunt**: [Fullhunt Website](https://fullhunt.io)
- **Rapidapi**: [RapidAPI Website](https://rapidapi.com)
- **Bufferover**: [Bufferover Website](https://dns.bufferover.run)
- **Certspotter**: [Certspotter Website](https://sslmate.com/certspotter)

### Config Mode

Subdominator offers a convenient config mode that allows you to use your configured API keys and custom settings. You can enable the config mode by using the `--config` flag with the Subdominator command.

```bash
python3 subdominator.py -d target.com --config
```

### Non-Config Mode

If you choose not to use the config mode, Subdominator will automatically switch to non-config mode. In this mode, Subdominator will make use of available public resources to collect a sufficient number of subdomains for your bug hunting needs.

Happy bug hunting with Subdominator! If you have any suggestions or feedback, feel free to contribute or open an issue on our GitHub repository: [Subdominator GitHub Repository](https://github.com/sanjai-AK47/Subdominator)
