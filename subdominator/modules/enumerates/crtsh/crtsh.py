from colorama import Fore, Style
import aiohttp
import sys
from fake_useragent import UserAgent

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def crtsh(domain, session, args):
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        headers = {
            "User-Agent": UserAgent().random
        }
        proxy = args.proxy if args.proxy else None
        async with session.get(url, timeout=args.timeout, headers=headers ,proxy=proxy, ssl=False) as response:
            if response.status != 200:
                return []
            data = await response.json()
            subdomains = [domain for domains in data for domain in domains['name_value'].split('\n')]
            return subdomains
        
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Crtsh, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Crtsh, due to Serverside Error", file=sys.stderr)
                    
    except KeyboardInterrupt as e:
        quit()
        
    except TimeoutError as e:
        if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Crtsh, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Crtsh, due to Timeout Error", file=sys.stderr)
                    
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Crtsh, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Crtsh, due to Clientside connection Error", file=sys.stderr)
                    
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at crtsh : {e}, {type(e)}{reset}", file=sys.stderr)