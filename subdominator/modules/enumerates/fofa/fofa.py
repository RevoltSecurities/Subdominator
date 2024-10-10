from colorama import Fore, Style
import aiofiles
import random
import yaml
import aiohttp
import sys
import base64

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def fofa(domain, session, configs, username, args):
    try:
        try:
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "fofa" not in data:
                    return 
                
                randvalue = data.get("fofa", [])
                
                if randvalue is None:  
                    return []
                   
            randomkey = random.choice(data.get("fofa", []))
            
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in fofa reader block: {e}, {type(e)}{reset}",file=sys.stderr)
                
        if randomkey is None:
            return []
        
        try:
            
            FOFA = []
            pagenum = 1
            domain_encoded = f"""domain="{domain}" """.encode('utf-8')
            subdomains = base64.b64encode(domain_encoded).decode('utf-8')
            
            proxy = args.proxy if args.proxy else None
            while True:
                url = f"https://fofa.info/api/v1/search/all?key={randomkey}&qbase64={subdomains}&page={pagenum}&full=true&size=1000"
                async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                    if response.status != 200:
                        return FOFA
                    data = await response.json()
                    if "results" not in data:
                        return FOFA
                    for result in data.get('results', []):
                        url = result[0]
                        if url.startswith("https://"):
                            url = url.replace("https://", "")
                        elif url.startswith("http://"):
                            url = url.replace("http://", "") 
                        else :
                            url = url
                        if ':' in url:
                            subdomain = url.split(':')[0]
                        else:
                            subdomain = url
                        FOFA.append(subdomain)
                        
                        for r in FOFA:
                            print(r)
                    
                    size = data.get('size')
                    print(size)
                    if size < 1000:
                        return FOFA
                    pagenum += 1
    
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for FOFA API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for FOFA API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for FOFA API, due to ClientSide connection Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for FOFA API, due to Clientside connection Error", file=sys.stderr) 
        
        except KeyboardInterrupt as e:
            quit()
                           
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api fofa req block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
            
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api fofa main block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
        