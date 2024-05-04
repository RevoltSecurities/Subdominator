## Subdominator - Unleash the Power of Subdomain Enumeration

Subdominator is a powerful tool for passive subdomain enumeration during bug hunting and reconnaissance processes. It is designed to help researchers and cybersecurity professionals discover potential security vulnerabilities by efficiently enumerating subdomains some various free passive resources.

![GitHub last commit](https://img.shields.io/github/last-commit/RevoltSecurities/Subdominator) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/RevoltSecurities/Subdominator) [![GitHub license](https://img.shields.io/github/license/sanjai-AK47/Subprober)](https://github.com/RevoltSecurities/Subdominator/blob/main/LICENSE) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/d-sanjai-kumar-109a7227b/)

### Features:

   - fast and powerfull to enumerate subdomains.
   - 35+ passive results to enumerate subdomains.
   - configurable API keys setup
   - Integrated notification system

### Usage:
```code
subdominator -h
```
```yaml
                    __         __                       _                    __                
   _____  __  __   / /_   ____/ /  ____    ____ ___    (_)   ____   ____ _  / /_  ____    _____
  / ___/ / / / /  / __ \ / __  /  / __ \  / __ `__ \  / /   / __ \ / __ `/ / __/ / __ \  / ___/
 (__  ) / /_/ /  / /_/ // /_/ /  / /_/ / / / / / / / / /   / / / // /_/ / / /_  / /_/ / / /    
/____/  \__,_/  /_.___/ \__,_/   \____/ /_/ /_/ /_/ /_/   /_/ /_/ \__,_/  \__/  \____/ /_/     
                                                                                               

                     @RevoltSecurities


          
[DESCRIPTION]: Subdominator a passive subdomain enumeration that discovers subdomains for your targets using with passive and open source resources

[USAGE]: 

    subdominator [flags]
    
[FLAGS]: 

    [INPUT]: 
    
        -d,   --domain                  :  domain name to enumerate subdomains.
        -dL,  --domain-list             :  filename that contains domains for subdomain enumeration.
        stdout                          :  subdominator supports stdout to pipe its output
        
    [OUTPUT]: 
    
        -o,   --output                  :  filename to save the outputs.
        -oD,  --output-directory        :  directory name to save the outputs (use it when -dL is flag used).
        
    [OPTIMIZATION]: 
    
        -t,   --timeout                 : timeout value for every sources requests. 
    
    [Update]: 
    
        -up,   --update                 :  update subdominator for latest version but yaml source update required manual to not affect your api keys configurations.
        -duc, --disable-update-check    :  disable automatic update check for subdominator
        -sup, --show-updates            :  shows latest version updates of subdominator 
        
    [CONFIG]: 
    
        -nt,  --notify              :  send notification of found subdomain using source Slack, Pushbullet, Telegram, Discord
        -p,   --proxy               :  http proxy to use with subdominator (intended for debugging the performance of subdominator).
        -cp,  --config-path         :  custom path of config file for subdominator to read api keys ( default path: /home/sanjai/.config/Subdominator/provider-config.yaml)
        
    [DEBUG]: 
    
        -h,   --help                :  displays this help message and exits 
        -v,   --version             :  show current version of subdominator and latest version if available and exits
        -ske, --show-key-error      :  show keys error for out of credits and key not provided for particular sources
        -sre, --show-timeout-error  :  show timeout error for sources that are timeout to connect
        -nc,  --no-color            :  disable the colorised output of subdominator
        -ls,  --list-source         :  display the sources of subdominator uses for subdomain enumerations and exits (included for upcoming updates on sources).

```

### Subdominator Integrations:

Subdominator integrates with various free API passive sources to gather valuable subdomain information. We would like to give credit to the following websites for providing free-to-obtain API keys for subdomain enumeration.
Claim your free API keys here:
**Subdomains Resources**:
- **VirusTotal**: [VirusTotal](https://www.virustotal.com)
- **Chaos**: [Chaos](https://chaos.projectdiscovery.io)
- **Dnsdumpter**: [Dnsdumpster](https://dnsdumpster.com)
- **Whoisxml**: [WhoisXML](https://whois.whoisxmlapi.com)
- **SecurityTrails**: [SecurityTrails](https://securitytrails.com)
- **Bevigil**: [Bevigil](https://bevigil.com/)
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
- **Shodan** : [Shodan](https://shodan.io)
- **Huntermap** : [Hunter](https://hunter.how/)
- **Google**: [Google](https://developers.facebook.com/)
- **Facebook**: [Facebook](https://programmablesearchengine.google.com/controlpanel/create)
- **Quake**: [Quake](https://quake.360.cn/)
- **RapidFinder**: [RapidFinder](https://rapidapi.com/Glavier/api/subdomain-finder3/pricing)
- **RapidScan**: [RapidScan](https://rapidapi.com/sedrakpc/api/subdomain-scan1/pricing)

**Notification Resources**:
- **Slack**: [Slack](https://slack.com)
- **Pushbullet**: [Pushbullet](pushbullet.com/)


### Installation:

**Subdominator requires python latest version to be installed and with latest version `pip` commandline tool 
```code
pip install git+https://github.com/RevoltSecurities/Subdominator
```

### Post Installation setup:

`subdominator` can be used after installing successfully but if you want to use subdominator efficiently with its maximum level then some source requires API keys to setup and users can use this command:
```code
subdominator -ls`
``
```yaml
                    __         __                       _                    __                
   _____  __  __   / /_   ____/ /  ____    ____ ___    (_)   ____   ____ _  / /_  ____    _____
  / ___/ / / / /  / __ \ / __  /  / __ \  / __ `__ \  / /   / __ \ / __ `/ / __/ / __ \  / ___/
 (__  ) / /_/ /  / /_/ // /_/ /  / /_/ / / / / / / / / /   / / / // /_/ / / /_  / /_/ / / /    
/____/  \__,_/  /_.___/ \__,_/   \____/ /_/ /_/ /_/ /_/   /_/ /_/ \__,_/  \__/  \____/ /_/     
                                                                                               

                     @RevoltSecurities

[Version]: Subdominator current version v1.0.7 (latest)
[INFO]: Current Available free passive resources: [39]
[INFO]: Sources marked with an * needs API key(s) or token(s) configuration to works
[INFO]: Hey sanjai you can config your api keys or token here /home/sanjai/.config/Subdominator/provider-config.yaml to work
abuseipDB                                                                                                                                                                                                                                     
alienvault                                                                                                                                                                                                                                    
anubis                                                                                                                                                                                                                                        
bevigil*                                                                                                                                                                                                                                      
binaryedge*                                                                                                                                                                                                                                   
bufferover*                                                                                                                                                                                                                                   
censys*                                                                                                                                                                                                                                       
certspotter*                                                                                                                                                                                                                                  
chaos*                                                                                                                                                                                                                                        
columbusapi                                                                                                                                                                                                                                   
crtsh                                                                                                                                                                                                                                         
digitorus                                                                                                                                                                                                                                     
dnsdumpster*                                                                                                                                                                                                                                  
dnsrepo                                                                                                                                                                                                                                       
facebook*                                                                                                                                                                                                                                     
fullhunt*                                                                                                                                                                                                                                     
google*                                                                                                                                                                                                                                       
hackertarget                                                                                                                                                                                                                                  
huntermap*                                                                                                                                                                                                                                    
intelx*                                                                                                                                                                                                                                       
leakix*                                                                                                                                                                                                                                       
netlas*                                                                                                                                                                                                                                       
quake*                                                                                                                                                                                                                                        
rapidapi*                                                                                                                                                                                                                                     
rapiddns                                                                                                                                                                                                                                      
redhuntlabs*                                                                                                                                                                                                                                  
securitytrails*                                                                                                                                                                                                                               
shodan*                                                                                                                                                                                                                                       
shodanx                                                                                                                                                                                                                                       
shrewdeye                                                                                                                                                                                                                                     
sitedossier                                                                                                                                                                                                                                   
subdomaincenter                                                                                                                                                                                                                               
urlscan                                                                                                                                                                                                                                       
virustotal*                                                                                                                                                                                                                                   
waybackarchive                                                                                                                                                                                                                                
whoisxml*                                                                                                                                                                                                                                     
zoomeyeapi*                                                                                                                                                                                                                                   
rapidfinder*: Rapidfinder requires rapidapi api key but before it required to subscribe for free and please see here: https://rapidapi.com/Glavier/api/subdomain-finder3/pricing                                                              
rapidscan*  : Rapidscan requires rapidapi api key but before it required to subscribe for free and please see here: https://rapidapi.com/sedrakpc/api/subdomain-scan1/pricing       
```

here above we can see subdominator resources it uses and resource marked with an (*) need API keys to work and users can collect API keys from those websites and hyperlink will provided
for sources when using command `subdominator -ls` every source link provided as a hyperlink so place your cursor on sources will show the hyperlink on your terminal

### Keys configurations:

so we saw what are the resources are available for subdominator so now where to paste keys? it easy just see in your `~/$HOME/.config/Subdominator/provider-config.yaml` and all sourcess are available 
there, now paste your API keys and One more thing **Subdominator follow same keys setup syntax of subfinder and you refer** https://docs.projectdiscovery.io/tools/subfinder/install#post-install-configuration  **but before refering there is only one difference is for** `zoomeyeapi` in `subdominator` which in `subfinder` you need to give both host and key ex:
<br>
```yaml
zoomeyeapi:
   - zoomeye.hk:AudbAfjHslif_sudf
```
but in `subdominator` you should give only api keys not host for ex:
```yaml
zooeyeapi:
   - AudbAfjHslif_sudf
```
***Now lets come to other resources setup that varies from subfinder***:

   - Dnsdumpter Setup:
     
      ***Dnsdumpster requires csrf token and cookie to obtain it visit **Dnsdumpter**: [Dnsdumpster](https://dnsdumpster.com)
      Search any domain and Intercept the requests your burp that contains token and cookie. Copy that and paste in your yaml file**

      <h1 align="center">
        <img src="https://github.com/sanjai-AK47/Subdominator/assets/119435129/d0aa5316-7698-4942-9512-2b3c3dc0a007" width="700px">
        <br>
      </h1>

   - Google Setup:
     - Step 1: First login a google account in your browser
     - Step 2: Visit [here](https://programmablesearchengine.google.com/controlpanel/create) and create a search engine and choose all web option like below mentioned in images
        <h1 align="center">
        <img src="https://private-user-images.githubusercontent.com/119435129/273359357-7b871906-a08b-4473-bc47-31f797ae88f6.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTQ4MDg5NTMsIm5iZiI6MTcxNDgwODY1MywicGF0aCI6Ii8xMTk0MzUxMjkvMjczMzU5MzU3LTdiODcxOTA2LWEwOGItNDQ3My1iYzQ3LTMxZjc5N2FlODhmNi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwNTA0JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDUwNFQwNzQ0MTNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT04ODI0MzNhNzUwZWI0YzQ2ZDUyYTRmOWU1MDEzMjExNGQxYjAxNDNkZWY1NGVjNjA1YTYyMDRkZDQwZTgyNTQ3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.-4oyXpQwjgLoRfdgnRQgbrnz45j6rRVABSQ6jcGKCoo" width="700px">
        <br>
      </h1>
     - Step 3: After Creating your successfull search engine it time to copy your cx id 
     - Step 4: After completing these all process now its time to grab your api keys of google [here](https://developers.google.com/custom-search/v1/introduction)
     - Step 5: Press the get key button and create a new project with any name you want and click next
     - Step 6: After creating and completing your api key is generated and press show key then copy it
     - Step 7: Now its time to paste your google cx id and API key in yaml file
       ```yaml
       google
          #cxID:Apikey
          - 23892479:AIdjhakbkdiudgiao
       ```

**So you configured this different resources of subdominator, now follow the other steps to setting up API keys which I mentioned before here** https://github.com/RevoltSecurities/Subdominator/edit/main/README.md#keys-configurations
**Now After setting up your api keys your provider yaml file looks like**
```yaml
censys: 
  - 9f5a-be11-4b9e-9564-9596e78:Va92kyMYPS7ANKpI8CjV

facebook:
  - 1550699734936481:3b2eff7304659559380ad88d8c4b82f

google:
   - 34992b4aee9494e7b:AIzaSyCcEqqOERofbkudEY_iVC2_Wfv0A

intelx:
  - 2.intelx.io:1995e804-3c71-4938042-8042802-efa29ae2964d

zoomeyeapi:
   - 3833802-b9FF-6E1A5-7d2d-9792d64082adf
   - 6F28942CC-ACA5-573E8-d769-99b4c728042d

redhuntlabs: 
  - https://reconapi.redhuntlabs.com/community/v1/domains/subdomains:VRp7HK3jWiRSnpPfois7979spn4tvDVi0vM

dnsdumpster:
  - zsdqYb0rvIVYh2uPHo5Yk4EljV9GEKn44hDL9V2DFXznflW37Q5pZl8pvQHUHWav:Z488EzyPXVwDAhDGlm8gTBvkubRfLyBxuTytPjA17aa2yA5ULO8HySZoG6ptOKoY

```
Booyah ⚡ completed , now you can run `subdominator` with its maxiumum and wait for 2-4 minutes then you will have your results.

### Security:

Subdominator is a promising tool that will never cause any threats to users or security researcher and its safe to use. Even without
Users permissions subdominator will not update itself and I welcome everyone who are intrested  contribute for Subdominator can create
their issues and report it.

### License:
Subdominator is built by [RevoltSecurities](https://github.com/RevoltSecurities) Team with ❤️ and your support will encourage us to improve the `subdominator` more and Community contributors are
Welcome  to contribute for subdominator and If you love the `subdominator` support it by giving a ⭐ .



    



