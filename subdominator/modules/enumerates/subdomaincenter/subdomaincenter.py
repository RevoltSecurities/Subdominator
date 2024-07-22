from colorama import Fore, Style
import aiofiles
import random
import yaml
import aiohttp
import sys
import asyncio

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def subdomaincenter(domain, session, args):
    try:
        subdomaincenters = []
        url = f"https://api.subdomain.center/?domain={domain}"
        proxy = args.proxy if args.proxy else None
        async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False) as response:
            if response.status !=200:
                return
            data = await response.json()
            for subdomain in data:
                subdomaincenters.append(subdomain)
            return subdomaincenters
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Subdomaincenter API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Subdomaincenter API, due to Serverside Error", file=sys.stderr)
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Subdomaincenter API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Subdomaincenter API, due to Clientside connection Error", file=sys.stderr)
    except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Subdomaincenter, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Subdomaincenter, due to Timeout Error", file=sys.stderr)
                           
    except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in subdomaincenter request block: {e}, {type(e)}{reset}", file=sys.stderr)