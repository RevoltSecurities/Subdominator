from colorama import Fore, Style
import aiohttp
import re
import sys
from fake_useragent import UserAgent

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def digitorus(domain, session, args):
    try:
        url = f"https://certificatedetails.com/{domain}"
        proxy = args.proxy if args.proxy else None
        headers = {
            "User-Agent": UserAgent().random
        }
        async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False, headers=headers) as response:
            data = await response.text()
            filterdomain = re.escape(domain)
            pattern = r'(?i)(?:https?://)?([a-zA-Z0-9*_.-]+\.' + filterdomain + r')'
            subdomains = re.findall(pattern, data)
            if subdomains:
                return subdomains
            return []
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Digitorus API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Digitorus API, due to Serverside Error", file=sys.stderr)
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Digitorus API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Digitorus API, due to Clientside connection Error", file=sys.stderr) 
    except TimeoutError as e:
        if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Digitorus API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Digitorus API, due to Timeout Error", file=sys.stderr)
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}exception at digitorus: {e}, {type(e)}{reset}", file=sys.stderr)