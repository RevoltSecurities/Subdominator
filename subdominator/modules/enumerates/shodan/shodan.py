from colorama import Fore, Style
import aiofiles
import random
import yaml
import aiohttp
import sys
import asyncio

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def shodan(domain, session, configs, username, args):
    
    try:
        
        try:
            
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
            
            if "shodan" not in data:
                return
            
            rand = data.get("shodan", [])
            
            if rand is None:
                return
            
            randomkey = random.choice(data.get("shodan", []))
            
            if randomkey is None:
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
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in shodan reader block: {e}, {type(e)}{reset}", file=sys.stderr)
                
        try:
            
            shodans = []
            
            url = f"https://api.shodan.io/dns/domain/{domain}?key={randomkey}"
            proxy = args.proxy if args.proxy else None
            
            async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                data = await response.json()
                if response.status != 200:
                    return
                
                subdomains = data.get("subdomains", [])
                
                for subdomain in subdomains:
                    
                    shodans.append(f"{subdomain}.{domain}")
                    
                return shodans
            
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Shodan API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Shodan API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Shodan API, due to ClientSide connection Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for Shodan API, due to Clientside connection Error", file=sys.stderr) 
        
        except KeyboardInterrupt as e:
            quit()
        
        except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Shodan API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Shodan API, due to Timeout Error", file=sys.stderr)
                           
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in shodan request block: {e}, {type(e)}{reset}", file=sys.stderr)
            
    except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in shodan main block: {e}, {type(e)}{reset}", file=sys.stderr)
        