import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader
from urllib.parse import unquote
arpsyndicates = []

async def arpsyndicate(domain: str, session: httpx.AsyncClient, configs: str,args):
    try:
        if args.include_resources and "arpsyndicate" not in args.include_resources and not args.all:
            return arpsyndicates
        
        if args.exclude_resources and "arpsyndicate" in args.exclude_resources:
            return arpsyndicates
        
        randomkey = await singlekeyloader(configs,"arpsyndicate")
        if randomkey is None:
            return arpsyndicates
        
        url = f"https://api.subdomain.center/beta/?domain={domain}&auth={randomkey}"
        response: httpx.Response = await session.request("GET",url,timeout=args.timeout)
        if response.status_code != 200:
            return []
        data = response.json()
        arpsyndicates.extend(data)
        for subdomain in data:
            if "%" in subdomain:
                subdomain = unquote(subdomain)
            arpsyndicates.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Arpsyndicate due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in Arpsyndicate API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Arpsyndicate: {len(arpsyndicates)}", "info", args.no_color)
        return arpsyndicates