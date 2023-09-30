## Subdominator - Unleash the Power of Subdomain Enumeration

Subdominator is a powerful tool for passive subdomain enumeration during bug hunting and reconnaissance processes. It is designed to help researchers and cybersecurity professionals discover potential security vulnerabilities by efficiently enumerating subdomains.

### Latest release Installation:

#### Method 1:

```bash
git clone https://github.com/sanjai-AK47/Subdominator.git

cd Subdominator

pip install subdominator

subdominator -h

```
## Dont Worry if the above installation failed there another method also there for you

#### Method2:

```bash
git clone https://github.com/sanjai-AK47/Subdominator.git
cd Subdominator
pip install .
subdominator -h

```

# Note for old version Linux Users:

### Delete old version of Subdominator for Linux Executable file

```bash

sudo rm /usr/local/bin/subdominator

```

## After deleting the old version of Subdominator you can install the  latest version of Subdominator with new Instructions mentioned above


### Abilities Of Subdominator Version1.0.4

- Subdominator have upgraded with concurrency which better more faster now than before

- Now The Subdominator configuration yaml file  can store unlimited api keys for all services

- OSINT domains file mode bug fixed

- Recursive mode logical errors have been fixed with concurrency

- Now Subdominator can enumerate Subdomains for domains in a text file with more concurrency


- Any OS users of subdominator can run the subdominator anywhere in their system
 
- Passive subdomain enumeration using multiple APIs and Open source interations

- Fast and comprehensive results for efficient bug hunting and for Information Gathering
 
- Easy-to-use with simple command-line options
 
- Config mode for loading API keys and custom configurations
 
- Automatic non-config mode if no custom configuration is provided

- Saving the results of Subdominator can be user defined or Subdominator will automatically saved the output
 
- Run The Subdominator excutable file anywhere and The configuration file be automatically detected in your machiene

### ALL Users Insatllation:

```bash

git clone https://github.com/sanjai-AK47/Subdominator.git

cd SubDominator

pip install subdominator or pip install .

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
Virustotal: #Unlimited keys                   [Note]: Users follow my instruction and syntax as same if u want add 1 or more keys for particular api services for this configuration file and Thankyou!
  
Chaos: #Unlimited keys

  - # Insert your Chaos API key here
  
Dnsdumpter:  #Unlimited keys and tokens


  - # Csrf_Cookie:Csrf_Token

Whoisxml: #Unlimited keys

  - # Insert your Whoisxml API key here
  
SecurityTrails: #Unlimited keys

  - # Insert your SecurityTrails API key here
  
Bevigil: #Unlimited keys 

  - # Insert your Bevigil API keys
  
Binaryedge: #Unlimited keys

  - # Insert your Binaryedge API key here
  
Rapidapi: #Unlimited keys

  - # Insert your Rapidapi API key here
  
Redhunt: #Unlimited keys 

  - # Insert your Redhunt API key here
  
Bufferover: #Unlimited keys 

  - # Insert your Bufferover API key here
  
Certspotter: #Unlimited keys 

  - # Insert your Certspotter API key here
  
Censys: #Unlimited censys-id and key as you want

  - # Censys_API_ID:Censys_Secret_Token 
  
Fullhunt: #Unlimited keys

  - # Insert your Fullhunt API key here
  
Leakix: #Unlimited keys

  - # Insert your Leakix API key here
  
Netlas: #Unlimited keys

  - # Insert your Netlas API key here
  
Zoomeye-API: #Unlimited keys

  - # Insert your Zoomeye API key here
  
Zoomeye-Auth: #Unlimited as u want

  - # your_zoomeye_email:your_zoomeye_password
  
Pushbullet-Notify: #limited keys is enough for pushbullet

  - # Insert your Pushbullet Notify key here
```

#### Please make sure to replace `#your_api_key_here` with the respective API keys and replace the `email` with your api email and `password` api passoword you obtain from the corresponding websites.

### Set the Unlimited api keys Where its commented can holds Unlimited api keys


## New Changes in yaml file

```bash
[Note]: Users follow my instruction and syntax as same if u want add 1 or more keys for particular api services for this configuration file and Thankyou!
  
Dnsdumpter:  #Unlimited keys and tokens


  - # Csrf_Cookie:Csrf_Token

Redhunt: #Unlimited keys 

  - # Insert your Redhunt API key here
  
Censys: #Unlimited censys-id and key as you want

  - # Censys_API_ID:Censys_Secret_Token 

  
Zoomeye-Auth: #Unlimited as u want

  - # your_zoomeye_email:your_zoomeye_password

```

## [INFO]: Observe the change that for token, cookie, censys id and api, zoomeye auths are now changed so we can store unlimited keys and configuration and it will make easy and no more configuration after that . Which means spending time with configuration of api keys helps you in future



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
- **Redhunt**: [Redhunt](https://https://devportal.redhuntlabs.com/)


### Dnsdumpter:

Dnsdumpster requires csrf token and cookie to obtain it visit **Dnsdumpter**: [Dnsdumpster](https://dnsdumpster.com)

Search any domain and Intercept the requests your burp that contains token and cookie. Copy that and paste in your yaml file

Example Image:
  
![Screenshot from 2023-07-24 21-47-10](https://github.com/sanjai-AK47/Subdominator/assets/119435129/d0aa5316-7698-4942-9512-2b3c3dc0a007)

After this all things you can run the Subdominator efficiently for subdomain enumeration


### Config Mode

Subdominator offers a convenient config mode that allows you to use your configured API keys and custom settings. You can enable the config mode by using the `--config` flag with the Subdominator command.

```bash
subdominator -d target.com --config
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
