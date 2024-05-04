import re
from fake_useragent import UserAgent
from colorama import Fore, Style
import aiohttp
import sys

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def abuseipdb(domain, session, args):
    try:
        url = f"https://www.abuseipdb.com/whois/{domain}" 
        proxy = args.proxy if args.proxy else None    
        headers = {
                     "User-Agent": UserAgent().random,
                    "Cookie": "abuseipdb_session="
        }
        async with session.get(url, timeout=10, headers=headers, proxy=proxy, ssl=False) as response:
            data = await response.text()
            if response.status != 200:
                return []
            tags = re.findall(r'<li>\w.*</li>', data)
            subdomains = [re.sub("</?li>", "", tag) + f".{domain}" for tag in tags]
            return subdomains
    except TimeoutError as e:
        if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Abuseipdb API, due to Timeout", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Abuseipdb API, due to Timeout", file=sys.stderr)      
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Abuseipdb API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Abuseipdb API, due to Serverside Error", file=sys.stderr)            
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Abuseipdb API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Alienvault API, due to ClientSide connection Error", file=sys.stderr)
    except KeyboardInterrupt as e:
        quit()
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in abuseipdb: {e}, {type(e)}{reset}", file=sys.stderr)
