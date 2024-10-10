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


async def facebook(domain, session, configs, username, args):
    try:
        
        try:
            async with aiofiles.open(configs, "r") as streamr:
                data = yaml.safe_load(await streamr.read())
                if "facebook" not in data:
                    return []
                randvalue = data.get("facebook", [])
                if randvalue is None:  
                    return []
                
            randomkeys = random.choice(data.get("facebook", []))
            randomid, randomsecret = randomkeys.split(":")
            
            if randomid is None or randomsecret is None:
                return []
        
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at fb key loader: {e}, {type(e)}{reset}", file=sys.stderr)
            
        try:
            fbcerts = []
            randomtoken = f"{randomid}|{randomsecret}"
            url = f"https://graph.facebook.com/v18.0/certificates?fields=domains&access_token={randomtoken}&query={domain}&limit=1000"
            proxy = args.proxy if args.proxy else None
            while True:
                async with session.get(url, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                    if response.status != 200:
                        return fbcerts
                    data = await response.json()
                    for item in data['data']:
                        subdomains = item['domains']
                        for subdomain in subdomains:
                            if subdomain.endswith(f"{domain}"):
                                fbcerts.append(subdomain)
                    pages = data.get("paging", {})
                    next_page = pages.get('next')
                    if next_page:
                        url = next_page
                    if not next_page:
                        return fbcerts

        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Facebook API, due to Serverside Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for Facebook API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Facebook API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Facebook API, due to Clientside connection Error", file=sys.stderr) 
        
        except KeyboardInterrupt as e:
            quit()
            
        except TimeoutError as e:
           if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Facebook API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Facebook API, due to Timeout Error", file=sys.stderr) 
           return fbcerts
                           
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api facebook req block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
            
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at fb main: {e}, {type(e)}{reset}", file=sys.stderr)
            
        

        