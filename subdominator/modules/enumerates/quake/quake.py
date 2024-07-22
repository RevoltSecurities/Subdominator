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

async def quake(domain, session, configs, username, args):
    
    try:
        
        try:
            
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "quake" not in data:
                    
                    return 
                
                randvalue = data.get("quake", [])
                
                if randvalue is None:  
                      
                    return  
                   
            randomkey = random.choice(data.get("quake", []))
            
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured at quake read block: {e}, {type(e)}{reset}", file=sys.stderr)
            
        try:
            quakes = []
            url = f"https://quake.360.net/api/v3/search/quake_service"
            data = {
                'query': f'domain: {domain}',
                'include': ['service.http.host'],
                'latest': True,
                'start': 0,
                'size': 500,
            }
            
            auth = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0',
                'Accept': '*/*',
                'Accept-Language': 'en',
                'Connection': 'close',
                'Content-Type': 'application/json',
                'X-Quaketoken': randomkey
            }
            proxy = args.proxy if args.proxy else None
            async with session.post(url, headers=auth, json=data, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                                
                if response.status != 200:
                    if args.show_key_info:
                            if not args.no_color:
                                print(f"[{bold}{red}ALERT{reset}]: Quake blocking our request, {username} please check your api usage for this keys: {randomkey}", file=sys.stderr)
                            else:
                                print(f"[ALERT]: Quake blocking our request, {username} please check your api usage for this keys: {randomkey}", file=sys.stderr)
                    return []
                
                data = await response.json()
                                
                for entry in data['data']:
                    
                    subdomain = entry['service']['http']['host']
                    quakes.append(subdomain)
                    
                return quakes
            
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Quake API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Quake API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Quake API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Quake API, due to Clientside connection Error", file=sys.stderr) 
            
        except KeyboardInterrupt as e:
            quit()
            
        except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Quake API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Quake API, due to Timeout Error", file=sys.stderr)
                    
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at quake req: {e}, {type(e)}{reset}", file=sys.stderr)
            
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at quake main: {e}, {type(e)}{reset}", file=sys.stderr)
    