from colorama import Fore, Style
import aiofiles
import random
import yaml
import aiohttp
import sys
from fake_useragent import UserAgent

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def c99(domain, session, configs, username, args):
    try:
        try:
            
            async with aiofiles.open(configs, "r") as streamr:
                data = yaml.safe_load(await streamr.read())
                if "c99" not in data:
                    return []
                randvalue = data.get("c99", [])
                    
                if randvalue is None:  
                    return []
                       
                randomkey = random.choice(data.get("c99", []))
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in c99 reader block: {e}, {type(e)}{reset}",file=sys.stderr)
            
        if randomkey is None:
            return 
        try:
            url = f"https://api.c99.nl/subdomainfinder?key={randomkey}&domain={domain}&json=true"
            proxy = args.proxy if args.proxy else None
            headers = {"User-Agent": UserAgent().random}
            async with session.get(url, headers=headers,timeout=args.timeout, proxy=proxy , ssl=False) as response:
                if response.status != 200:
                    return []
                data = await response.json()
                if "subdomain" in data:
                    C99= [entry["subdomain"] for entry in data]
                    return C99
                    
        except aiohttp.ServerConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for C99 API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for C99 API, due to Serverside Error", file=sys.stderr)
                        
        except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for C99 API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for C99 API, due to Clientside connection Error", file=sys.stderr)
        except KeyError as e:
            pass 
        except TypeError as e:
            pass
        except KeyboardInterrupt as e:
            quit()
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api C99 req block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api c99 api main block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
    