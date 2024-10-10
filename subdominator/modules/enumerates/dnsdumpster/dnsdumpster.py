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
        
        try:
            
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "dnsdumpster" not in data:
                    
                    return []
                
                rand = data.get("dnsdumpster", [])
                
                if rand is None:
                    
                    return []
                
                cooktoken = random.choice(data.get("dnsdumpster", []))
                
                randcookie, randtoken = cooktoken.split(":")
                
                if randcookie is None or randtoken is None:
                    
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
            
            dnsdumpsters = []
            
            url = f"https://dnsdumpster.com/"
                
            auth = {
                'Cookie': f'csrftoken={randcookie}',
                'User-Agent': UserAgent().random,
                'Referer': 'https://dnsdumpster.com/'
                }
            
            data = {
                'csrfmiddlewaretoken': f'{randtoken}',
                'targetip': domain,
                'user': 'free'
               }
            proxy = args.proxy if args.proxy else None
            async with session.post(url, headers=auth, data=data, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                
                data = await response.text()
                
                if response.status != 200:
                    return []
                
                pattern = re.compile(rf"\b[a-zA-Z0-9]+\b\.{domain}\b")
                
                subdomains = pattern.findall(data)
                
                subdomains1 = re.findall(fr'(?<=http://)[\w.-]+(?=\.{domain})', data) #re from stf
                
                for subs in subdomains1:
                    if not subs.endswith(f"{domain}"): 
                        dnsdumpsters.append(f"{subs}.{domain}") 
                    else:
                        dnsdumpsters.append(subs) 
                                        
                for subdomain in subdomains:
                    if not subdomain.endswith(f"{domain}"): 
                        dnsdumpsters.append(f"{subdomain}.{domain}")
                    else:
                        dnsdumpsters.append(subdomain)
                        
                return dnsdumpsters
            
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
                    
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api dnsdumpster main block: {e}, due to: {type(e)}", file=sys.stderr)
                
