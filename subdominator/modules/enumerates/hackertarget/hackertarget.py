from colorama import Fore, Style
import aiohttp
import sys

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def hackertarget(domain, session, args):
    try:
        hackertargets =[]
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        proxy= args.proxy if args.proxy else None
        async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False) as response:
            if response.status !=200:
                return
            responsed = await response.text()
            data = responsed.splitlines()
            for subdomain in data:
                if "API count exceeded - Increase Quota with Membership" in subdomain:
                    pass
                else:
                    subdomain = subdomain.split(",")[0]
                    hackertargets.append(subdomain)
        return hackertargets
    
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Hackertarget API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Hackertarget API, due to Serverside Error", file=sys.stderr)
                    
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Hackertarget API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Hackertarget API, due to Clientside connection Error", file=sys.stderr)
                    
    except TimeoutError as e:
        if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Hackertarget API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Hackertarget API, due to Timeout Error", file=sys.stderr)
                    
    except KeyboardInterrupt as e:
        quit()
        
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}INFO{reset}]: {bold}{white}Exception at hackertarget: {e}, {type(e)}{reset}", file=sys.stderr)
            