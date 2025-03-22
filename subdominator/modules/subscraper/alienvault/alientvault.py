import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents
alienvaults = []

async def alienvault(domain: str, session: httpx.AsyncClient,args) -> list[str]:
    try:
        if args.include_resources and "alienvault" not in args.include_resources and not args.all:
            return alienvaults
        
        if args.exclude_resources and "alienvault" in args.exclude_resources:
            return alienvaults
        
        headers = {"User-Agents": UserAgents()}
        url = f"https://otx.alienvault.com/api/v1/indicators/hostname/{domain}/passive_dns"
        response: httpx.Response = await session.request("GET",url, timeout=args.timeout, headers=headers) 
        if response.status_code != 200:
            return alienvaults
        data = response.json()
        for entries in data['passive_dns']:
            subdomain = entries['hostname']
            if subdomain.endswith(f".{domain}"):
                alienvaults.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Alienvault API, due to: {e}", "warn", args.no_color)    
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in Alienvalut module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Alienvault API: {len(alienvaults)}", "info")
        return alienvaults