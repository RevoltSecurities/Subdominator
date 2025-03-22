import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents,dualkeyloader
googles = []

async def google(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "google" not in args.include_resources and not args.all:
            return googles

        if args.exclude_resources and "google" in args.exclude_resources:
            return googles
        page = 1
        if args.dork:
            dork = args.dork
        else:
            dork = f"site:*.{domain}%20-www"
        while True:
            randomcx, randomkey = await dualkeyloader(configs, "google", False)
            if randomcx is None or randomkey is None:
                return googles
            url = f"https://customsearch.googleapis.com/customsearch/v1?q={dork}&cx={randomcx}&num=10&start={page}&key={randomkey}&alt=json"
            headers = {
                "User-Agent": UserAgents()
            }
            response: httpx.Response = await session.request("GET", url, headers=headers, timeout=args.timeout)
            if response.status_code != 200:
                return googles
            data = response.json()
            items = data.get("items", [])
            if not items:
                return googles
            for item in items:
                subdomain = item.get("displayLink")
                if subdomain:
                    googles.append(subdomain)
            page += 1
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Google API, due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in Google API module: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total subdomains found by Google API: {len(googles)}", "info", args.no_color)
        return googles