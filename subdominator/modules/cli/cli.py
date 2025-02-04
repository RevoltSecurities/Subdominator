#!/usr/bin/env python3
from colorama import Fore,Back,Style
import argparse
import time as t
import random
import traceback

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

args = None

def cli():
    try:
        parser = argparse.ArgumentParser(add_help=False, usage=argparse.SUPPRESS,exit_on_error=False)
        parser.add_argument("-d", "--domain", type=str)
        parser.add_argument("-dL", "--domain-list", type=str)
        parser.add_argument("-cp", "--config-path", type=str)
        parser.add_argument("-o", "--output", type=str)
        parser.add_argument("-oD", "--output-directory", type=str)
        parser.add_argument("-t", "--timeout", type=float, default=30)
        parser.add_argument("-up", "--update", action="store_true")
        parser.add_argument("-nt", "--notify", action="store_true")
        parser.add_argument("-px", "--proxy", type=str)
        parser.add_argument("-h", "--help", action="store_true")
        parser.add_argument("-v","--version", action="store_true")
        parser.add_argument("-ski", "--show-key-info", action="store_true")
        parser.add_argument("-ste", "--show-timeout-info", action="store_true")
        parser.add_argument("-nc", "--no-color", action="store_true")
        parser.add_argument("-ls", "--list-source", action="store_true")
        parser.add_argument("-duc", "--disable-update-check", action="store_true")
        parser.add_argument("-sd", "--sec-deb", action="store_true")
        parser.add_argument("-sup", "--show-updates", action="store_true")     
        parser.add_argument("-fw", "--filter-wildcards", action="store_true")
        parser.add_argument("-oJ", "--output-json", type=str)
        parser.add_argument("-s", "--silent", action="store_true")
        parser.add_argument("-sc", "--sources", type=lambda s: s.split(","), help="Comma-separated list of sources")

        global args 
                
        return parser.parse_args()
        
    
    except argparse.ArgumentError as e:
        
        print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Please use the command for more infromation:{reset} {bold}{blue}subdominator -h{reset}")
        
        exit()
        
    except argparse.ArgumentTypeError as e:
        
        print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Please use the command for more infromation:{reset} {bold}{blue}subdominator -h{reset}")
        
        exit()
        
        
    except Exception as e:
        
        print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Unexpected Error: {traceback.format_exc()} {reset}")
        
        pass
    
    except KeyboardInterrupt as e:
        
        print(f"\n[{bold}{blue}INFO{reset}]: {bold}{white}CTRL+C Pressed{reset}")
        
        SystemExit