from colorama import Fore, Style
import aiohttp
import sys
import asyncio

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def anubis(domain, session, args):
    try:
        anubiss = []
        url = f"https://jonlu.ca/anubis/subdomains/{domain}"
        proxy = args.proxy if args.proxy else None
        async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False) as response:
            if response.status != 200:
                return []
            data = await response.json()
            for subdomain in data:
                if subdomain.endswith(f".{domain}") :
                    anubiss.append(subdomain)
            return anubiss        
    except TimeoutError as e:
        if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Anubis API, due to Timeout", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Anubis API, due to Timeout", file=sys.stderr)
    except KeyboardInterrupt as e:
        quit()
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Anubis API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Anubis API, due to Serverside Error", file=sys.stderr)
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Anubis API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Anubis API, due to Clientside connection Error", file=sys.stderr)
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occred in anubis: {e}, {type(e)}{reset}", file=sys.stderr)


    