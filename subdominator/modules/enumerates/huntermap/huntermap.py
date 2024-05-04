from colorama import Fore, Style
import aiofiles
import random
import yaml
import aiohttp
import sys
import datetime
from datetime import datetime, timedelta
import base64


bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def randomkeys(configs, username, args):
    try:
            async with aiofiles.open(configs, "r") as streamr:
                data = yaml.safe_load(await streamr.read())
                if "huntermap" not in data:  
                    return
                rand = data.get("huntermap", [])
                if rand is None:
                    return
                randomkey = random.choice(data.get("huntermap", []))
                
                if randomkey is None:
                    return 
                return randomkey
        
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at randomkey huntermap: {e}, {type(e)}{reset}", file=sys.stderr)

async def huntermap(domain, session, configs, username, args):
    
    try:
        try:
            
            hunterhows = []
            endtime =  datetime.now().strftime("%Y-%m-%d")
            yeartime =  datetime.now() - timedelta(days=27.8*12)
            inititatetime = yeartime.strftime("%Y-%m-%d")
            query = base64.urlsafe_b64encode(domain.encode("utf-8")).decode('ascii')
            page_size = 100
            page =1 
            
            while True:
                randomapikey = await randomkeys(configs, username, args)
                if not randomapikey:
                    return
                url = f"https://api.hunter.how/search?api-key={randomapikey}&query={query}&start_time={inititatetime}&end_time={endtime}&page={page}&page_size={page_size}"
                proxy = args.proxy if args.proxy else None
                async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                    
                    data = await response.json()
                    if response.status !=200:
                        if args.show_key_info:
                            if not args.no_color:
                             print(f"[{bold}{red}ALERT{reset}]: Huntermap blocking our request, {username} please check your api usage for this key: {randomapikey}", file=sys.stderr)
                            else:
                                print(f"[ALERT]: Huntermap blocking our request, {username} please check your api usage for this key: {randomapikey}", file=sys.stderr)
                        if len(hunterhows)>0:
                            return hunterhows
                        return []
                    
                    subdomains =  data.get("data", {}).get("list", [])
                    
                    total =  data.get("data", {}).get("total", 0)
                        
                    for subdomain in subdomains: 
                        subdomain =  subdomain['domain']
                        if subdomain.endswith(f"{domain}"):
                            hunterhows.append(subdomain)
                            
                    if total <= len(hunterhows):
                        for subdomain in hunterhows:
                            if subdomain.endswith(f"{domain}"):
                                hunterhows.append(subdomain)
                    
                        return hunterhows
                    page +=1
                    
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color:  
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Huntermap API, due to Serverside Error", file=sys.stderr)     
                else:
                    print(f"[INFO]: Timeout reached for Huntermap API, due to Serverside Error", file=sys.stderr)
                    
        except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color:  
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Huntermap API, due to Timeout Error", file=sys.stderr)     
                else:
                    print(f"[INFO]: Timeout reached for Huntermap API, due to Timeout Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color:   
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Huntermap API, due to ClientSide connection Error", file=sys.stderr)      
                else:  
                    print(f"[INFO]: Timeout reached for Huntermap API, due to Clientside connection Error", file=sys.stderr) 
        except AttributeError as e:
            return hunterhows
        
        except KeyboardInterrupt as e:
            quit()
        
        except Exception as e:
            return hunterhows

    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}INFO{reset}]: {bold}{white}At main huntermap: {e}, {type(e)}{reset}", file=sys.stderr)        
                    
                    
            
            