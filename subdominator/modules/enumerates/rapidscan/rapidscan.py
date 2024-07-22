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

async def rapidscan(domain, session, configs, username, args):
    try:
        try:
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "rapidapi" not in data:
                    
                    return 
                
                randvalue = data.get("rapidapi", [])
                
                if randvalue is None:  
                    return []
                   
            randomkey = random.choice(data.get("rapidapi", []))
            if randomkey is None:
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in rapidscan reader block: {e}, {type(e)}{reset}",file=sys.stderr)
                
        try:
            rapidscans = []
            url =  "https://subdomain-scan1.p.rapidapi.com/"
            params = {"domain":f"{domain}"}
            auth = {
	        "X-RapidAPI-Key": f"{randomkey}",
	        "X-RapidAPI-Host": "subdomain-scan1.p.rapidapi.com"
            }
            proxy = args.proxy if args.proxy else None
            async with session.get(url, headers=auth, timeout=20, params=params,proxy=proxy, ssl=False) as response:
                if response.status == 403:
                    if args.show_key_info:
                        if not args.no_color:
                            print(f"[{bold}{red}ALERT{reset}]: Rapidscan blocking our request, {username} please check that you subscribed to rapidscan API service: {randomkey}", file=sys.stderr)
                        else:
                            print(f"[ALERT]: Rapidscan blocking our request, {username} please check that you subscribed to rapidscan API service: {randomkey}", file=sys.stderr)
                    return []
                
                if  response.status != 200:
                    if args.show_key_info:
                        if not args.no_color:
                        
                            print(f"[{bold}{red}ALERT{reset}]: Rapidscan blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                        else:
                            print(f"[ALERT]: Rapidscan blocking our request, {username} please check your api usage for this key: {randomkey}", file=sys.stderr)
                    return []
                
                data = await response.json()
                for subdomain in data:
                    rapidscans.append(subdomain)
                return rapidscans
        
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Rapidscan API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Rapidscan API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Rapidscan API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Rapidscan API, due to Clientside connection Error", file=sys.stderr) 
        
        except KeyboardInterrupt as e:
            quit()
                           
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api rapidscan req block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
                    
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in rapidscan main block: {e}, {type(e)}{reset}", file=sys.stderr)