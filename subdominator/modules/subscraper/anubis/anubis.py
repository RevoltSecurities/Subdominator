import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents
anubiss = []

async def anubis(domain: str, session: httpx.AsyncClient, args):
    try:
        
        if args.include_resources and "anubis" not in args.include_resources and not args.all:
            return anubiss
        
        if args.exclude_resources and "anubis" in args.exclude_resources:
            return anubiss
        
        headers = {"User-Agent": UserAgents()}
        url = f"https://anubisdb.com/anubis/subdomains/{domain}"
        response: httpx.Response = await session.get(url, timeout=args.timeout,headers=headers, follow_redirects=True)
        if response.status_code != 200:
            return anubiss
        data = response.json()
        for subdomain in data:
            if subdomain.endswith(f".{domain}") :
                anubiss.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Anubis API, due to: {e}", "warn", args.no_color)    
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in Anubis API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Anubis API: {len(anubiss)}", "info", args.no_color)
        return anubiss