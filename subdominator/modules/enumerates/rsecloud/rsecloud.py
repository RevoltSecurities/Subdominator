from colorama import Fore, Style
import aiofiles
import random
import yaml
import aiohttp
import sys

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def randomkeys(configs, username, args):
    try:
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "rsecloud" not in data:
                    
                    return 
                
                randvalue = data.get("rsecloud", [])
                
                if randvalue is None:  
                      
                    return []
                   
            randomkey = random.choice(data.get("rsecloud", []))
            
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in rsecloud reader block: {e}, {type(e)}{reset}",file=sys.stderr)
                

async def rsecloud(domain, session, configs, username, args):
            
    try:
        rseclouds = []
        page = 1
        jsons = {
            "domain": f"{domain}"
        }
        while True:
            randomkey = await randomkeys(configs, username, args)
            
            if not randomkey:
                return []
            
            url = f"https://api.rsecloud.com/api/v1/subdomains?page={page}"
            
            headers = {
                
                "Content-Type": "application/json",
                "X-API-Key": f"{randomkey}"
            }
            proxy = args.proxy if args.proxy else None
            async with session.post(url, timeout=args.timeout, proxy=proxy, ssl=False, headers=headers, json=jsons) as response:
                
                if response.status != 200:
                    if args.show_key_info:
                        if not args.no_color:
                             print(f"[{bold}{red}ALERT{reset}]: RseCloud blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                        else:
                                print(f"[ALERT]: RseCloud blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                        if len(rseclouds)>0:
                            return rseclouds
                        return []
                    
                data = await response.json()
                
                subdomains =  data.get("data", {})
                
                total = data.get("total_pages", {})
                                
                for subdomain in subdomains:
                    rseclouds.append(subdomain)
                    
                if total == page:
                    
                    return rseclouds
                
                page +=1
    
    except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color:  
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for RseClouds API, due to Serverside Error", file=sys.stderr)     
                else:
                    print(f"[INFO]: Timeout reached for RseClouds API, due to Serverside Error", file=sys.stderr)
                    
    except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color:  
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for RseClouds API, due to Timeout Error", file=sys.stderr)     
                else:
                    print(f"[INFO]: Timeout reached for RseClouds API, due to Timeout Error", file=sys.stderr)
                
    except aiohttp.ClientConnectionError as e:
            if args.show_timeout_info:
                if not args.no_color:   
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for RseClouds API, due to ClientSide connection Error", file=sys.stderr)      
                else:  
                    print(f"[INFO]: Timeout reached for RseClouds API, due to Clientside connection Error", file=sys.stderr)
                          
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api rsecloud request & main block: {e}, due to: {type(e)}{reset}", file=sys.stderr)