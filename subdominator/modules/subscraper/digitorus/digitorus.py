import httpx
import re
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents
digitorus_subs = []

async def digitorus(domain: str, session: httpx.AsyncClient, args):
    try:
        if args.include_resources and "digitorus" not in args.include_resources and not args.all:
            return digitorus_subs
        
        if args.exclude_resources and "digitorus" in args.exclude_resources:
            return digitorus_subs

        url = f"https://certificatedetails.com/{domain}"
        headers = {"User-Agent": UserAgents()} 
        response: httpx.Response = await session.get(url, headers=headers, timeout=args.timeout)
        if response.status_code != 200:
            logger(f"Digitorus API returned bad response status: {response.status_code}.", "warn", args.no_color)
            return digitorus_subs

        data = response.text
        filterdomain = re.escape(domain)
        pattern = r'(?i)(?:https?://)?([a-zA-Z0-9*_.-]+\.' + filterdomain + r')'
        subdomains = re.findall(pattern, data)
        if subdomains:
            digitorus_subs.extend(subdomains)

    except httpx.TimeoutException as e:
        logger(f"Timeout reached for Digitorus API due to: {e}", "warn", args.no_color)

    except Exception as e:
        logger(f"Exception occurred in Digitorus API module: {e}, {type(e)}", "warn", args.no_color)

    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Digitorus API: {len(digitorus_subs)}", "info", args.no_color)
        return digitorus_subs