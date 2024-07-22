from colorama import Fore, Style
import aiohttp
import sys
from fake_useragent import UserAgent

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def columbusapi(domain, session, args):
    try:
        columbusapis = []
        url = f"https://columbus.elmasy.com/api/lookup/{domain}?days=-1"
        proxy= args.proxy if args.proxy else None
        headers = {
            "User-Agent": UserAgent().random
        }
        
        async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False, headers=headers) as response:
            if response.status !=200:
                return []
            data=await response.json()
            for subdomain in data:
                columbusapis.append(f"{subdomain}.{domain}")
            return columbusapis
        
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Columbus API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Columbus API, due to Serverside Error", file=sys.stderr)
    except TimeoutError as e:
        if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Columbus API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Columbus API, due to Timeout Error", file=sys.stderr) 
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Columbus API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Columbus API, due to Clientside connection Error", file=sys.stderr) 
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured at columbusapi: {e}, {type(e)}{reset}", file=sys.stderr)