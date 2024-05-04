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

async def binaryget(domain, session, randkey, pagenum, pagesize, args):
    
    try:
        url = f"https://api.binaryedge.io/v2/query/domains/subdomain/{domain}?page={pagenum}&pagesize={pagesize}"
        auth = {
            'User-Agent': UserAgent().random,
            'X-Key': f'{randkey}'
        }
        proxy = args.proxy if args.proxy else None
        async with session.get(url, timeout=args.timeout, headers=auth, proxy=proxy, ssl=False) as response:
            data = await response.json()
            if response.status != 200:
                return 
            subdomains = data.get("events", [])
            if subdomains:
                return subdomains
            
    except aiohttp.ServerConnectionError as e:
            
        if args.show_timeout_info:
            if not args.no_color: 
                print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Binaryegde API, due to Serverside Error", file=sys.stderr)    
            else:
                print(f"[INFO]: Timeout reached for Binaryegde API, due to Serverside Error", file=sys.stderr)
                    
    except TimeoutError as e:
        if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Binaryegde API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Binaryegde API, due to Timeout Error", file=sys.stderr)
                    
    except KeyboardInterrupt as e:
        quit()
                
    except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Binaryegde API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Binaryegde API, due to Clientside connection Error", file=sys.stderr) 
            
    except Exception as e:
        if args.sec_deb:
            print(f"Exception in binaryget: {e}, {type(e)}",file=sys.stderr)
        

async def binaryedge(domain, session, configs, username, args):
        
    try:
        
        try:
            
            binaryedges = []
            
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "binaryedge" not in data:
                    
                    return []
                
                randvalue = data.get("binaryedge", [])
                
                if randvalue is None:  

                    return []

            randomkey = random.choice(data.get("binaryedge", []))
            
            if randomkey is None:
                
                return []
            pagenum = 1
            pagesize = 100
        
            while True:
            
                subdomains = await binaryget(domain, session, randomkey, pagenum, pagesize, args)
            
                if subdomains:
                
                    for subdomain in subdomains:
                    
                        binaryedges.append(subdomain)
                    
                if not subdomains:
                    if len(binaryedge)>0:
                        return binaryedges
                    else:
                        return []
            
                pagenum += 1
            
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
            print(f"Exception occured in api binaryedge reader block: {e}, due to: {type(e)}", file=sys.stderr)
        