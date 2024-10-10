from colorama import Fore, Style
import re
import httpx
import sys
from fake_useragent import UserAgent
from subdominator.modules.utils import compiler, extracts

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL
Waybackurls = set()

async def waybackarchive(domain, args):
    try:
       headers = {
           "User-Agent": UserAgent().random
       }
       proxy = args.proxy if args.proxy else None
       async with httpx.AsyncClient(verify=False, proxy=proxy) as request:
           async with request.stream("GET", f"https://web.archive.org/cdx/search/cdx?url=*.{domain}&collapse=urlkey&fl=original", headers=headers, timeout=httpx.Timeout(read=300.0, connect=args.timeout, write=None, pool=None), follow_redirects=True) as response:
               async for url in response.aiter_lines():
                   subdomains = await extracts(url, domain)
                   if subdomains:
                       for subdomain in subdomains:
                           subdomain = subdomain.lstrip("25").lstrip("2F").lstrip("40").lstrip(".").lstrip("B0")
                           if subdomain not in Waybackurls and not subdomain.startswith("%3D") and not subdomain.startswith("3D"):
                               Waybackurls.add(subdomain)
    except KeyboardInterrupt as e:
        quit()
    except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Webarchive, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Webarchive, due to Timeout Error", file=sys.stderr)
    except httpx.ConnectTimeout:
        if args.show_timeout_info:
            if not args.no_color: 
                print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Webarchive, due to Timeout Error", file=sys.stderr)    
            else:
                print(f"[INFO]: Timeout reached for Webarchive, due to Timeout Error", file=sys.stderr)
    except httpx.ConnectError:
        if args.show_timeout_info:
            if not args.no_color: 
                print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Webarchive, due to Timeout Error", file=sys.stderr)    
            else:
                print(f"[INFO]: Timeout reached for Webarchive, due to Timeout Error", file=sys.stderr)
    except httpx.ReadTimeout:
        pass
    except Exception as e:
        if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in wayback request block: {e}, {type(e)}{reset}", file=sys.stderr)
    finally:
        return Waybackurls