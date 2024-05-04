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

async def virustotal(domain, session, configs, username, args):
    try:
        
        virustotals = []
         
        try:
            
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "virustotal" not in data:
                    
                    return 
                
                randvalue = data.get("virustotal", [])
                
                if randvalue is None:  
                      
                    return  
                   
            randomkey = random.choice(data.get("virustotal", []))
            
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in virustotal reader block: {e}, {type(e)}{reset}", file=sys.stderr) 
                     
        if randomkey is None:
            
            return
        
        try:
            
            url = f"https://www.virustotal.com/vtapi/v2/domain/report?apikey={randomkey}&domain={domain}"
            proxy = args.proxy if args.proxy else None
            
            async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False) as response:   
                if response.status != 200:  
                    
                    if args.show_key_info:
                        if not args.no_color:
                            print(f"[{bold}{red}ALERT{reset}]: Virustotal blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                        else:
                            print(f"[ALERT]: Virustotal blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                    return []
                            
                data = await response.json()  
                     
                if 'subdomains' in data:
                        subdomains = data['subdomains']    
                        for subdomain in subdomains:  
                            virustotals.append(subdomain)
                return virustotals
                
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Virustotal API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Virustotal API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Virustotal API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Virustotal API, due to Clientside connection Error", file=sys.stderr) 
             
                           
        except KeyboardInterrupt as e:
            quit()
        
        except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Virustotal API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Virustotal API, due to Timeout Error", file=sys.stderr)
                           
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in virustotal request block: {e}, {type(e)}{reset}", file=sys.stderr)
            
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api virustotal main block: {e}, due to: {type(e)}{reset}", file=sys.stderr)

            
            
                                
                                
                    
                    
            
            
            
            
            
