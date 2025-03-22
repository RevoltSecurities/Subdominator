import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, singlekeyloader
fullhunts = []

async def fullhunt(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "fullhunt" not in args.include_resources and not args.all:
            return fullhunts

        if args.exclude_resources and "fullhunt" in args.exclude_resources:
            return fullhunts

        randomkey = await singlekeyloader(configs, "fullhunt")
        if randomkey is None:
            return fullhunts
        url = f"https://fullhunt.io/api/v1/domain/{domain}/subdomains"
        headers = {
            "User-Agent": UserAgents(),
            "X-API-KEY": randomkey
        }
        response: httpx.Response = await session.request("GET", url, headers=headers, timeout=args.timeout)
        if response.status_code != 200:
            if args.show_key_info:
                logger(f"FullHunt blocking our request, {username}, please check your API usage for this key: {randomkey}","warn",args.no_color)
            return fullhunts
        data = response.json()
        subdomains = data.get("hosts", [])
        fullhunts.extend(subdomains)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for FullHunt API, due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in FullHunt API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total subdomains found by FullHunt API: {len(fullhunts)}", "info", args.no_color)
        return fullhunts
