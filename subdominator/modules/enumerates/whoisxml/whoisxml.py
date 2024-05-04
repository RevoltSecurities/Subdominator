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

async def whoisxml(domain, session, configs, username, args):
    
    try:
        
        try:
            async with aiofiles.open(configs, "r") as streamr:
                data = yaml.safe_load(await streamr.read())
                if "whoisxmlapi" not in data:
                    return 
                
                randvalue = data.get("whoisxmlapi", [])
                
                if randvalue is None:  
                    return  
            randomkey = random.choice(data.get("whoisxmlapi", []))
            
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in whoisxmlapi request block: {e}, {type(e)}{reset}", file=sys.stderr)
                    
        if randomkey is None:
            return []
            
        try:
            
            whoisxmls = []
            
            url = f"https://subdomains.whoisxmlapi.com/api/v1?apiKey={randomkey}&domainName={domain}"  
            proxy = args.proxy if args.proxy else None
            async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                
                data = await response.json()
                if response.status != 200:
                    if args.show_key_info:
                        if not args.no_color:
                            print(f"[{bold}{red}ALERT{reset}]: Whoisxmlapi blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                            
                        else:
                            print(f"[ALERT]: Whoisxmlapi blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                    return []
                
                found_result = data.get('result', {}).get('records', [])
                
                for subdomains in found_result:
                    
                    subdomain = subdomains.get('domain')
                    
                    if subdomain:
                        
                        whoisxmls.append(subdomain)               
                
                return whoisxmls
            
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Whoisxml API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for whoisxml API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Whoisxml API, due to ClientSide connection Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for Whoisxml API, due to Clientside connection Error", file=sys.stderr) 
                                      
        except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Whoisxml API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Whoisxml API, due to Timeout Error", file=sys.stderr)
                    
        except KeyboardInterrupt as e:
            quit()
            
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in whoisxmlapi request block: {e}, {type(e)}{reset}", file=sys.stderr)
            
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in whoisxmlapi main block: {e}, {type(e)}{reset}", file=sys.stderr)
