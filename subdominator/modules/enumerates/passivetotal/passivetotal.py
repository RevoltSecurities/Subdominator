from colorama import Fore, Style
import aiofiles
import random
import yaml
import aiohttp
import sys
from fake_useragent import UserAgent
import re

filter = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}\\032")
bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

Passivetotals = []

async def passivetotal(domain, session, configs, username, args):
    try:
        try:
            async with aiofiles.open(configs, "r") as streamr:
                data = yaml.safe_load(await streamr.read())
                if "passivetotal" not in data:
                    return []
                rand = data.get("passivetotal", [])
                if rand is None:
                    return []
                randomkeys = random.choice(data.get("passivetotal", []))
                if randomkeys is None:
                    return []
                username, randomkey = randomkeys.split(":")
        except yaml.YAMLError as e:
            if args.show_key_info: 
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Hey {username} Please check syntax of {configs}{reset}", file=sys.stderr)  
                else:
                    print(f"[INFO]: Hey {username} Please check syntax of {configs}", file=sys.stderr) 
        except TypeError as e:
            pass 
        except KeyboardInterrupt as e:
            quit()
        except yaml.YAMLObject as e:
            if args.show_key_info: 
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Hey {username} Please check syntax of {configs}{reset}", file=sys.stderr)    
                else:
                    print(f"[INFO]: Hey {username} Please check syntax of {configs}", file=sys.stderr)
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in passivetotal reader block: {e}, {type(e)}{reset}", file=sys.stderr)
        if username is None or randomkey is None:
            return []
        try:
            url = f"https://api.passivetotal.org/v2/enrichment/subdomains?query={domain}"
            headers = {
                "User-Agent": UserAgent().random,
                "Content-Type": "application/json"
            }
            async with session.get(url, headers=headers, auth=aiohttp.BasicAuth(username, randomkey), ssl=False, timeout=args.timeout, proxy=args.proxy if args.proxy else None) as response:
                jdata = await response.json()
                subdomains = jdata.get("subdomains", [])
                for subdomain in subdomains:
                    if filter.match(subdomain):
                        continue
                    filtered_subdomain = f"{subdomain}.{domain}"
                    Passivetotals.append(filtered_subdomain)
        except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Passive API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Passive API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Passivetotal API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Passivetotal API, due to Clientside connection Error", file=sys.stderr) 
                    
        except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Passivetotal API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Passivetotal API, due to Timeout Error", file=sys.stderr) 
                
        except KeyboardInterrupt as e:
            quit()
            
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api passivetotal req block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
                    
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api passivetotal main block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
    finally:
        return Passivetotals