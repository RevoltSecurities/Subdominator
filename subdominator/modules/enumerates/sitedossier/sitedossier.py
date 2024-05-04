from colorama import Fore, Style
import aiohttp
import sys
import re

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def sitedossier(domain, session, args):
    try:
        sitedossiers=[]
        page = 1
        while True:
            url = f"http://www.sitedossier.com/parentdomain/{domain}/{page}"
            proxy = args.proxy if args.proxy else None
            async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                if response.status !=200:
                    if len(sitedossiers)>0:
                        return sitedossiers
                    return []
                data = await response.text()
                filterdomain = re.escape(domain)
                pattern = r'(?i)(?:https?://)?([a-zA-Z0-9*_.-]+\.' + filterdomain + r')'
                subdomains = re.findall(pattern, data)
                for subdomain in subdomains:
                    sitedossiers.append(subdomain)
                if "Show next 100 items" not in data:
                    if len(sitedossiers)>0:
                        return sitedossiers
                    return []
                page+=100
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Sitedossier, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Sitedossier, due to Serverside Error", file=sys.stderr)
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Sitedossier, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Sitedossier, due to Clientside connection Error", file=sys.stderr)
                    
    except KeyboardInterrupt as e:
        quit()
        
    except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Sitedossier, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Sitedossier, due to Timeout Error", file=sys.stderr)
                           
    except Exception as e:
        if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in sitedossier request block: {e}, {type(e)}{reset}", file=sys.stderr)