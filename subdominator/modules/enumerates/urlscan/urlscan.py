from colorama import Fore, Style
import aiohttp
import sys

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def urlscan(domain , session, args):
    try:
        urlscans = []
        url = f"https://urlscan.io/api/v1/search/?q=page.domain:{domain}&size=10000"
        proxy= args.proxy if args.proxy else None
        async with session.get(url, timeout=args.timeout, proxy=proxy,ssl=False) as response:
            if response.status != 200:
                return
            data = await response.json()
            for domain in data['results']:
                subdomain = domain['page']['domain']
                urlscans.append(subdomain)
            return urlscans
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Urlscan, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Urlscan due to Serverside Error", file=sys.stderr)
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Urlscan, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Urlscan, due to Clientside connection Error", file=sys.stderr) 
                    
    except KeyboardInterrupt as e:
        quit()
        
    except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Urlscan, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Urlscan, due to Timeout Error", file=sys.stderr)
                           
    except Exception as e:
        if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in urlscan request block: {e}, {type(e)}{reset}", file=sys.stderr)
                