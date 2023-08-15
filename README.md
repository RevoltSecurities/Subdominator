## Subdominator - Unleash the Power of Subdomain Enumeration

Subdominator is a powerful tool for passive subdomain enumeration during bug hunting and reconnaissance processes. It is designed to help researchers and cybersecurity professionals discover potential security vulnerabilities by efficiently enumerating subdomains.

### Latest release Installation:
1. **Download the Release**: Visit the [Releases](https://github.com/sanjai-AK47/Subdominator/releases) page and download the latest release (`SubdominatorV1.0.1.zip`).

2. **Extract Files**: Extract the downloaded ZIP file to your desired location.

3. **Run Subdominator**:

   - **Python Script**: If you prefer to run the Python script, navigate to the extracted directory and execute the following command:
     
     ```bash
     python subdominator.py
     ```

   - **Linux Executable**: If you prefer to use the Linux executable, navigate to the extracted directory and execute the following command:
     
     ```bash
     ./subdominator
     ```


### Features Of Version1.0.1

- Provided Linux executable file to execute anywhere in your Linux machiene
- Passive subdomain enumeration using multiple APIs and Open source interations
- Fast and comprehensive results for efficient bug hunting and for Information Gathering
- Easy-to-use with simple command-line options
- Config mode for loading API keys and custom configurations
- Automatic non-config mode if no custom configuration is provided
- Saving the results of Subdominator can be user defined or Subdominator will automatically saved the output
- Run The Subdominator excutable file anywhere and The configuration file be automatically detected in your machiene
- Linux Users can also run the executable of subdominator or directly run the Subominator python script directly
- Dont worry if your not a Linux users because Other users can also run the Subdominator python script

### Other Users Insatllation:

```bash
cd $HOME
git clone https://github.com/sanjai-AK47/Subdominator.git
cd SubDominator
pip install -r requirements.txt
python3 subdominator.py --help
```

### Linux Users Installation for Executable file:
```bash
cd $HOME
git clone https://github.com/sanjai-AK47/Subdominator.git
cd SubDominator
pip install -r requirements.txt
mv subdominator /usr/local/bin/
subdominator -h
```

## Dont forget to configure your yaml file with api keys:


### Configure the config_keys.yaml file:

```yaml
VirusTotal:

  api_key: #YOUR_VIRUS_TOTAL_API_KEY

Chaos:

  api_key: #YOUR_CHAOS_API_KEY

Dnsdumpter:

  csrf_cookie: #YOUR_DNSDUMPTER_CSRF_COOKIE

  csrf_token: #YOUR_DNSDUMPTER_CSRF_TOKEN

Whoisxml:

  api_key: #YOUR_WHOISXML_API_KEY

SecurityTrails:

  api_key: #YOUR_SECURITY_TRAILS_API_KEY

Bevigil:

  api_key: #YOUR_BEVIGIL_API_KEY

Binaryedge:

  api_key: #YOUR_BINARYEDGE_API_KEY

Fullhunt:

  api_key: #YOUR_FULLHUNT_API_KEY

Rapidapi:

  api_key: #YOUR_RAPIDAPI_API_KEY

Bufferover:

  api_key: #YOUR_BUFFEROVER_API_KEY

Certspotter:

  api_key: #YOUR_CERTSPOTTER_API_KEY

Censys:

  api_secret_id: #YOUR_CENSYS_API_SECRET_ID

  api_secret_key: #YOUR_CENSYS_API_SECRET_KEY

Leakix:

  api_key: #YOUR_LEAKIX_API_KEY

Netlas:

  api_key: #YOUR_NETLAS_API_KEY

Zoomeye:

  api_key: #YOUR_ZOOMEYE_API_KEY

  email: #YOUR_ZOOMEYE_EMAIL
  
  password: #YOUR_ZOOMEYE_PASSWORD

```

Please make sure to replace `#your_api_key_here` with the respective API keys you obtain from the corresponding websites.


### Information for Previous Users:

Save your old keys in some file then update the keys to the new config_keys.yaml file After updating your new version of  configuraton yaml file with respective api keys , id and email and passowords
Then you can delete the old version of yaml file.

### API Integrations and Credits

Subdominator integrates with various APIs to gather valuable subdomain information. We would like to give credit to the following websites for providing free-to-obtain API keys for subdomain enumeration.
Claim your free API keys here:

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
- **Certspotter**: [Certspotter](https://sslmate.com/certspotter)
- **Censys**: [Censys](https://search.censys.io/)
- **Fullhunt**: [Fullhunt](https://fullhunt.io/)
- **Zoomeye**: [Zoomeye](https://www.zoomeye.org/)
- **Netlas**: [Netlas](https://netlas.io/)
- **Leakix**: [Leakix](https://leakix.net/)


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
