from colorama import Fore, Style
import aiohttp
import sys

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def alienvault(domain, session,args):
    try:
        alienvaults = []
        url = f"https://otx.alienvault.com/api/v1/indicators/hostname/{domain}/passive_dns"
        proxy = args.proxy if args.proxy else None
        async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False) as response:
            if response.status != 200:
                return []
            data = await response.json()
            for entries in data['passive_dns']:
                subdomain = entries['hostname']
                if subdomain.endswith(f".{domain}"):
                    alienvaults.append(subdomain)
            return alienvaults
    except TimeoutError as e:
        if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Alienvault API, due to Timeout", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Alienvault API, due to Timeout", file=sys.stderr)
    except KeyboardInterrupt as e:
        quit()
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Alienvault API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Alienvault API, due to Serverside Error", file=sys.stderr)
                
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Alienvault API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Alienvault API, due to Clientside connection Error", file=sys.stderr)
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]Exception occred in alienvault: {e}, {type(e)}", file=sys.stderr)