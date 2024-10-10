from colorama import Fore, Style
import aiofiles
import random
import yaml
import httpx
import sys
import os
import asyncio
import json
bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

merklemaps = []
async def Merklemap(Domain, args): # use this method
    try:
        page = 1
        proxy = args.proxy if args.proxy else None
        while True:
            async with httpx.AsyncClient(proxy=proxy, verify=False) as session:
                response = await session.request("GET", f"https://api.merklemap.com/search?query=*.{Domain}&page={page}", timeout=httpx.Timeout(connect=args.timeout, read=1000.0, write=None, pool=None))
                data = response.json()
                if not data['results']:
                    return merklemaps
                for result in data['results']:
                    if 'domain' in result:
                        domain = result.get('domain')
                        cname = result.get('subject_common_name')
                        merklemaps.append(domain)
                        merklemaps.append(cname)
                page +=1
    except httpx._exceptions.ConnectTimeout:
        if args.show_timeout_info:
            if not args.no_color:   
                print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Merklemap API, due to ClientSide connection Error", file=sys.stderr)      
            else:  
                print(f"[INFO]: Timeout reached for Merklemap API, due to Clientside connection Error", file=sys.stderr) 
    except httpx._exceptions.ConnectError:
        if args.show_timeout_info:
            if not args.no_color:   
                print(f"[{bold}{red}INFO{reset}]: {bold}{white}Unable to establish client connection to Merklemap API{reset}", file=sys.stderr)      
            else:  
                print(f"[INFO]: Unable to establish client connection to Merklemap API", file=sys.stderr) 
    except httpx._exceptions.ReadTimeout:
        return merklemaps
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]Exception occred in merklemap: {e}, {type(e)}", file=sys.stderr)
        return merklemaps
        
async def merklemap(Domain, args):
    try:
        resploader = []
        url = f"https://api.merklemap.com/search?query=*.{Domain}&stream=true"
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", url, timeout=httpx.Timeout(connect=30, read=1000.0, write=None, pool=None)) as response:
                lines = []
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        resploader.append(line[6:])
        for line in resploader:
            json_data = json.loads(line)
            domain = json_data.get("domain",'')
            cname  = json_data.get("subject_common_name",'')
            merklemaps.append(domain)
            merklemaps.append(cname)
    except httpx._exceptions.ConnectTimeout:
        if args.show_timeout_info:
            if not args.no_color:   
                print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Merklemap API, due to ClientSide connection Error", file=sys.stderr)      
            else:  
                print(f"[INFO]: Timeout reached for Merklemap API, due to Clientside connection Error", file=sys.stderr) 
    except httpx._exceptions.ConnectError:
        if args.show_timeout_info:
            if not args.no_color:   
                print(f"[{bold}{red}INFO{reset}]: {bold}{white}Unable to establish client connection to Merklemap API{reset}", file=sys.stderr)      
            else:  
                print(f"[INFO]: Unable to establish client connection to Merklemap API", file=sys.stderr) 
    except httpx._exceptions.ReadTimeout:
        return merklemaps
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]Exception occred in merklemap: {e}, {type(e)}", file=sys.stderr)
    finally:
        return merklemaps
    