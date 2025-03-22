from colorama import Fore,Style,init
import sys
import random
init()

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


def logger(message: str, level="info", nocolored=False):
    if level == "info":
        if nocolored:
            leveler = "INFO"
        else:
            leveler = f"{bold}{blue}INFO{reset}"
            
    elif level == "warn":
        if nocolored:
            leveler = "WRN"
        else:
            leveler = f"{bold}{red}WRN{reset}"
            
    elif level == "error":
        if nocolored:
            leveler = "ERR"
        else:
            leveler = f"{bold}{red}ERR{reset}"
            
    elif level == "verbose":
        if nocolored:
            leveler = "VRB"
        else:
            leveler = f"{bold}{green}VRB{reset}"
    
    elif level == "debug":
        if nocolored:
            leveler = "DBG"
        else:
            leveler = f"{bold}{cyan}DBG{reset}"  

    else:
        if nocolored:
            leveler = f"{level.upper()}"
        else:
            leveler = f"{bold}{green}{level.upper()}{reset}"
    
    if nocolored:
        print(f"[{leveler}]: {message}", file=sys.stderr)
    else:
        print(f"[{bold}{blue}{leveler}{reset}]: {bold}{white}{message}{reset}", file=sys.stderr)
    
def bannerlog(banner: str):
    print(banner, file=sys.stderr)
    
def stdinlog(message):
    print(message)