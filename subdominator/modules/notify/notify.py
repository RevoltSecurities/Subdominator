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

async def reader(service, configs, username,args):
    try:
            async with aiofiles.open(configs, "r") as streamr:
                
                data = yaml.safe_load(await streamr.read())
                
                if f"{service}" not in data:
                    return 
                
                randvalue = data.get(f"{service}", [])
                
                if randvalue is None:  
                    return
                   
            randomkey = random.choice(data.get(f"{service}", []))
            return randomkey
            
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
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in notify reader block: {e}, {type(e)}{reset}",file=sys.stderr)
            
async def slack(domain, subdomains, url, session, args):
    try:
        results = '\n'.join(subdomains)
        payloads = {"text": f"Total subdomains {len(subdomains)} found for {domain}:\n{results}"}
        async with session.post(url, json=payloads) as response:
            pass
    except aiohttp.ClientConnectionError as e:
        pass
    except TimeoutError as e:
        pass
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in slack sender: {e}, {type(e)}{reset}", file=sys.stderr)
            

async def pushbullet(domain, subdomains, randomkey, session, args):
    try:
        url = f'https://api.pushbullet.com/v2/pushes'  
        results = '\n'.join(subdomains)
        headers = {
            'Access-Token': randomkey,
            
            'Content-Type': 'application/json'
            }
        jdata = {
            'type': 'note',
            'title': f"Total subdomains {len(subdomains)} found for {domain}:",
            'body': f"{results}"
        }
        async with session.post(url, headers=headers, json=jdata) as response:
            pass
        
    except aiohttp.ClientConnectionError as e:
        pass
    except TimeoutError as e:
        pass
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in slack sender: {e}, {type(e)}{reset}", file=sys.stderr)
            
            
async def notify(domain, subdomains, configpath, username, args):
    try:
        
        url = await reader("slack", configpath, username, args)
        randomkey = await reader("pushbullet", configpath, username, args)
        
        async with aiohttp.ClientSession() as session:
            if url:
                await slack(domain, subdomains, url,session, args)
            if randomkey:
                await pushbullet(domain, subdomains, randomkey, session, args)
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}exception in notify: {e}, {type(e)}{reset}", file=sys.stderr)