from colorama import Fore, Style
import aiohttp
import sys
from fake_useragent import UserAgent

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def racent(domain, session, args):
    try:
        racents =[]
        url = f"https://face.racent.com/tool/query_ctlog?keyword={domain}"
        headers = {
            "User-Agent": UserAgent().random
        }
        proxy = args.proxy if args.proxy else None
        async with session.get(url, headers=headers, ssl=False, proxy=proxy, timeout=args.timeout) as response:
            if response.status != 200:
                return []
            
            data = await response.json()
            if "CTLog 查询超过限制" in data:
                return []
            
            for subdomains in data['data']['list']:
                for subdomain in subdomains['dnsnames']:
                    racents.append(subdomain)
            return racents
        
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Racent API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Racent API, due to Serverside Error", file=sys.stderr)
    except TypeError as e:
        pass
    
    except TimeoutError as e:
        if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Racent API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Racent API, due to Timeout Error", file=sys.stderr) 
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Racent API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Racent API, due to Clientside connection Error", file=sys.stderr) 
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured at Racent api: {e}, {type(e)}{reset}", file=sys.stderr)