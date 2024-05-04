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

async def getID(domain, session, host, key, args):
    try:
        baseurl = f"https://{host}/phonebook/search?k={key}"
        auth = {
            "User-Agent": UserAgent().random
        }
        
        reqbody = {
            "Maxresults": 100000,
            "Media": 0,
            "Target": 1,
            "Term": domain,
            "Terminate": None,
            "Timeout" : 20,
            
        }
        
        async with session.post(baseurl, headers=auth, timeout=10, json=reqbody) as response:
            if response.status != 200:
                return
            data = await response.json()
            id = data.get("id")
            return id
        
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured at intelx getID block: {e}, {type(e)}{reset}", file=sys.stderr)

async def intelx(domain , session, configs, username, args):
    
    try:
        
        try:
            intelxs = []
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "intelx" not in data:
                    
                    return 
                
                randvalue = data.get("intelx", [])
                
                if randvalue is None:  
                      
                    return  
                   
            randomkeys = random.choice(data.get("intelx", []))
            
            randhost, randkey = randomkeys.split(":")
            
            if randhost is None or randkey is None:
                return
            
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in intelx reader block: {e}, {type(e)}{reset}", file=sys.stderr)
            
        try:
            
            id = await getID(domain, session, randhost, randkey, args)
            if not id:
                return
            
            while True:
                baseurl = f"https://{randhost}/phonebook/search/result?k={randkey}&id={id}&limit=10000"
                auth = {
                "User-Agent": UserAgent().random
                }
                proxy = args.proxy if args.proxy else None
                async with session.get(baseurl, headers=auth, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                    if response.status != 200:
                        return
                    data = await response.json()
                    for item in data.get('selectors', []):
                        subdomain = item.get('selectorvalue')
                        if subdomain:
                            intelxs.append(subdomain)
                        
                    if data.get('status') not in [0, 3]:
                        return intelxs
                    
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for IntelX API, due to Serverside Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for IntelX API, due to Serverside Error", file=sys.stderr)
                    
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for IntelX API, due to ClientSide connection Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for IntelX API, due to Clientside connection Error", file=sys.stderr) 
        
        except TimeoutError as e:
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for IntelX API, due to Timeout Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for IntelX API, due to Timeout Error", file=sys.stderr)
        
        except KeyboardInterrupt as e:
            quit()

        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occred at intelx req block: {e}, {type(e)}{reset}", file=sys.stderr)
        
    except Exception as e:
        
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at intelx main block: {e}, {type(e)}{reset}", file=sys.stderr)