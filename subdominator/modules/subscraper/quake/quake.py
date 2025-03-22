import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader, UserAgents
quakes = []

async def quake(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "quake" not in args.include_resources and not args.all:
            return quakes
        if args.exclude_resources and "quake" in args.exclude_resources:
            return quakes

        randomkey = await singlekeyloader(configs, "quake")
        if randomkey is None:
            return quakes

        url = "https://quake.360.net/api/v3/search/quake_service"
        headers = {
            "User-Agent": UserAgents(),
            "Accept": "*/*",
            "Accept-Language": "en",
            "Connection": "close",
            "Content-Type": "application/json",
            "X-Quaketoken": randomkey
        }
        data = {
            "query": f"domain: {domain}",
            "include": ["service.http.host"],
            "latest": True,
            "start": 0,
            "size": 500,
        }
        response: httpx.Response = await session.request("POST",url,headers=headers,json=data,timeout=args.timeout)
        if response.status_code != 200:
            if args.show_key_info:
                logger(f"Quake API blocking request. {username}, check API key usage: {randomkey}", "warn", args.no_color)
            return quakes
        result = response.json()
        for entry in result.get("data", []):
            subdomain = entry.get("service", {}).get("http", {}).get("host")
            if subdomain:
                quakes.append(subdomain)
    except httpx.TimeoutException:
        if args.show_timeout_info:
            logger("Timeout reached for Quake API", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in Quake API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Quake API: {len(quakes)}", "info", args.no_color)
        return quakes