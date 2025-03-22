import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents
urlscans = []

async def urlscan(domain: str, session: httpx.AsyncClient, args):
    try:
        if args.include_resources and "urlscan" not in args.include_resources and not args.all:
            return urlscans
        
        if args.exclude_resources and "urlscan" in args.exclude_resources:
            return urlscans
        headers = {"User-Agent": UserAgents()}
        url = f"https://urlscan.io/api/v1/search/?q=page.domain:{domain}&size=10000"
        response: httpx.Response = await session.request("GET", url, timeout=args.timeout, headers=headers)
        if response.status_code != 200:
            return []
        data = response.json()
        for entry in data.get("results", []):
            subdomain = entry["page"]["domain"]
            urlscans.append(subdomain)
        return urlscans
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Urlscan due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in Urlscan module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Urlscan: {len(urlscans)}", "info", args.no_color)
        return urlscans
