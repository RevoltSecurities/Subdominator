import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents,singlekeyloader
Builtwiths = []

async def builtwith(domain: str,session: httpx.AsyncClient, configs: str, username: str, args): 
    try:
        if args.include_resources and "builtwith" not in args.include_resources and not args.all:
            return Builtwiths
        
        if args.exclude_resources and "builtwith" in args.exclude_resources:
            return Builtwiths
        
        randomkey = await singlekeyloader(configs, "builtwith")
        if randomkey is None:
            return Builtwiths
        url = f"https://api.builtwith.com/v21/api.json?KEY={randomkey}&HIDETEXT=yes&HIDEDL=yes&NOLIVE=yes&NOMETA=yes&NOPII=yes&NOATTR=yes&LOOKUP={domain}"
        headers = {
            "User-Agent": UserAgents()
        }
        response: httpx.Response =  await session.request("GET",url, headers=headers, timeout=args.timeout)
        if response.status_code != 200:
            if args.show_key_info:
                logger(f"Builtwith blocking our request, {username} please check your api usage for this key: {randomkey}", "warn", args.no_color)
            return Builtwiths
        
        jdata = response.json()
        if isinstance(jdata, dict):
            results = jdata.get("Results", [])
            for result in results:
                for chunk in result.get("Result", {}).get("Paths", []):
                    domain_name = chunk.get("Domain", "")
                    subdomain = chunk.get("SubDomain", "")                  
                    if domain_name and subdomain:
                        Builtwiths.append(f"{subdomain}.{domain_name}")
    except httpx.TimeoutException as e:
        logger(f"Timeout reached for Builtwith API, due to: {e}", "warn", args.no_color) 
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in Builtwith API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Builtwith API: {len(Builtwiths)}", "info", args.no_color)
        return Builtwiths