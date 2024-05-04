from colorama import Fore, Style
import aiofiles
import random
import yaml
import aiohttp
import sys
from fake_useragent import UserAgent

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

async def censys(domain, session, configs, username, args): # code converted from subfinder gloang --> Subdominator python
    
    try:
        
        try:
            
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "censys" not in data:
                    
                    return []
                
                rand = data.get("censys", [])
                
                if rand is None:
                    
                    return []
                randomkeys = random.choice(data.get("censys", []))
                
                if randomkeys is None:
                    
                    return []
                
                randomtoken, randomsecret = randomkeys.split(":")
                
                if randomtoken is None or randomsecret is None:
                    
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in censys reader block: {e}, {type(e)}{reset}", file=sys.stderr)
                    
        try:
            
            censyss = []
            url = "https://search.censys.io/api/v2/certificates/search"
            maxpage = 10
            maxdata = 100
            cursor = None
            params = {'q': domain, 'per_page': maxdata}
            proxy = args.proxy if args.proxy else None
            
            for _ in range(maxpage+1):
                
                if cursor:
                    
                    params['cursor'] = cursor
                    
                async with session.get(url, auth=aiohttp.BasicAuth(randomtoken, randomsecret), params=params, proxy=proxy, ssl=False) as response:
                    
                    data = await response.json()
                    if response.status != 200:
                        if args.show_key_info:
                            if not args.no_color:
                                print(f"[{bold}{red}ALERT{reset}]: Censys blocking our request, {username} please check your api usage for this keys: {randomsecret}, {randomtoken}", file=sys.stderr)
                            else:
                                print(f"[ALERT]: Censys blocking our request, {username} please check your api usage for this keys: {randomsecret}, {randomtoken}", file=sys.stderr)
                        if len(censyss) > 0:
                            return censyss
                        else:
                            return []
                    
                    if 'result' in data and 'hits' in data['result']:
                        
                        for hit in data['result']['hits']:
                            
                            for name in hit.get('names', []):
                                
                                censyss.append(name)
                                
                        cursor = data['result']['links'].get('next')
                        
                        if not cursor:
                            
                            break
                        
            return censyss
        
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Censys API, due to Serverside Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for Censys API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Censys API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Censys API, due to Clientside connection Error", file=sys.stderr) 
                    
        except TimeoutError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Censys API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Censys API, due to Timeout Error", file=sys.stderr) 
                
        except KeyboardInterrupt as e:
            quit()
            
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api censys req block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
                    
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api censys main block: {e}, due to: {type(e)}{reset}", file=sys.stderr)