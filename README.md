## Subdominator - Passive Subdomain Enumeration Tool

Subdominator is an open-source and powerful tool for passive subdomain enumeration during bug hunting and reconnaissance processes. It is designed to help researchers and cybersecurity professionals discover potential security vulnerabilities by efficiently enumerating subdomains.

### Features

- Passive subdomain enumeration using multiple APIs
- Fast and comprehensive results for efficient bug hunting
- Easy-to-use with simple command-line options
- Config mode for loading API keys and custom configurations
- Automatic non-config mode if no custom configuration is provided

### Insatllation:

```bash
cd $HOME
git clone https://github.com/sanjai-AK47/Subdominator.git
cd SubDominator
pip install -r requirements.txt
python3 subdominator.py --help
```
### Configure the config_keys.yaml file:

```yaml
VirusTotal:
  api_key: #your_virustotal_api_key_here

Chaos:
  api_key: #your_chaos_api_key_here

Dnsdumpter:
  csrf_cookie: #your_dnsdumpter_csrf_cookie_here
  csrf_token: #your_dnsdumpter_csrf_token_here

Whoisxml:
  api_key: #your_whoisxml_api_key_here

SecurityTrails:
  api_key: #your_securitytrails_api_key_here

Bevigil:
  api_key: #your_bevigil_api_key_here

Binaryedge:
  api_key: #your_binaryedge_api_key_here

Fullhunt:
  api_key: #your_fullhunt_api_key_here

Rapidapi:
  api_key: #your_rapidapi_api_key_here

Bufferover:
  api_key: #your_bufferover_api_key_here

Certspotter:
  api_key: #your_certspotter_api_key_here
```

Please make sure to replace `#your_api_key_here` with the respective API keys you obtain from the corresponding websites.

### API Integrations and Credits

Subdominator integrates with various APIs to gather valuable subdomain information. We would like to give credit to the following websites for providing free-to-obtain API keys for subdomain enumeration

- **VirusTotal**: [VirusTotal](https://www.virustotal.com)
- **Chaos**: [Chaos](https://chaos.projectdiscovery.io)
- **Dnsdumpter**: [Dnsdumpster](https://dnsdumpster.com)
- **Whoisxml**: [WhoisXML](https://whois.whoisxmlapi.com)
- **SecurityTrails**: [SecurityTrails](https://securitytrails.com)
- **Bevigil**: [Bevigil](https://www.bevigil.com)
- **Binaryedge**: [BinaryEdge](https://binaryedge.io)
- **Fullhunt**: [Fullhunt](https://fullhunt.io)
- **Rapidapi**: [RapidAPI](https://rapidapi.com)
- **Bufferover**: [Bufferover](https://tls.bufferover.run/)
- **Certspotter**: [Certspotter Website](https://sslmate.com/certspotter)


### Dnsdumpter:

Dnsdumpster requires csrf token and cookie to obtain it visit **Dnsdumpter**: [Dnsdumpster](https://dnsdumpster.com)

Search any domain and Intercept the requests your burp that contains token and cookie. Copy that and paste in your yaml file

Example Image:
  
![Screenshot from 2023-07-24 21-47-10](https://github.com/sanjai-AK47/Subdominator/assets/119435129/d0aa5316-7698-4942-9512-2b3c3dc0a007)

After this all things you can run the Subdominator efficiently for subdomain enumeration


### Config Mode

Subdominator offers a convenient config mode that allows you to use your configured API keys and custom settings. You can enable the config mode by using the `--config` flag with the Subdominator command.

```bash
python3 subdominator.py -d target.com --config
```
## Config example image:

![Screenshot from 2023-07-24 22-18-53](https://github.com/sanjai-AK47/Subdominator/assets/119435129/01939ba0-b7fe-4153-98a4-a189234caf4c)


![Screenshot from 2023-07-24 22-18-35](https://github.com/sanjai-AK47/Subdominator/assets/119435129/4f394f9a-ff32-429b-9781-5a41a112e36f)


### Non-Config Mode

If you choose not to use the config mode, Subdominator will automatically switch to non-config mode. In this mode, Subdominator will make use of available public resources to collect a sufficient number of subdomains for your bug hunting needs.

## Non-Config example image
![Screenshot from 2023-07-24 22-22-37](https://github.com/sanjai-AK47/Subdominator/assets/119435129/1eda42cd-8547-4b39-b548-18687479122f)


![Screenshot from 2023-07-24 22-22-17](https://github.com/sanjai-AK47/Subdominator/assets/119435129/f28462ce-dac8-47d6-a7a0-66d0bde1f373)



Happy bug hunting with Subdominator! If you have any suggestions or feedback, feel free to contribute or open an issue on our GitHub repository: [Subdominator GitHub Repository](https://github.com/sanjai-AK47/Subdominator)
