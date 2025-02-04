from colorama import Fore,Back,Style
import random
red =  Fore.RED
green = Fore.GREEN
magenta = Fore.MAGENTA
cyan = Fore.CYAN
mixed = Fore.RED + Fore.BLUE
blue = Fore.BLUE
yellow = Fore.YELLOW
white = Fore.WHITE
reset = Style.RESET_ALL
bold = Style.BRIGHT
colors = [ green, cyan, blue]
random_color = random.choice(colors)


def help(path):
    print(f"""
          
{bold}{white}[{reset}{bold}{blue}DESCRIPTION{reset}{bold}{white}]{reset}: {bold}{white}Subdominator a passive subdomain enumeration that discovers subdomains for your targets using with passive and open source resources{reset}

{bold}{white}[{reset}{bold}{blue}USAGE{reset}{bold}{white}]{reset}: {bold}{white}

    subdominator [flags]{reset}
    
{bold}{white}[{reset}{bold}{blue}FLAGS{reset}{bold}{white}]{reset}: {bold}{white}

    {bold}{white}[{reset}{bold}{blue}INPUT{reset}{bold}{white}]{reset}: {bold}{white}
    
        -d,   --domain                  :  domain name to enumerate subdomains.
        -dL,  --domain-list             :  filename that contains domains for subdomain enumeration.
        stdin/stdout                    :  subdominator now supports stdin/stdout
        
    {bold}{white}[{reset}{bold}{blue}OUTPUT{reset}{bold}{white}]{reset}: {bold}{white}
    
        -o,   --output                  :  filename to save the outputs.
        -oD,  --output-directory        :  directory name to save the outputs (use it when -dL is flag used).
        -oJ,  --output-json             :  filename to save output in json fromat
        
    {bold}{white}[{reset}{bold}{blue}SOURCE{reset}{bold}{white}]{reset}: {bold}{white}
    
        -sc,   --sources                 :  specify sources to use for enumeration (-sc crtsh,shodan).
        
    {bold}{white}[{reset}{bold}{blue}OPTIMIZATION{reset}{bold}{white}]{reset}: {bold}{white}
    
        -t,   --timeout                 :  timeout value for every sources requests. 
    
    {bold}{white}[{reset}{bold}{blue}UPDATE{reset}{bold}{white}]{reset}: {bold}{white}
    
        -up,   --update                 :  update subdominator for latest version but yaml source update required manual to not affect your api keys configurations.
        -duc, --disable-update-check    :  disable automatic update check for subdominator
        -sup, --show-updates            :  shows latest version updates of subdominator 
        
    {bold}{white}[{reset}{bold}{blue}CONFIG{reset}{bold}{white}]{reset}: {bold}{white}
    
        -nt,  --notify                  :  send notification of found subdomain using source Slack, Pushbullet, Telegram, Discord
        -p,   --proxy                   :  http proxy to use with subdominator (intended for debugging the performance of subdominator).
        -cp,  --config-path             :  custom path of config file for subdominator to read api keys ( default path: {path})
        -fw,  --filter-wildcards        :  filter the found subdomains with wildcards and give cleaned output
        
    {bold}{white}[{reset}{bold}{blue}DEBUG{reset}{bold}{white}]{reset}: {bold}{white}
    
        -h,   --help                    :  displays this help message and exits 
        -s,   --silent                  :  show only subdomain in output (this is not included for -ski,-sti)
        -v,   --version                 :  show current version of subdominator and latest version if available and exits
        -ski, --show-key-info           :  show keys error for out of credits and key not provided for particular sources
        -ste, --show-timeout-info       :  show timeout error for sources that are timeout to connect
        -nc,  --no-color                :  disable the colorised output of subdominator
        -ls,  --list-source             :  display the sources of subdominator uses for subdomain enumerations and exits (included for upcoming updates on sources).{reset}""")
    
    quit()
    