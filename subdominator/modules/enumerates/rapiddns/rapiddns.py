from colorama import Fore, Style
import aiohttp
import sys
from fake_useragent import UserAgent
import re

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL


async def rapiddns(domain, session, args):
    try:
        
        rapiddnss = []
        
        for pagenum in range(1, 7+1):
            
            url = f"https://rapiddns.io/subdomain/{domain}?page={pagenum}"
            
            auth = {
                "User-Agent": UserAgent().random
            }
            proxy = args.proxy if args.proxy else None
            async with session.get(url, headers=auth, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                
                data = await response.text()
                filterdomain = re.escape(domain)
                pattern = r'(?i)(?:https?://)?([a-zA-Z0-9*_.-]+\.' + filterdomain + r')'
                subdomains = re.findall(pattern, data)
                for subdomain in subdomains:
                    rapiddnss.append(subdomain)
                    
                if "Next" not in data:
                    return rapiddnss
                
    except TimeoutError as e:
        if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Rapiddns, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Rapiddns, due to Timeout Error", file=sys.stderr)
            
    
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Rapiddns, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Rapiddns, due to Serverside Error", file=sys.stderr)
            
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Rapiddns, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Rapiddns, due to Clientside connection Error", file=sys.stderr) 
                
    except Exception as e:
        print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at rapiddsn: {e}, {type(e)}{reset}", file=sys.stderr)
