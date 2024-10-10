#!/usr/bin/env python3
from colorama import Fore,Back,Style
from art import *
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
colors = [ green, cyan, blue, white, magenta]
random_color = random.choice(colors)


def banner():
    tool_name = "subdominator"
    fonts = ["big", "ogre", "shadow", "script",  "graffiti", "slant"]
    selected_font = random.choice(fonts)
    banner = text2art(f"{tool_name}", font=selected_font)
    banner = f"""{bold}{random_color}{banner}{reset}
                     {bold}{white}@RevoltSecurities{reset}\n"""
    return banner

