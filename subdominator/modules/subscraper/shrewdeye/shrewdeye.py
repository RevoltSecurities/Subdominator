import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents
Shrewdeyes = []

async def shrewdeye(domain: str, session: httpx.AsyncClient, args):
    try:
        if args.include_resources and "shrewdeye" not in args.include_resources and not args.all:
            return Shrewdeyes
        
        if args.exclude_resources and "shrewdeye" in args.exclude_resources:
            return Shrewdeyes
        
        url = f"https://shrewdeye.app/domains/{domain}.txt"
        headers = {"User-Agent":UserAgents()}
        response = await session.request("GET",url,timeout=args.timeout,headers=headers)
        if response.status_code != 200:
            return Shrewdeyes
        data = response.text.strip()
        if not data:
            return Shrewdeyes
        subdomains = data.split("\n")
        Shrewdeyes.extend(subdomains)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Shrewdeye API due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in Shrewdeye API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Shrewdeye: {len(Shrewdeyes)}", "info", args.no_color)
        return Shrewdeyes