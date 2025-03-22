import httpx
import re
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents
rapiddnss = []

async def rapiddns(domain: str, session: httpx.AsyncClient, args):
    try:
        if args.include_resources and "rapiddns" not in args.include_resources and not args.all:
            return rapiddnss
        if args.exclude_resources and "rapiddns" in args.exclude_resources:
            return rapiddnss
        for pagenum in range(1, 8):
            url = f"https://rapiddns.io/subdomain/{domain}?page={pagenum}"
            headers = {"User-Agent": UserAgents()}
            response: httpx.Response = await session.request("GET",url,headers=headers,timeout=args.timeout)
            data = response.text
            filterdomain = re.escape(domain)
            pattern = rf'(?i)(?:https?://)?([a-zA-Z0-9*_.-]+\.{filterdomain})'
            subdomains = re.findall(pattern, data)
            rapiddnss.extend(subdomains)
            if "Next" not in data:
                return rapiddnss
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for RapidDNS due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in RapidDNS module due to: {e}, type: {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by RapidDNS: {len(rapiddnss)}", "info", args.no_color)
        return rapiddnss