from colorama import Fore, Style
import aiofiles
import random
from fake_useragent.fake import UserAgent
import yaml
import aiohttp
import sys
import json

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL
Builtwiths = []

async def builtwith(domain,session, configs, username, args): #not tested but we implemented for experimental
    try:
        try:
            async with aiofiles.open(configs, "r") as streamr:
                data = yaml.safe_load(await streamr.read())
                if "builtwith" not in data:
                    return []
                randvalue = data.get("builtwith", [])
                if randvalue is None:  
                    return []
            randomkey = random.choice(data.get("builtwith", []))
        except yaml.YAMLError as e:
            if args.show_key_info: 
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Hey {username} Please check syntax of {configs}{reset}", file=sys.stderr)  
                else:
                    print(f"[INFO]: Hey {username} Please check syntax of {configs}", file=sys.stderr)         
        except TypeError as e:
            pass 
        except yaml.YAMLObject as e:
            if args.show_key_info: 
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Hey {username} Please check syntax of {configs}{reset}", file=sys.stderr)    
                else:
                    print(f"[INFO]: Hey {username} Please check syntax of {configs}", file=sys.stderr)   
        except KeyboardInterrupt as e:
            quit()
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in builtwith reader block: {e}, {type(e)}{reset}",file=sys.stderr)
        if randomkey is None:
            return Builtwiths
        try:
            url = f"https://api.builtwith.com/v21/api.json?KEY={randomkey}&HIDETEXT=yes&HIDEDL=yes&NOLIVE=yes&NOMETA=yes&NOPII=yes&NOATTR=yes&LOOKUP={domain}"
            proxy = args.proxy if args.proxy else None
            headers = {
                "User-Agent": UserAgent().random
            }
            async with session.get(url, headers=headers, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                if response.status != 200:
                    if args.show_key_info:
                        if not args.no_color:
                            print(f"[{bold}{red}ALERT{reset}]: Builtwith blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                        else:
                            print(f"[ALERT]: Builtwith blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                    return Builtwiths
                jdata = await response.json()
                if isinstance(jdata, dict):
                    results = jdata.get("Results", [])
                    if results:
                        for result in results:
                            for chunk in result.get("Result", {}).get("Paths", []):
                                domain = chunk.get("Domain", "")
                                subdomain = chunk.get("SubDomain", "")
                                if domain and subdomain:
                                    Subdomain = f"{subdomain}.{domain}"
                                    Builtwiths.append(Subdomain)
        except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Builtwith API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Builtwith API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Builtwith API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Builtwith API, due to Clientside connection Error", file=sys.stderr) 
        except KeyboardInterrupt as e:
            quit()
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api builtwith req block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api builtwith main block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
    finally:
        return Builtwiths