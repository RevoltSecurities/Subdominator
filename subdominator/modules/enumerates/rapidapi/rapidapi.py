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

async def rapidapi(domain, session, configs, username, args):
    
    try:
        
        try:
            
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "rapidapi" not in data:
                    
                    return
                
                elif "whoisxmlapi" not in data:
                    
                    return
                else:
                    
                    pass
                
                randomrapidkey = random.choice(data.get("rapidapi", []))
                
                randomwhoiskey = random.choice(data.get("whoisxmlapi", []))
                
                if randomrapidkey is None:
                    
                    return
                
                if randomwhoiskey is None:
                    
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
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at rapidapi reader block: {e}, {type(e)}{reset}", file=sys.stderr)
                    
        try:
            
            rapids = []
            
            url = "https://subdomains-lookup.p.rapidapi.com/api/v1"
            
            params = {"domainName": domain,"apiKey": randomwhoiskey ,"outputFormat":"JSON"}
            
            auth = {
	                "X-RapidAPI-Key": randomrapidkey,
	                "X-RapidAPI-Host": "subdomains-lookup.p.rapidapi.com"
                 }
            proxy = args.proxy if args.proxy else None
            async with session.get(url, params=params, headers=auth,timeout=args.timeout, proxy=proxy, ssl=False) as response:
                
                data = await response.json()
                
                if response.status != 200:
                    
                    if args.show_key_info:
                        
                        if not args.no_color:
                        
                            print(f"[{bold}{red}ALERT{reset}]: Rapidadpi blocking our request, {username} please check your api usage for this keys: {randomwhoiskey}, {randomrapidkey}", file=sys.stderr)
                            
                        else:
                            
                            print(f"[ALERT]: Rapidapi blocking our request, {username} please check your api usage for this keys: {randomwhoiskey}, {randomrapidkey}", file=sys.stderr)
                    
                    return []
                
                subdomains = data.get('result', {}).get('records', [])
                
                for sub in subdomains:
                    
                    subdomain = sub.get("domain")
                    
                    if subdomain:
                        
                        rapids.append(subdomain)
                        
                return rapids
        
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for RapidAPI API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for RapidAPI API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for RapidAPI API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for RapidAPI API, due to Clientside connection Error", file=sys.stderr) 
             
        except KeyboardInterrupt as e:
            quit()
        
        except TimeoutError as e:
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for RapidAPI API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for RapidAPI API, due to Timeout Error", file=sys.stderr)
                    
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api rapid req block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
            
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api rapid main block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
            