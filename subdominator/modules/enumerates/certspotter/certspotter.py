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

async def certspotter(domain, session, configs, username, args):
    
    try:
        
        try:
            
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "certspotter" not in data:
                    
                    return [] 
                
                randvalue = data.get("certspotter", [])
                
                if randvalue is None:  
                      
                    return []
                   
            randomkey = random.choice(data.get("certspotter", []))
            
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in certspotter reader block: {e}, {type(e)}{reset}", file=sys.stderr)
                    
        if randomkey is None:
        
            return []
        
        try:
            
            certspotters = []
            
            url = f"https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names"
            
            auth = {"Authorization": f"Bearer {randomkey}"}
            proxy = args.proxy if args.proxy else None
            async with session.get(url, headers=auth, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                
                data = await response.json()
                
            if response.status != 200:
                
                return []
            
            for entry in data :
                    
                dns_names = entry.get('dns_names',[])
                    
                for dns_name in dns_names:
                        
                    if dns_name.startswith("*.") and dns_name.endswith(f".{domain}"):
                            
                        subdomain = dns_name[2:]
                            
                        certspotters.append(subdomain)
                        
                    elif dns_name.endswith(f".{domain}"):
                            
                        certspotters.append(dns_name)
                        
                    else:
                            pass
                        
            return certspotters
        
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Certspotter API, due to Serverside Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for Certspotter API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Certspotter API, due to ClientSide connection Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for Certspotter API, due to Clientside connection Error", file=sys.stderr) 
             
        except KeyboardInterrupt as e:
            quit()
            
        except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Certspotter API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Certspotter API, due to Timeout Error", file=sys.stderr)
                    
        except Exception as e:
            if args.sec_deb:    
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api certspotter req block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
            
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api certpotter main block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
