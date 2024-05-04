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

async def randomkeys(configs, username, args):
    try:
            
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "netlas" not in data:
                    
                    return
                
                rand = data.get("netlas", [])
                
                if rand is None:
                    return
                
                randomkey = random.choice(data.get("netlas", []))
                
                
                if randomkey is None:
                    
                    return
                return randomkey
                
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
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in netlas randomkey: {e}, {type(e)}{reset}", file=sys.stderr)
            

async def netlas(domain, session, configs, username, args):
    
    try:
        
        try:
            
            netlass = []
            
            getcount = f"https://app.netlas.io/api/domains_count/?q=domain:*.{domain}+AND+NOT+domain:{domain}"
            
            randomkey = await randomkeys(configs, username, args)
            
            if randomkey is None:
                
                return []
            
            getauth = {
                "accept":    "application/json",
                "X-API-Key": f"{randomkey}"
            }
            proxy = args.proxy if args.proxy else None
            async with session.get(getcount, headers=getauth, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                
                responsed = await response.json()
                if response.status !=200:
                    return []
                
                counts = responsed['count']
                                
            for val in range(0, counts+10, 20):
                
                url = f"https://app.netlas.io/api/domains/?q=domain:*.{domain}+AND+NOT+domain:{domain}&source_type=include&start={val}"
                
                randomKey = await randomkeys(configs, username, args)
                
                auth = {
                "accept":    "application/json",
                "X-API-Key": f"{randomKey}"
            }
                
                async with session.get(url, headers=auth, timeout=args.timeout, proxy=proxy, ssl=False) as response:
                    
                    data = await response.json()
                    
                    if response.status != 200:
                        
                        if len(netlass)>0:
                            return netlass
                        else:
                            return []
                    for item in data['items']:
                    
                        subdomain = item['data']['domain']   
                        netlass.append(subdomain)
                          
            return netlass    
        
        except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Netlas API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Netlas API, due to Serverside Error", file=sys.stderr)
                
        except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Netlas API, due to ClientSide connection Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Netlas API, due to Clientside connection Error", file=sys.stderr)
                    
        except TimeoutError as e:
               if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Netlas API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Netlas API, due to Timeour Error", file=sys.stderr)
        
        except KeyboardInterrupt as e:
            quit()
              
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: Exception at req block of netlas: {e}, {type(e)}{reset}", file=sys.stderr)
                    
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: Exception at main block of netlas: {e}, {type(e)}{reset}", file=sys.stderr)   
        