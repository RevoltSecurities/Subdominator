from colorama import Fore, Style
import aiofiles
import random
import yaml
import aiohttp
import sys
import asyncio
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
                
                if "zoomeyeapi" not in data:
                    return
                
                rand = data.get("zoomeyeapi", [])
                if rand is None:
                    return
                
                randomkey = random.choice(data.get("zoomeyeapi", []))
                
                if randomkey is None:
                    return
                return randomkey
                
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
                              
    except Exception as e:
        if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in zoomeyeapi reader block: {e}, {type(e)}{reset}", file=sys.stderr)
    
async def region(domain, session,randomkey, args): 
    
    try:
        url = f"https://api.zoomeye.org/domain/search?q={domain}&type=1&s=1000&page=1"
        
        auth = {
            "API_KEY": f"{randomkey}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        async with session.get(url, headers=auth, timeout=10) as response:
            return response.status                 
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in zooeye region block: {e}, {type(e)}{reset}", file=sys.stderr)

async def zoomeyeapi(domain, session , configs, username, args):
            
        try: 
            
            zoomeyes = []
            
            testkey = await randomkeys(configs, username, args)
            
            status = await region(domain, session,testkey, args)
                
            page =1
            
            while True:
                if status != 403:
                    url = f"https://api.zoomeye.org/domain/search?q={domain}&type=1&s=1000&page={page}" # for china users
                else:
                    url = f"https://api.zoomeye.hk/domain/search?q={domain}&type=1&s=1000&page={page}"  # for other countries users
                    
                randomkey = await randomkeys(configs, username, args)
                if not randomkey:
                    if len(zoomeyes)>0:
                        return zoomeyes
                    return
                    
                auth = {
                    "API-KEY": f"{randomkey}",
                    "User-Agent": f"{UserAgent().random}"
                }
                proxy = args.proxy if args.proxy else None
                async with session.get(url, headers=auth, timeout=args.timeout, proxy=proxy,ssl=False) as response:
                    
                    data = await response.json()

                    if response.status != 200:
                        if len(zoomeyes)>0:
                            return zoomeyes
                        return
                    
                    if "list" not in data:
                        if args.show_key_info:
                            if not args.no_color:
                                print(f"[{bold}{red}ALERT{reset}]: Zoomeye blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                            else:
                                print(f"[ALERT]: Zoomeye blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                        if len(zoomeyes)>0:
                            return zoomeyes
                        return
                    
                    for item in data["list"]:
                        zoomeyes.append(item["name"])
                                
                    page +=1
                    
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Zoomeye API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Zoomeye API, due to Serverside Error", file=sys.stderr)
                    
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Zoomeye API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Zoomeye API, due to Clientside connection Error", file=sys.stderr) 
                    
        except KeyboardInterrupt as e:
            quit()        
            
        except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Zoomeye API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Zoomeye API, due to Timeout Error", file=sys.stderr)
                           
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in zoomeye request block: {e}, {type(e)}{reset}", file=sys.stderr)