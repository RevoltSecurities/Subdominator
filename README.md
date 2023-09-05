## Subdominator - Unleash the Power of Subdomain Enumeration

Subdominator is a powerful tool for passive subdomain enumeration during bug hunting and reconnaissance processes. It is designed to help researchers and cybersecurity professionals discover potential security vulnerabilities by efficiently enumerating subdomains.

### Latest release Installation:
1. **Download the Release**: Visit the [Releases](https://github.com/sanjai-AK47/Subdominator/releases) page and download the latest release (`SubdominatorV1.0.2.zip`).

2. **Extract Files**: Extract the downloaded ZIP file to your desired location.

3. **Run Subdominator**:

   - **Python Script**: If you prefer to run the Python script, navigate to the extracted directory and execute the following command:
     
     ```bash
     python3 subdominator.py -h
     ```

   - **Linux Executable**: If you prefer to use the Linux executable, navigate to the extracted directory and execute the following command:
     
     ```bash
     ./subdominator -h
     ```
# Note for old version Linux Users:

### Delete old version of Subdominator for Linux Executable file

```bash

sudo rm /usr/local/bin/subdominator

```

## After deleting the old version of Subdominator you can install the Linux binary of latest version of Subdominator


### Abilities Of Subdominator Version1.0.3

- Now The Subdominator configuration yaml file  can store unlimited api keys for some services

- OSINT mode bug fixed

- It have recursive mode when user enables the mode it enumerate recursively for wild cards

- Now Subdominator can enumerate Subdomains for domains in a text file

- New Mode Introduced for User, That Subdominator can now send notification to your pc or mobile

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

cd Subdominator

pip install -r requirements.txt

sudo mv subdominator /usr/local/bin/

subdominator -h
```

## Subdominator Usage:

   ``` bash

      Subdominator is a powerful tool for subdomain enumeration. You can use it with various options to customize your subdomain discovery process.

     usage: subdominator.py [-h] [-d DOMAIN] [-dL DOMAINS_LIST] [-nt] [-r] [-vrs] [-cf] [-o OUTPUT]

    Subdominator Unleash the Power of Subdomain Enumeration

Options:

  -h, --help                   Show this help message and exit

  -d DOMAIN, --domain DOMAIN                     Specify the target domain to find subdomains

  -dL DOMAINS_LIST, --domains-list DOMAINS_LIST  Provide a filename containing a list of domains to find subdomains

  -nt, --notify     Notification                 Send push notifications to your Android Phone or Desktop when Subdominator has finished its process

  -r, --recursive   Recursive Enumeration        Enable recursive enumeration for wildcards in found subdomains

  -vrs, --version   Version                      Check for the latest version of Subdominator

  -cf, --config     Configuration Mode          Find subdomains with the configured API keys

  -o OUTPUT, --output OUTPUT                    Specify the filename to save the output

   ```

## [INFO]: Enabling the notification mode can help you When Subdominator do enumeration for list of domains or in recursive mode


## Dont forget to configure your yaml file with api keys:


## Setup for Notification !:

Set up a Pushbullet account on your PC and Phone
    
For PC
        
   Go to [Pushbullet.com](https://www.pushbullet.com/)
            
   Create an account

   Get a api key and paste in Pushbullet-Notify in configuration yaml file

   Add the extension to your PC with the Pushbullet Extension regarding to your browser
            
For Phone
      
   Install the Pushbullet app on your phone.
        
   Log in using the same email address that you used to log in to your PC !.
        

### New updated yaml file:

```yaml
Virustotal: # Unlimited keys
  - # Your Virustotal API Key here

  - # Your Virustotal API Key here

  - # Your Virustotal API Key here

Chaos: # Unlimited or Limited keys - Your choice

  - # Your Chaos API Key here

  - # Another Chaos API Key here

Dnsdumpter: # Limited token and cookie

  csrf_cookie: # Your Dnsdumpter CSRF Cookie here

  csrf_token: # Your Dnsdumpter CSRF Token here

Whoisxml: # Unlimited keys

  - # Your Whoisxml API Key here

  - # Another Whoisxml API Key here

SecurityTrails: # Unlimited keys

  - # Your SecurityTrails API Key here

  - # Another SecurityTrails API Key here

Bevigil: # Unlimited keys

  - # Your Bevigil API Key here

  - # Another Bevigil API Key here

  - # Yet another Bevigil API Key here

Binaryedge: # Unlimited keys

  - # Your Binaryedge API Key here

  - # Another Binaryedge API Key here

  - # Yet another Binaryedge API Key here

Rapidapi: # Unlimited keys

  - # Your Rapidapi Key here

  - # Another Rapidapi Key here

Bufferover: # Unlimited keys

  - # Your Bufferover API Key here

  - # Another Bufferover API Key here

Certspotter: # Unlimited keys

  - # Your Certspotter API Key here

  - # Another Certspotter API Key here

Censys: # Limited Keys and ids

  api_secret_id: # Your Censys API Secret ID here

  api_secret_key: # Your Censys API Secret Key here

Fullhunt: # Unlimited keys

  - # Your Fullhunt API Key here

  - # Another Fullhunt API Key here

  - # Yet another Fullhunt API Key here

Leakix: # Unlimited keys

  - # Your Leakix API Key here

  - # Another Leakix API Key here

Netlas: # Unlimited keys

  - # Your Netlas API Key here

  - # Another Netlas API Key here

Zoomeye-API: # Unlimited keys

  - # Your Zoomeye-API Key here

Zoomeye-Auth: # Limited

  email: # Your Zoomeye Authentication Email here

  password: # Your Zoomeye Authentication Password here


Pushbullet-Notify: # Limited
  - # Your Pushbullet API Key here
```

#### Please make sure to replace `#your_api_key_here` with the respective API keys and replace the `email` with your api email and `password` api passoword you obtain from the corresponding websites.

### Set the Unlimited api keys Where its commented can holds Unlimited api keys


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


### OSINT Mode

If you choose not to use the config mode, Subdominator will automatically switch to non-config mode. In this mode, Subdominator will make use of available public resources to collect a sufficient number of subdomains for your bug hunting needs.

## OSINT example image
![Screenshot from 2023-07-24 22-22-37](https://github.com/sanjai-AK47/Subdominator/assets/119435129/1eda42cd-8547-4b39-b548-18687479122f)


![Screenshot from 2023-07-24 22-22-17](https://github.com/sanjai-AK47/Subdominator/assets/119435129/f28462ce-dac8-47d6-a7a0-66d0bde1f373)



Happy bug hunting with Subdominator! If you have any suggestions or feedback, feel free to contribute or open an issue on our GitHub repository: [Subdominator GitHub Repository](https://github.com/sanjai-AK47/Subdominator)
