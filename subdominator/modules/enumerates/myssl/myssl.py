from colorama import Fore, Style
import aiohttp
import sys
from fake_useragent import UserAgent

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def myssl(domain, session, args):
    try:
        myssls = []
        
        url= f"https://myssl.com/api/v1/discover_sub_domain?domain={domain}"
        headers = {
            "User-Agent": UserAgent().random
        }
        proxy = args.proxy if args.proxy else None
        async with session.get(url, headers=headers, timeout=args.timeout, ssl=False, proxy=proxy) as response:
            if response.status !=200:
                return []
            data = await response.json()
            for subdomains in data.get("data"):
                subdomain = subdomains['domain']
                if subdomain.endswith(f".{domain}"):
                    myssls.append(subdomain)
            return myssls
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Myssl API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Myssl API, due to Serverside Error", file=sys.stderr)
    except TimeoutError as e:
        if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Myssl API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Myssl API, due to Timeout Error", file=sys.stderr) 
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Myssl API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Myssl API, due to Clientside connection Error", file=sys.stderr) 
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured at Myssl api: {e}, {type(e)}{reset}", file=sys.stderr)