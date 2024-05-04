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

async def redhuntapi(url, domain, session, randkey, pagenum, pagesize, args):
    try:
        
        base_url = f"{url}?domain={domain}&page_size={pagesize}&page={pagenum}"
        auth = {
            "X-BLOBR-KEY": randkey
        }
        proxy = args.proxy if args.proxy else None
        async with session.get(base_url, headers=auth, timeout=args.timeout, proxy=proxy, ssl=False) as response:
            
            if response.status !=200:
                return 
            data = await response.json()
            
            if 'subdomains' in data:
            
                return data['subdomains']
            return 
    except TimeoutError as e:
        if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Redhuntlabs API, due to Timeout Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Redhuntlabs API, due to Timeout Error", file=sys.stderr)
                    
    except aiohttp.ServerConnectionError as e:
            
            if args.show_timeout_info:
                if not args.no_color: 
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Redhuntlabs API, due to Serverside Error", file=sys.stderr)    
                else:
                    print(f"[INFO]: Timeout reached for Redhuntlabs API, due to Serverside Error", file=sys.stderr)
                
    except aiohttp.ClientConnectionError as e:
            
            if args.show_timeout_info:
                 
                if not args.no_color: 
                    
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Redhuntlabs API, due to ClientSide connection Error", file=sys.stderr)    
                    
                else:
                    
                    print(f"[INFO]: Timeout reached for Redhuntlabs API, due to Clientside connection Error", file=sys.stderr) 
            
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at request redhuntlabs: {e}, {type(e)}{reset}", file=sys.stderr)
            
    
async def redhuntlabs(domain, session, configs, username, args):
    
    try:
        try:
            
            redhuntlabss = []
            
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if "redhuntlabs" not in data:
                    
                    return
                
                rand = data.get("redhuntlabs", [])
                
                if rand is None:
                    
                    return
                randomkeys = random.choice(data.get("redhuntlabs", []))
                
                if randomkeys is None:
                    
                    return
                url, randkeys = randomkeys.rsplit(":", 1)
                
                if randkeys is None:
                    return
                
                if url:
                    url = url
                else:
                    url = f"https://reconapi.redhuntlabs.com/community/v1/domains/subdomains"
            
            pagenum = 1
            
            pagesize = 1000
            
            while True:
                
                subdomains = await redhuntapi(url, domain, session, randkeys, pagenum, pagesize, args)
                
                if not subdomains:
                    if len(redhuntlabss)>0:
                        return redhuntlabss
                    return 
                
                redhuntlabss.extend(subdomains)
                
                pagenum +=1
                
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
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception at main redhuntlabs: {e}, {type(e)}{reset}", file=sys.stderr)
                    
                
                
            
            
            