import httpx
import re
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents
Sitedossiers = []

async def sitedossier(domain: str, session: httpx.AsyncClient, args):
    try:
        if args.include_resources and "sitedossier" not in args.include_resources and not args.all:
            return Sitedossiers
        
        if args.exclude_resources and "sitedossier" in args.exclude_resources:
            return Sitedossiers
        
        page = 1
        while True:
            url = f"http://www.sitedossier.com/parentdomain/{domain}/{page}"
            headers = {"User-Agent": UserAgents()}
            response = await session.request("GET",url,timeout=args.timeout, headers=headers)
            if response.status_code != 200:
                return Sitedossiers
            data = response.text
            filterdomain = re.escape(domain)
            pattern = rf'(?i)(?:https?://)?([a-zA-Z0-9*_.-]+\.{filterdomain})'
            subdomains = re.findall(pattern, data)
            Sitedossiers.extend(subdomains)
            if "Show next 100 items" not in data:
                return Sitedossiers 
            page += 100
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Sitedossier due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in Sitedossier module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Sitedossier: {len(Sitedossiers)}", "info", args.no_color)
        return Sitedossiers