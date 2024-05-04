from colorama import Fore, Style
import aiohttp
import sys
from bs4 import  XMLParsedAsHTMLWarning, MarkupResemblesLocatorWarning, BeautifulSoup
from fake_useragent import UserAgent
import warnings


bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def shodanx(domain, session, args):
    try:
        shodanxs = []
        url = f"https://www.shodan.io/domain/{domain}"
        auth = {
            "User-Agent": UserAgent().random
        }
        proxy= args.proxy if args.proxy else None
        async with session.get(url, headers=auth, timeout=args.timeout, proxy=proxy, ssl=False) as response:
            if response.status != 200:
                return []
            data = await response.text()
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)
                warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
                soup = BeautifulSoup(data, "lxml")
                ul = soup.find('ul', id='subdomains')
                if not ul:
                    return []
                subdomains = ul.findAll("li")
                for result in subdomains:
                    subdomain=f"{result.text.strip()}.{domain}"
                    shodanxs.append(subdomain)
                return shodanxs
            
    except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for ShodanX, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for ShodanX, due to Serverside Error", file=sys.stderr)
                    
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for ShodanX, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for ShodanX, due to Clientside connection Error", file=sys.stderr) 
                    
    except KeyboardInterrupt as e:
        quit()
        
    except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for ShodanX , due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for ShodanX, due to Timeout Error", file=sys.stderr)
                           
    except Exception as e:
        if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in shodan request block: {e}, {type(e)}{reset}", file=sys.stderr)