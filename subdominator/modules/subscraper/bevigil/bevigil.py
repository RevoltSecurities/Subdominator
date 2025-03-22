import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents,singlekeyloader
bevigils = []

async def bevigil(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "bevigil" not in args.include_resources and not args.all:
            return bevigils
        
        if args.exclude_resources and "bevigil" in args.exclude_resources:
            return bevigils
        
        randomkey = await singlekeyloader(configs,"bevigil")
        
        if randomkey is None:
            return bevigils
        
        url = f"https://osint.bevigil.com/api/{domain}/subdomains"
        headers = {
        'User-Agent': UserAgents(),
        'X-Access-Token': randomkey
        }
        response: httpx.Response = await  session.request("GET",url, headers=headers, timeout=args.timeout)
        if response.status_code != 200:
            if args.show_key_info:
                logger(f"Bevigil blocking our request, {username} please check your api usage for this key: {randomkey}", "warn", args.no_color)
            return []
        data = response.json()
        subdomains = data.get("subdomains", [])
        for subdomain in subdomains:
            bevigils.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Bevigil API, due to: {e}", "warn", args.no_color)    
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in Bevigil API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomins found by Bevigil API: {len(bevigils)}", "info", args.no_color)
        return bevigils