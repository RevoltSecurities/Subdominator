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

async def chaos(domain, session, configs, username, args):
    
    try:
        try:
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "chaos" not in data:
                    
                    return 
                
                randvalue = data.get("chaos", [])
                
                if randvalue is None:  
                      
                    return []
                   
            randomkey = random.choice(data.get("chaos", []))
            
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in chaos reader block: {e}, {type(e)}{reset}",file=sys.stderr)
                
        if randomkey is None:
        
            return []
    
        try:
        
            Chaos = []
        
            url = f"https://dns.projectdiscovery.io/dns/{domain}/subdomains"
        
            auth = {
            'Authorization': randomkey
            }
            proxy = args.proxy if args.proxy else None
            async with session.get(url, headers=auth, timeout=args.timeout, proxy=proxy, ssl=False) as response:
            
                data = await response.json()
            
                if response.status != 200:
                    
                    if args.show_key_info:
                        
                        if not args.no_color:
                        
                            print(f"[{bold}{red}ALERT{reset}]: Chaos blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                        else:
                            print(f"[ALERT]: Chaos blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                    
                    return []
                
                if 'subdomains' in data:
                            
                    subdomains = data['subdomains']
                            
                    for subdomain in subdomains:
                                            
                        if not subdomain.endswith(f".{domain}"):
                                
                            Chaos.append(f"{subdomain}.{domain}")
                                                
                        else:
                                                
                            Chaos.append(f"{subdomain}")
                        
                    return Chaos
              
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Chaos API, due to Serverside Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for Chaos API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Chaos API, due to ClientSide connection Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for Chaos API, due to Clientside connection Error", file=sys.stderr) 
        
        except KeyboardInterrupt as e:
            quit()
                           
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api chaos req block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
            
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api chaos main block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
        
        
            
            
        
        