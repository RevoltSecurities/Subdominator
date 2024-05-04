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

async def randomkeys(configs, username, args):
    try:
            async with aiofiles.open(configs, "r") as streamr:
                data = yaml.safe_load(await streamr.read())
                if "google" not in data:
                    return
                
                rand = data.get("google", [])
                if rand is None:
                    return
                randomkey = random.choice(data.get("google", []))
                
                cx, key = randomkey.split(":")
                return cx, key
                
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
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in google randomkey: {e}, {type(e)}{reset}", file=sys.stderr)
            
            
async def google(domain, session, configs, username, args):
    try:
        googles = []
        page = 1
        while True:
            randomcx, randomkey = await randomkeys(configs, username, args)

            if randomcx is None or randomkey is None:
                return googles
            
            url = f"https://customsearch.googleapis.com/customsearch/v1?q=site:*.{domain}%20-www&cx={randomcx}&num=10&start={page}&key={randomkey}&alt=json"
            headers = {
                "User-Agent": UserAgent().random
            }
            proxy=args.proxy if args.proxy else None
            async with session.get(url, headers=headers, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                if response.status != 200:
                    return googles
                
                data = await response.json()
                for item in data.get("items", []):
                    subdomains = item.get("displayLink")
                    if subdomains:
                        googles.append(subdomains)
                    
            page+1
                
    except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Google API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Google API, due to Serverside Error", file=sys.stderr)
                
    except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Google API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Google API, due to Clientside connection Error", file=sys.stderr)
                    
    except TimeoutError as e:
               if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Google API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Google API, due to Timeour Error", file=sys.stderr)
        
    except KeyboardInterrupt as e:
            quit()
              
    except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: Exception at req block of google: {e}, {type(e)}{reset}", file=sys.stderr)
