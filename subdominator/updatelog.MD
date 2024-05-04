# Subdominator V1.0.7 updatelog 

**What's New?**

**Passive Resource Updates:**

**Subdominator  new updates is fully focus in performace and results in your subdomain enumeration process
and for that subdominator now updates with 35+ passive resources which utilized API keys and Open source data
and in Subdominator V1.0.7 below passive sources are added and each sources used to scrape subdomains from their
database and new API passive resources like google,facebook,quake enhance your subdomain results and new open source
resource Shodanx which uses shodan database to get subdomain from shodan without any API keys.**


- **New Passive Resourcess:**
    - [facebook](https://developers.facebook.com/)
    - [quake](https://quake.360.cn/)
    - [intelx](https://intelx.io/)
    - [google](https://programmablesearchengine.google.com/controlpanel/create)
    - [rapidfinder](https://rapidapi.com/Glavier/api/subdomain-finder3/pricing) : Rapidfinder is a source that utilizes the same rapidapi key but requires subscription and its free $0
    - [rapidscan](https://rapidapi.com/sedrakpc/api/subdomain-scan1/pricing)    : Rapiscan also utilizes same rapidapi key and with same price subscription required


- **New Flag Options:**

    - `-ls`, `--list-source` which are used to show the resources used subdominator
    - `-px`, `--proxy` which are used to to request via your proxy (ex: -px http://localhost:8080)

**Performance Enhancement Updates**

**Subdominator is now converted from traditional threading to asynchronous performance which subdominator uses python coroutines for concurrent request
by this subdominator utilizes it full resources and give you subdomains so for your results it may takes 1-3 minutes  if your internet speedis good and 
Subdominator utlizes open sources and passive resource where `subfinder` also didn't so by this you may see your results difference in both tools
and `subdominator` dont uses some sources that `subfinder` uses because subdominator is aim to give you good results from free API and Open sources so dont
worry still you will get more results that you didn't see it before and also Subdominator have integrated notification option which are **[slack](https://slack.com/intl/en-in/)** and **[pushbullet](https://pushbullet.com/)** so by these source you can pass your results via notification also.**

**Configuration Enhancement Updates**

**Previous Subdominator version read API keys from a file called `config_keys.yaml` but in this update of subdominator, the configuration system changes
to config path of your system for ex: `~/$HOME/.config/Subdominator/provider-config.yaml` and this is the path were new users and existing users
required to setup your API keys or else you can give your custom path to file using `-cf` or `--config-path` that follow keys syntax fot subdominator and
dont worry if you dont know setup your keys subdominator follows the same config syntax that `subfinder` follows but one difference is only for ***zoomeyeapi*** is
that subdominator users should give only keys and dont need host because subdominator automatically verify and use your api key for it.So now you know keys syntax
now where to get keys?, Its simple use command `subdominator -ls` which shows the resources and resources contains hyperlink for it and resources which marked with
an (*) requires API keys to work and your One time setup will is enough and some resources only needs to change keys if their usage is exhausted and dont worry if
any keys balance is exhausted subdominator will show and for that you need to enable  `-ski` or `--show-key-info`.

AHH ! done for now thats all but more to come so always look on for latest updates and Happy Hacking hackers!**
