from colorama import Fore, Style
import aiofiles
import random
import yaml
import aiohttp
import sys
import re
from fake_useragent import UserAgent

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def dnsdumpster(domain, session, configs, username, args):
    
    try:
        dnsdumpsters = []
        
        try:
            
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "dnsdumpster" not in data:
                    
                    return []
                
                rand = data.get("dnsdumpster", [])
                
                if rand is None:
                    
                    return []
                
                randomapikey = random.choice(data.get("dnsdumpster", []))
                
                if randomapikey is None:
                    return []
                
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in dnsdumpster reader block: {e}, {type(e)}", file=sys.stderr) 
        try:
            sections = ['a', 'cname', 'mx', 'ns']
            
            url = f"https://api.dnsdumpster.com/domain/{domain}"
            headers = {
                "X-API-Key": randomapikey
            }
            page = 1
            proxy = args.proxy if args.proxy else None
            while True:
                params = {"page": page}
                async with session.get(url, headers=headers, params=params,timeout=args.timeout, proxy=proxy, ssl=False) as response:
                    if response.status != 200:
                        return dnsdumpsters
                    
                    data = await response.json()
                    
                    error = data.get("error", None)
                    if error is not None:
                        return dnsdumpsters
                    
                    for section in sections:
                        if section in data:
                            matching_domains = [
                                record["host"] for record in data[section] if record["host"].endswith(f".{domain}")
                                ]
                            dnsdumpsters.extend(matching_domains)
                    page +=1
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Dnsdumpster API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Dnsdumpster API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Dnsdumpster API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Dnsdumpster API, due to Clientside connection Error", file=sys.stderr) 
        
        except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Dnsdumpster API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Dnsdumpster API, due to Timeout Error", file=sys.stderr)
                    
        except KeyboardInterrupt as e:
            quit()
                           
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api dnsdumpster req block: {e}, due to: {type(e)}{reset}", file=sys.stderr)  
            return dnsdumpsters
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api dnsdumpster main block: {e}, due to: {type(e)}", file=sys.stderr)
        return dnsdumpsters