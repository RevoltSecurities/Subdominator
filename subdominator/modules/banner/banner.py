#!/usr/bin/env python3
from art import *
from subdominator.modules.logger.logger import logger, random, random_color, reset,bold,white

def banner():
    tool_name = "subdominator"
    fonts = ["big", "ogre", "shadow", "script",  "graffiti", "slant"]
    selected_font = random.choice(fonts)
    banner = text2art(f"{tool_name}", font=selected_font)
    banner = f"""{bold}{random_color}{banner}{reset}
                     {bold}{white}- RevoltSecurities{reset}\n"""
    return banner