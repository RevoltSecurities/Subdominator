import re
import tldextract
import aiofiles
import yaml
import random
from typing import Optional,Tuple
from fake_useragent import UserAgent
import os
from subdominator.modules.logger.logger import logger
from colorama import Fore,Style
import sys

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

def Exit(code=0):
    sys.exit(code)

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

def UserAgents() -> str:
    return UserAgent().random

async def singlekeyloader(filename: str, source: str) -> Optional[str]:
    try:
        async with aiofiles.open(filename, "r") as streamr:
            data = yaml.safe_load(await streamr.read())
            if source not in data:
                return None
            randomkey = random.choice(data.get(source, []))
            if len(randomkey) != 0:
                return randomkey
            else:
                return None
    except Exception as e:
        return None
    
async def dualkeyloader(filename: str, source: str, splits=False) -> Optional[Tuple[str, str]]:
    try:
        async with aiofiles.open(filename, "r") as streamr:
            data = yaml.safe_load(await streamr.read())
            if source not in data:
                return None,None
            randomkeys = random.choice(data.get(source, []))
            if len(randomkeys) != 0 :
                if splits:
                    key1, key2 = randomkeys.rsplit(":", 1)
                else:
                    key1, key2 = randomkeys.split(":")
                return key1,key2
            else:
                return None,None
    except Exception as e:
        return None

def filters(results):
    if not results:
        return []
    filtered = []
    for subdomains in results:
        if subdomains is None:
            subdomains = []
        for subdomain in subdomains:
            if subdomain is not None:
                filtered.append(subdomain)
    return sorted(set(filtered))


async def reader(filename: str, args) -> list:
    try:
        async with aiofiles.open(filename, mode="r") as streamr:
            data = await streamr.read()
        return data.splitlines()
    except FileNotFoundError:
        logger(f"File '{filename}' not found. Please check if it exists.")
        Exit(1)
    except Exception as e:
        logger(f"Exception in file reader module due to: {e} ({type(e).__name__})", "warn", args.no_color)
        Exit(1)

async def check_file_permission(filename: str, args):
    try:
        async with aiofiles.open(filename, mode="a"):
            pass  
        return True
    except PermissionError:
        logger(f"Permission denied: User doesn't have write permission in  '{filename}' file", "warn", args.no_color)
        return False
    except Exception as e:
        logger(f"Exception in permission check: {e} ({type(e).__name__})", "warn", args.no_color)
        return False
    
async def check_directory_permission(directory: str, args):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        test_file = os.path.join(directory, ".permission_check")
        async with aiofiles.open(test_file, mode="w") as test:
            await test.write("test")
        os.remove(test_file)        
        return True
    except PermissionError:
        logger(f"Permission denied: User doesn't have write permission in '{directory}' directory", "warn", args.no_color)
        return False
    except Exception as e:
        logger(f"Exception in directory permission check: {e} ({type(e).__name__})", "warn", args.no_color)
        return False

def split_to_list(values: str, delimiter: str = ",") -> list:
    return [val.strip() for val in values.split(delimiter) if val.strip()]