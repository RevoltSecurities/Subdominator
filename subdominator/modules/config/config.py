import appdirs
from colorama import Fore, Back, Style
import os
import sys

white = Fore.WHITE
blue = Fore.BLUE
red = Fore.RED
bold = Style.BRIGHT
reset = Style.RESET_ALL

yamls = """bevigil: []          

binaryedge: []

bufferover: []

builtwith: []

c99: []

censys: []

certspotter: []

chaos: []

dnsdumpster: []

facebook: []

fofa: []

fullhunt: []

google: []

huntermap: []

intelx: []

leakix: []

netlas: []

passivetotal: []

quake: []

rapidapi: []

redhuntlabs: []

rsecloud: []

virustotal: []

securitytrails: []

shodan: []

trickest: []

whoisxmlapi: []

zoomeyeapi: []

# for notifications
slack: []

pushbullet: []

# subdominator follow same syntax of key configuration of subfinder follows but some resource will be different so please look on github page of subdominator for keys setup.
"""

def get_username():
    try:
        username = os.getlogin()
    except OSError:
        username = os.getenv('USER') or os.getenv('LOGNAME') or os.getenv('USERNAME') or 'User'
    except Exception as e:
        username = "User"
    return username


def config(): 
    try:
        username = get_username()
        get_config = appdirs.user_config_dir()
        subdominator_dir = f"{get_config}/Subdominator"
        filename = "provider-config.yaml"
        config_path = f"{subdominator_dir}/{filename}"
        
        if os.path.exists(subdominator_dir):
            if os.path.exists(config_path):
                return config_path
            else:
                with open(config_path, "w") as w:
                    w.write(yamls)
                return config_path
        else:
            os.makedirs(subdominator_dir)
            with open(config_path, "w") as w:
                w.write(yamls)
            return config_path
    except Exception as e:
        print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured at config module: {e}{reset}", file=sys.stderr)

def cachedir():
    try:
        cachedir = appdirs.user_cache_dir()
        return cachedir
    except Exception as e:
        pass

def custompath(args):
    
    try:
        if os.path.exists(args.config_path) and os.path.isfile(args.config_path):
            return args.config_path
        else:
            if args.no_color:
                print(f"[WRN]: please check the the config file exists")
                quit()
            else:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}please check the the config path exists{reset}")
    except KeyboardInterrupt as e:
        quit()