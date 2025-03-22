import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, dualkeyloader
zoomeyes = []

async def zoomeyeapi(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "zoomeye" not in args.include_resources and not args.all:
            return zoomeyes
        
        if args.exclude_resources and "zoomeye" in args.exclude_resources:
            return zoomeyes
        
        host,randomkey = await dualkeyloader(configs, "zoomeyeapi")
        if randomkey is None:
            return zoomeyes

        base_url = f"https://{host}/domain/search"
        page = 1

        while True:
            url = f"{base_url}?q={domain}&type=1&s=1000&page={page}"
            headers = {
                "API-KEY": randomkey,
                "User-Agent": UserAgents(),
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            response: httpx.Response = await session.request("GET", url, headers=headers, timeout=args.timeout)
            if response.status_code != 200:
                if args.show_key_info:
                    logger(f"Zoomeye API blocking our request, {username} please check your API usage for this key: {randomkey}", "warn", args.no_color)
                return zoomeyes
            
            data = response.json()
            if "list" not in data:
                return zoomeyes
            subdomains = [item["name"] for item in data["list"] if "name" in item]
            zoomeyes.extend(subdomains)
            page += 1
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Zoomeye API, due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in Zoomeye API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Zoomeye API: {len(zoomeyes)}", "info", args.no_color)
        return zoomeyes