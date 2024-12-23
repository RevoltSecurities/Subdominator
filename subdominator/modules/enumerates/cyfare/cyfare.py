from colorama import Fore, Style
import aiohttp
import sys
from fake_useragent import UserAgent
bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def cyfare(domain, session, args):
    try:
        Cyfare = []
        url = "https://cyfare.net/apps/subfind/query.php"
        headers = {
            "User-Agent": UserAgent().random,
            "Origin": "https://cyfare.net",
            "Content-Type": "application/json"
        }
        jbody = {
            "domain": f"{domain}"
        }
        proxy = args.proxy if args.proxy else None
        async with session.post(url, headers=headers, json=jbody, timeout=args.timeout, ssl=False, proxy=proxy) as response:
            if response.status != 200:
                return Cyfare
            data = await response.json()
            subdomains = data.get("subdomains", [])
            if len(subdomains) > 0:
                Cyfare.extend(subdomains)
            return Cyfare
    except aiohttp.ServerConnectionError as e:
                if args.show_timeout_info:
                    if not args.no_color: 
                        print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Cyfare, due to Serverside Error", file=sys.stderr)    
                    else:
                        print(f"[INFO]: Timeout reached for Cyfare, due to Serverside Error", file=sys.stderr)  
    except KeyboardInterrupt as e:
            quit()
    except TimeoutError as e:
        if args.show_timeout_info:
            if not args.no_color: 
                print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Cyfare, due to Timeout Error", file=sys.stderr)    
            else:
                print(f"[INFO]: Timeout reached for Cyfare, due to Timeout Error", file=sys.stderr)
    except aiohttp.ClientConnectionError as e:
        if args.show_timeout_info:
            if not args.no_color: 
                print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Cyfare, due to ClientSide connection Error", file=sys.stderr)    
            else:
                print(f"[INFO]: Timeout reached for Cyfare, due to Clientside connection Error", file=sys.stderr)
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at cyfare API : {e}, {type(e)}{reset}", file=sys.stderr)
