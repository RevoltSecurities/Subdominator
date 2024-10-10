import re
from colorama import Fore, Style # to reduce imports and colorsvar assingings 
import tldextract

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def compiler(domain):
    pattern = re.compile(r"(?i)[a-zA-Z0-9\*_.-]+\." + re.escape(domain))
    return pattern

async def extracts(response, domain):
    regex = await compiler(domain)
    matches = regex.findall(response)
    return set(matches)
    
def check_subdomain(domain):
    parsed = tldextract.extract(domain)
    return parsed