import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader
from subdominator.modules.utils.utils import UserAgents

pugrecons = []

async def pugrecon(domain: str , session: httpx.AsyncClient,configs: str,args):
    try:
        if args.include_resources and "pugrecon" not in args.include_resources and not args.all:
            return pugrecons
        if args.exclude_resources and "pugrecon" in args.exclude_resources:
            return pugrecons

        randomkey = await singlekeyloader(configs, "pugrecon")
        if not randomkey:
            return pugrecons
        
        url = "https://pugrecon.com/api/v1/domains"

        headers = {
            "User-Agent": UserAgents(),
            "Authorization": f"Bearer {randomkey}",
            "Content-Type": "application/json"
        }

        json_data = {
            "domain_name": domain
        }

        response: httpx.Response = await session.request("POST", url, headers=headers, json=json_data, timeout=args.timeout)
        if response.status_code !=200:
            if args.verbose:
                logger(f"Pugrecon API returned bad response status:{response.status_code}.", "warn", args.no_color)
            return pugrecons
        
        data = response.json()
        for items in data.get("results"):
            subdomain = items.get("name")
            if subdomain.endswith(f".{domain}"):
                pugrecons.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout exception occurred in the Pugrecon API due to: {e}", "warn", args.no_color)    
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in Pugrecon module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Pugrecon API: {len(pugrecons)}", "info")
        return pugrecons