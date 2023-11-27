## Subdominator - Unleash the Power of Subdomain Enumeration

Subdominator is a powerful tool for passive subdomain enumeration during bug hunting and reconnaissance processes. It is designed to help researchers and cybersecurity professionals discover potential security vulnerabilities by efficiently enumerating subdomains.

### Latest release Installation:

#### Method 1:

```bash

pip install subdominator

subdominator -h

```
copy the config_keys.yaml configuration file from Subdominator github repository if you dont have in your machiene

## Dont Worry if the above installation failed there another method also there for you

#### Method2:

```bash
git clone https://github.com/sanjai-AK47/Subdominator.git
cd Subdominator
pip install .
subdominator -h

```

### Features Of Subdominator Version1.0.5

- Subdominator resultings logic are improved

- Subdominator supports Output redirection to other tool that means supports oneliners for your Bug Bounty Reconnaissance

- Any OS users of subdominator can run the subdominator anywhere in their system

- Easy Installation Through pip and also for easy Tools management


### Oneliners with Subdominator:

Subdominator new features is it supports the onliners with other tools of [projectdiscovery](https://github.com/projectdiscovery) and My other tools [Subprober](https://github.com/sanjai-AK47/Subprober) and [httprober](https://github.com/sanjai-AK47/Httprober) to improver your reconnassaince with efficiently

```bash
subdominator -d apple.com -o subdominator_subdomains.txt -cf | httprober -c 50 | subprober --verbose --title --server --application-type --word-count  -c 20 -o subprober.txt --silent
```

Result Images:

![Screenshot from 2023-11-27 10-53-10](https://github.com/sanjai-AK47/Subdominator/assets/119435129/ba37eaf8-3baa-45a5-869e-6a497a270931)


### ALL Users Insatllation:

```bash

git clone https://github.com/sanjai-AK47/Subdominator.git

cd SubDominator

pip install subdominator or pip install .

subdominator -h
```


## Subdominator Usage:

   ``` bash

     [DESCRIPTION]: Subdominator is a powerful tool for subdomain enumeration. You can use it with various options to customize your subdomain discovery process.

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

[INFO]: Enabling the notification mode can help you When Subdominator do enumeration for list of domains or in recursive mode


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

  - #Insert your Virustotal API key here
  
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

Shodan: #Unlimited keys
  - Insert your Shodan API key here

Hunter: #Unlimited keys
  - Insert your Hunterhow API key here
  
Zoomeye-API: #Unlimited keys

  - # Insert your Zoomeye API key here
  
Zoomeye-Auth: #Unlimited as u want

  - # your_zoomeye_email:your_zoomeye_password
  
Pushbullet-Notify: #limited keys is enough for pushbullet

  - # Insert your Pushbullet Notify key here
```

#### Please make sure to replace `#your_api_key_here` with the respective API keys and replace the `email` with your api email and `password` api passoword you obtain from the corresponding websites.

### Set the Unlimited api keys Where its commented can holds Unlimited api keys

## Update your  yaml file if you are existing user:

```yaml

Shodan: #Unlimited keys
  - Insert your Shodan API key here


Hunter: #Unlimited keys
  - Insert your Hunterhow API key here

```


## New Changes in yaml file

```yaml
[Note]: Users follow my instruction and syntax as same if u want add 1 or more keys for particular api services for this configuration file and Thankyou!
  
Dnsdumpter:  #Unlimited keys and tokens

  - zsdqYb0rvIVYh2uPHo5Yk4EljV9GEK3579fdg70s9dflW37Q5pZl8pvQHUHWav:Z488dfiasugf89692356bRfLyBxuTytPjA17aa2yA5ULO8HySZoG6ptOKoY


Redhunt: #Unlimited keys 

  - VRp7HK3jWiRSnpPHo2rDWp09078074tv
  
Censys: #Unlimited censys-id and key as you want

  - d573246-2343e-4072344-8773249-174cd6a0:Rdf2rII6cqkQ93425934KfZzzJ2q 

  
Zoomeye-Auth: #Unlimited as u want

  - yourZoomeyeMail@gmail.com:ZoomeyePassword


```

[INFO]: To check your configuration file syntax is right check [here](https://onlineyamltools.com/validate-yaml) by pasting your config_keys.yaml file to avoid yaml keys arrangements and syntax errors

[INFO]: Observe the change that for token, cookie, censys id and api, zoomeye auths are now changed so we can store unlimited keys and configuration and it will make easy and no more configuration after that . Which means spending time with configuration of api keys helps you in future


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

  
### New Api Integrations and Credits:

- **Shodan** : [Shodan](https://shodan.io)
- **HunterHow** : [Hunter](https://hunter.how/)


### Dnsdumpter:

Dnsdumpster requires csrf token and cookie to obtain it visit **Dnsdumpter**: [Dnsdumpster](https://dnsdumpster.com)

Search any domain and Intercept the requests your burp that contains token and cookie. Copy that and paste in your yaml file

  
![Screenshot from 2023-07-24 21-47-10](https://github.com/sanjai-AK47/Subdominator/assets/119435129/d0aa5316-7698-4942-9512-2b3c3dc0a007)

## Information:

Subdominator a Subdomain enumeration tool builded for bug hunters and pentesters and other Cybersecurity people, it mainly builded for information gathering purpose
so [I'm](https://www.linkedin.com/in/d-sanjai-kumar-109a7227b/) not responsible for any illegal works  and also support the Subdominator project with 
a ⭐ and show your ❤️ and support guys!
Happy Hacking with Subdominator! If you have any suggestions or feedback, feel free to contribute or open an issue on our GitHub repository: [Subdominator GitHub Repository](https://github.com/sanjai-AK47/Subdominator) or can contact me through [LinkedIN](https://www.linkedin.com/in/d-sanjai-kumar-109a7227b/) for any issues or upgrades
