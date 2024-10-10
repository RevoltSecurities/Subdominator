from colorama import Fore, Style
import aiofiles
import random
import yaml
import httpx
import sys
from fake_useragent import UserAgent
import asyncio

bold = Style.BRIGHT
blue = Fore.BLUE
red = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL

Trickest = []
sem = asyncio.Semaphore(50)


async def get_count(session, offset, domain, args):
    try:
        response = await session.request("GET", f"""https://api.trickest.io/solutions/v1/public/solution/a7cba1f1-df07-4a5c-876a-953f178996be/view?q=hostname ~ ".{domain}"&dataset_id=a0a49ca9-03bb-45e0-aa9a-ad59082ebdfc&limit=50&offset={offset}&select=hostname&orderby=hostname""", timeout=args.timeout)
        data = response.json()
        count = data.get("total_count")
        if count:
            return count
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api trickest get count block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
            

async def fetcher(session, offset, domain, args):
    try:
        async with sem:
            response = await session.request("GET", f"""https://api.trickest.io/solutions/v1/public/solution/a7cba1f1-df07-4a5c-876a-953f178996be/view?q=hostname ~ ".{domain}"&dataset_id=a0a49ca9-03bb-45e0-aa9a-ad59082ebdfc&limit=50&offset={offset}&select=hostname&orderby=hostname""", timeout=httpx.Timeout(read=300.0, connect=args.timeout, write=None, pool=None))
            data = response.json()
            results = data.get('results', [])
            if results:
                for result in results:
                    subdomain = result['hostname']
                    if subdomain.endswith(f".{domain}"):
                        Trickest.append(subdomain)
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api trickest fetcher block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
            

async def trickest(domain, configs, username, args): # well we can do it in while but will give very slow performance.
    try:
        tasks = []
        try:
            async with aiofiles.open(configs, "r") as streamr:
                data = yaml.safe_load(await streamr.read())
                if "trickest" not in data:
                    return []
                randvalue = data.get("trickest", [])
                if randvalue is None:  
                    return []
            randomkey = random.choice(data.get("trickest", []))
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
        except KeyboardInterrupt:
            exit()
        except asyncio.CancelledError:
            exit()
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception in trickest reader block: {e}, {type(e)}{reset}",file=sys.stderr)
        if randomkey is None:
            return []
        try:
            headers = {
                "User-Agent": UserAgent().random,
                "Authorization": f"Token {randomkey}"
            }
            async with httpx.AsyncClient(verify=False, proxy=args.proxy if args.proxy else None, headers=headers) as requests:
                total = await get_count(requests, 10, domain, args)
                if not total or total == 0:
                    return Trickest
                finals = int(total) / 10
                offset = 10
                for _ in range(0,int(finals)+1,1):
                    task = asyncio.ensure_future(fetcher(requests, offset, domain, args))
                    tasks.append(task)
                    offset+=10
                await asyncio.gather(*tasks, return_exceptions=False)
        except httpx._exceptions.ConnectTimeout:
            if args.show_timeout_info:
                if not args.no_color:   
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Timeout reached for Trickest API, due to ClientSide connection Error", file=sys.stderr)      
                else:  
                    print(f"[INFO]: Timeout reached for Trickest API, due to Clientside connection Error", file=sys.stderr) 
        except httpx._exceptions.ConnectError:
            if args.show_timeout_info:
                if not args.no_color:   
                    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Unable to establish client connection to Trickest API{reset}", file=sys.stderr)      
                else:  
                    print(f"[INFO]: Unable to establish client connection to Trickest API", file=sys.stderr) 
        except httpx._exceptions.ReadTimeout:
            pass
        except KeyboardInterrupt:
            exit()
        except asyncio.CancelledError:
            exit()
        except Exception as e:
            if args.sec_deb:
                print(f"[{bold}{red}WRN{reset}]Exception occred in trickest: {e}, {type(e)}", file=sys.stderr)
    except KeyboardInterrupt:
        exit()
    except asyncio.CancelledError:
        exit()
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception occured in api trickest main block: {e}, due to: {type(e)}{reset}", file=sys.stderr)
    finally:
        return Trickest