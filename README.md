## Subdominator - Unleash the Power of Subdomain Enumeration

<h1 align="center">
  <img src="img/subdominator-v2.png" alt="Subdominator" width="450px">
  <br>
</h1>

Subdominator is a powerful tool for passive subdomain enumeration during bug hunting and reconnaissance processes. It is designed to help researchers and cybersecurity professionals discover potential security vulnerabilities by efficiently enumerating subdomains some various free passive resources.

![GitHub last commit](https://img.shields.io/github/last-commit/RevoltSecurities/Subdominator) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/RevoltSecurities/Subdominator) [![GitHub license](https://img.shields.io/github/license/RevoltSecurities/Subdominator)](https://github.com/RevoltSecurities/Subdominator/blob/main/LICENSE)

### Features:
---

<h1 align="center">
        <img src="https://github.com/RevoltSecurities/Subdominator/assets/119435129/2a700962-6868-4a91-a8e8-2210189a4a23" width="700px">
        <br>
      </h1>

   - fast and powerfull to enumerate subdomains.
   - 50+ passive results to enumerate subdomains.
   - configurable API keys setup
   - Integrated notification system


### Info:
We request existing user to update their config yaml file with new resources by opening the config file in : ```bash $HOME/.config/Subdominator/provider-config.yaml``` and add the below resources:

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

        -d,   --domain                  :  domain name to enumerate subdomains.
        -dL,  --domain-list             :  filename that contains domains for subdomain enumeration.
        stdin/stdout                    :  subdominator now supports stdin/stdout

    [OUTPUT]:

        -o,   --output                  :  filename to save the outputs.
        -oD,  --output-directory        :  directory name to save the outputs (use it when -dL is flag used).
        -oJ,  --output-json             :  filename to save output in json fromat

    [OPTIMIZATION]:

        -t,   --timeout                 :  timeout value for every sources requests.

    [UPDATE]:

        -up,   --update                 :  update subdominator for latest version but yaml source update required manual to not affect your api keys configurations.
        -duc, --disable-update-check    :  disable automatic update check for subdominator
        -sup, --show-updates            :  shows latest version updates of subdominator

    [CONFIG]:

        -nt,  --notify                  :  send notification of found subdomain using source Slack, Pushbullet, Telegram, Discord
        -p,   --proxy                   :  http proxy to use with subdominator (intended for debugging the performance of subdominator).
        -cp,  --config-path             :  custom path of config file for subdominator to read api keys ( default path: /home/sanjai/.config/Subdominator/provider-config.yaml)
        -fw,  --filter-wildcards        :  filter the found subdomains with wildcards and give cleaned output

    [DEBUG]:

        -h,   --help                    :  displays this help message and exits
        -s,   --silent                  :  show only subdomain in output (this is not included for -ski,-sti)
        -v,   --version                 :  show current version of subdominator and latest version if available and exits
        -ski, --show-key-info           :  show keys error for out of credits and key not provided for particular sources
        -ste, --show-timeout-info       :  show timeout error for sources that are timeout to connect
        -nc,  --no-color                :  disable the colorised output of subdominator
        -ls,  --list-source             :  display the sources of subdominator uses for subdomain enumerations and exits (included for upcoming updates on sources).

```


### Subdominator Integrations:
---

Subdominator integrates with various free and Paid API passive sources to gather valuable subdomain information. We would like to give credit to the following websites for providing free-to-obtain API keys for subdomain enumeration.
Claim your free API and Paid keys here:

**Subdomains Resources**:
- **VirusTotal***: [VirusTotal](https://www.virustotal.com)
- **Chaos***: [Chaos](https://chaos.projectdiscovery.io)
- **Dnsdumpster***: [Dnsdumpster](https://dnsdumpster.com)
- **Whoisxml***: [WhoisXML](https://whois.whoisxmlapi.com)
- **SecurityTrails***: [SecurityTrails](https://securitytrails.com)
- **Bevigil***: [Bevigil](https://bevigil.com/)
- **Binaryedge***: [BinaryEdge](https://binaryedge.io)
- **Fullhunt***: [Fullhunt](https://fullhunt.io)
- **Rapidapi***: [RapidAPI](https://rapidapi.com) (requires: Rapid api key) 
- **Bufferover***: [Bufferover](https://tls.bufferover.run/)
- **Certspotter***: [Certspotter](https://sslmate.com/certspotter)
- **Censys***: [Censys](https://search.censys.io/)
- **Fullhunt***: [Fullhunt](https://fullhunt.io/)
- **Zoomeye***: [Zoomeye](https://www.zoomeye.org/)
- **Netlas***: [Netlas](https://netlas.io/)
- **Leakix***: [Leakix](https://leakix.net/)
- **Redhunt***: [Redhunt](https://https://devportal.redhuntlabs.com/)
- **Shodan*** : [Shodan](https://shodan.io)
- **Huntermap*** : [Hunter](https://hunter.how/)
- **Google***: [Google](https://programmablesearchengine.google.com/controlpanel/create)
- **Facebook***: [Facebook](https://developers.facebook.com/)
- **Quake***: [Quake](https://quake.360.cn/)
- **RapidFinder***: [RapidFinder](https://rapidapi.com/Glavier/api/subdomain-finder3/pricing) (requires: Rapid api key)
- **RapidScan***: [RapidScan](https://rapidapi.com/sedrakpc/api/subdomain-scan1/pricing) (requires: Rapid api key)
- **Fofa***: [Fofa](https://en.fofa.info/)
- **CodeRog***: [CodeRog](https://rapidapi.com/coderog-coderog-default/api/subdomain-finder5/pricing) (requires: Rapid api key)
- **C99***: [C99](https://subdomainfinder.c99.nl/)
- **RSECloud***: [RSECloud](https://rsecloud.com/search)
- **Intelx***: [Intelx](intelx.io)
- **Builtwith***:[Builtwith](https://api.builtwith.com/domain-api)
- **Passivetotal***:[PassiveTotal](https://api.riskiq.net/api/pdns_pt/#/)
- **Trickest***:[Trickest](https://trickest.io/)

**Notification Resources**:
- **Slack**: [Slack](https://slack.com)
- **Pushbullet**: [Pushbullet](pushbullet.com/)


### Installation:
---

Subdominator requires python latest version to be installed and with latest version `pip` commandline tool 
```code
pip install git+https://github.com/RevoltSecurities/Subdominator --break-system-packages
```
and if any error occured with `httpx` package please use this command to install the tool:
```bash
pip install git+https://github.com/RevoltSecurities/Subdominator --no-deps httpx==0.25.2
```
you can also install the tool using **pipx** and install the latest version by using this command:
```bash
pipx install git+https://github.com/RevoltSecurities/Subdominator
```


### Post Installation setup:
---

`subdominator` can be used after installing successfully but if you want to use subdominator efficiently with its maximum level then some source requires API keys to setup and users can use this command:
```code
subdominator -ls
```
```yaml
                    __         __                       _                    __                
   _____  __  __   / /_   ____/ /  ____    ____ ___    (_)   ____   ____ _  / /_  ____    _____
  / ___/ / / / /  / __ \ / __  /  / __ \  / __ `__ \  / /   / __ \ / __ `/ / __/ / __ \  / ___/
 (__  ) / /_/ /  / /_/ // /_/ /  / /_/ / / / / / / / / /   / / / // /_/ / / /_  / /_/ / / /    
/____/  \__,_/  /_.___/ \__,_/   \____/ /_/ /_/ /_/ /_/   /_/ /_/ \__,_/  \__/  \____/ /_/     
                                                                                               

                     @RevoltSecurities

[Version]: Subdominator current version v2.0.0 (latest)
[INFO]: Current Available free passive resources: [51]
[INFO]: Sources marked with an * needs API key(s) or token(s) configuration to works
[INFO]: Hey sanjai you can config your api keys or token here /home/sanjai/.config/Subdominator/provider-config.yaml to work
abuseipDB
alienvault
anubis
bevigil*
binaryedge*
bufferover*
builtwith*
c99*
censys*
certspotter*
chaos*
columbusapi
commoncrawl
crtsh
cyfare
digitorus
dnsdumpster*
dnsrepo
fofa*
facebook*
fullhunt*
google*
hackertarget
huntermap*
intelx*
leakix*
merklemap
myssl
netlas*
passivetotal*
quake*
racent
rapidapi*
rapiddns
redhuntlabs*
rsecloud*
securitytrails*
shodan*
shodanx
shrewdeye
sitedossier
subdomaincenter
trickest*
urlscan
virustotal*
waybackarchive
whoisxml*
zoomeyeapi*
rapidfinder*: Rapidfinder requires rapidapi api key but before it required to subscribe for free and please see here: https://rapidapi.com/Glavier/api/subdomain-finder3/pricing
rapidscan*: Rapidscan requires rapidapi api key but before it required to subscribe for free and please see here: https://rapidapi.com/sedrakpc/api/subdomain-scan1/pricing
coderog*: Coderog source required to subscribe for free and please see here: https://rapidapi.com/coderog-coderog-default/api/subdomain-finder5/pricing
```

here above we can see subdominator resources it uses and resource marked with an (*) need API keys to work and users can collect API keys from those websites and hyperlink will provided
for sources when using command `subdominator -ls` every source link provided as a hyperlink so place your cursor on sources will show the hyperlink on your terminal

### Keys configurations:
---

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


**Now lets come to other resources setup that varies from subfinder**:
---

   - Google Setup:
     - Step 1: First login a google account in your browser
     - Step 2: Visit [here](https://programmablesearchengine.google.com/controlpanel/create) and create a search engine and choose all web option like below mentioned in images
        <h1 align="center">
        <img src="https://github.com/sanjai-AK47/GoogleDorker/assets/119435129/7b871906-a08b-4473-bc47-31f797ae88f6" width="700px">
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
- DnsDumpster:

    Subdominator V2.0.0 implements new changes in code and API key configurations of dnsdumpster and now       its super easy to setup the dnsdumpster with its API keys.
    
    - Step 1: First visit [dnsdumpster site](https://dnsdumpster.com) and register a new account
    - Step 2: After registering your account, you can find you dnsdumpster API key [here](https://dnsdumpster.com/my-account/)
    - Step 3: Copy the API keys and paste in the yaml file like we did before in previous versions and its looks like:
    ```yaml
    dnsdumpster:
        - z4gi42ifs9asdjbopakwbhorhao0du42po92jkbnkjbsdug082sjbkdhohabdaoiuboadhg
        - jdbsaoug0242kjblas42po92jkbnkjbsdug082sjbkdhohabadsjbudaugiuga98t24vi2u
    ```
    so after this you can run without any exceptions in subdominator.

**So you configured this different resources of subdominator, now follow the other steps to setting up API keys which I mentioned before here:** https://github.com/RevoltSecurities/Subdominator/edit/main/README.md#keys-configurations
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
  - z4gi42ifs9asdjbopakwbhorhao0du42po92jkbnkjbsdug082sjbkdhohabdaoiuboadhg

```
and dont forget to collect keys for updated resources, Booyah ⚡ completed , now you can run `subdominator` with its maximum and wait for 10-15 minutes then you will have your results.


### Security:
---

Subdominator is a promising tool that will never cause any threats to users or security researcher and its safe to use. Even without
Users permissions subdominator will not update itself and I welcome everyone who are intrested  contribute for Subdominator can create
their issues and report it.



### License:
---
Subdominator is built by [RevoltSecurities](https://github.com/RevoltSecurities) Team with ❤️ and your support will encourage us to improve the `subdominator` more and Community contributors are
Welcome  to contribute for subdominator and If you love the `subdominator` support it by giving a ⭐ .
