import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, singlekeyloader

rapidfinders = []

async def rapidfinder(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "rapidfinder" not in args.include_resources and not args.all:
            return rapidfinders

        if args.exclude_resources and "rapidfinder" in args.exclude_resources:
            return rapidfinders

        randomkey = await singlekeyloader(configs, "rapidapi")
        if randomkey is None:
            return rapidfinders

        url = "https://subdomain-finder3.p.rapidapi.com/v1/subdomain-finder/"
        params = {"domain": domain}
        headers = {
            "User-Agent": UserAgents(),
            "X-RapidAPI-Key": randomkey,
            "X-RapidAPI-Host": "subdomain-finder3.p.rapidapi.com"
        }

        response: httpx.Response = await session.get(url, headers=headers, timeout=args.timeout, params=params)
        if response.status_code == 403:
            if args.show_key_info:
                logger(f"Rapidfinder blocking our request, {username} please check that you subscribed to the Rapidfinder API service: {randomkey}", "warn", args.no_color)
            return rapidfinders

        if response.status_code != 200:
            if args.show_key_info:
                logger(f"Rapidfinder blocking our request, {username} please check your API usage for this key: {randomkey}", "warn", args.no_color)
            return rapidfinders

        data = response.json()
        for item in data["subdomains"]:
            rapidfinders.append(item["subdomain"])
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Rapidfinder API, due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in Rapidfinder API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Rapidfinder API: {len(rapidfinders)}", "info", args.no_color)
        return rapidfinders
