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

async def securitytrails(domain, session, configs, username, args):
    
    try:
        
        try:
            
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "securitytrails" not in data:
                    
                    return 
                
                randvalue = data.get("securitytrails", [])
                
                if randvalue is None:  
                      
                    return  
                   
            randomkey = random.choice(data.get("securitytrails", []))
            
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in securitytrails reader block: {e}, {type(e)}{reset}", file=sys.stderr)
                    
        if randomkey is None:
        
            return []
        
        try:
            
            SecurityTrails = []
            
            url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains?children_only=false&include_inactive=true"
            
            auth = {
                "accept": "application/json",
                "APIKEY": randomkey
            }
            proxy = args.proxy if args.proxy else None
            async with session.get(url, headers=auth, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                
                data = await response.json()
                                                
                if response.status != 200:
                    
                    if args.show_key_info:
                        
                        if not args.no_color:
                            print(f"[{bold}{red}ALERT{reset}]: SecurityTrails blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                        else:
                            print(f"[ALERT]: SecurityTrails blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                    
                    return []
                
                subdomains = data.get("subdomains", [])
                    
                for subdomain in subdomains:
                            
                    SecurityTrails.append(f"{subdomain}.{domain}")
                        
                return SecurityTrails
                  
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for SecurityTrails API, due to Serverside Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for SecurityTrails API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for SecurityTrails API, due to ClientSide connection Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for SecurityTrails API, due to Clientside connection Error", file=sys.stderr) 
             
        except TimeoutError as e:
            if args.sec_deb:
                if args.show_timeout_info:
                    if not args.no_color: 
                    
                        print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for SecurityTrails API, due to Timeout Error", file=sys.stderr)    
                    else:
                        print(f"[INFO]: Timeout reached for SecurityTrails API, due to Timeout Error", file=sys.stderr)
                        
        except KeyboardInterrupt as e:
            quit()
                        
        except Exception as e:
            
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in securitytrails request block: {e}, {type(e)}{reset}", file=sys.stderr)
            
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in securitytrails main block: {e}, {type(e)}{reset}", file=sys.stderr)
            