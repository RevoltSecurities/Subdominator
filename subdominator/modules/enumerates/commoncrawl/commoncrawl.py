import asyncio
import httpx
import aiofiles
import os  
import random
from fake_useragent import UserAgent
from datetime import datetime
from colorama import Fore, Style
import re
from subdominator.modules.utils import compiler, extracts
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

Commoncrawls = set()

async def indexDB(args):
    try:
        headers = {
                "User-Agent": UserAgent().random
        }
        async with httpx.AsyncClient(headers=headers, timeout=args.timeout, verify=False,proxy=args.proxy if args.proxy else None) as session:
            response = await session.request("GET", "https://index.commoncrawl.org/collinfo.json", follow_redirects=True)
            return response.json()
    except KeyboardInterrupt:
        exit()
    except asyncio.CancelledError:
        exit()
    except httpx.RemoteProtocolError:
        pass
    except httpx.ReadTimeout:
        pass
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at CC index fetcher: {e}, {type(e)}{reset}")
            
async def CcClient(args,searchurl: str,domain):
    try:
        headers = {
                "User-Agent": UserAgent().random
        }
        async with httpx.AsyncClient(timeout=httpx.Timeout(read=300.0, connect=args.timeout, write=None, pool=None), headers=headers, verify=False, proxy=args.proxy if args.proxy else None) as request:
            async with  request.stream("GET", f"{searchurl}?url=*.{domain}", follow_redirects=True) as response:
                async for url in response.aiter_lines():

                    subdomains = await extracts(url, domain)
                    if subdomains:
                        for subdomain in subdomains:
                            subdomain = subdomain.lstrip("25").lstrip("2F").lstrip("40").lstrip(".")
                            if subdomain not in Commoncrawls and not subdomain.startswith("%3D") and not subdomain.startswith("3D"):
                                Commoncrawls.add(subdomain)
    except KeyboardInterrupt:
            exit()
    except asyncio.CancelledError as e:
            exit()
    except httpx.RemoteProtocolError:
            pass
    except httpx.ReadTimeout:
            pass
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at  CC url fetcher: {e}, {type(e)}{reset}")

async def commoncrawl(Domain, args):
    try:
        indexurls = []
        added = set()
        responsed = await indexDB(args)
        if responsed is None:
            return Commoncrawls
        ctyear = datetime.now().year
        years = [str(ctyear - i) for i in range(6)]
        for year in years:
            for index in responsed:
                if year not in added:
                    if year in index.get("name"):
                        indexurls.append(index.get('cdx-api'))
                        added.add(year)
        for url in indexurls:
            await CcClient(args, url, Domain)
        return Commoncrawls
    except KeyboardInterrupt:
            exit()
    except asyncio.CancelledError as e:
            exit()
    except Exception as e:
            if args.sec_deb:
                    print(f"Exception at commoncrawl: {e}, {type(e)}")