import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, singlekeyloader
rapidscans = []

async def rapidscan(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "rapidscan" not in args.include_resources and not args.all:
            return rapidscans

        if args.exclude_resources and "rapidscan" in args.exclude_resources:
            return rapidscans

        randomkey = await singlekeyloader(configs, "rapidapi")
        if randomkey is None:
            return rapidscans

        url = "https://subdomain-scan1.p.rapidapi.com/"
        params = {"domain": domain}
        headers = {
            "User-Agent": UserAgents(),
            "X-RapidAPI-Key": randomkey,
            "X-RapidAPI-Host": "subdomain-scan1.p.rapidapi.com"
        }

        response: httpx.Response = await session.get(url, headers=headers, timeout=args.timeout, params=params)
        
        if response.status_code == 403:
            if args.show_key_info:
                logger(f"Rapidscan blocking our request, {username} please check that you subscribed to the Rapidscan API service: {randomkey}", "warn", args.no_color)
            return rapidscans

        if response.status_code != 200:
            if args.show_key_info:
                logger(f"Rapidscan blocking our request, {username} please check your API usage for this key: {randomkey}", "warn", args.no_color)
            return rapidscans

        data = response.json()
        for subdomain in data:
            rapidscans.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Rapidscan API, due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in Rapidscan API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Rapidscan API: {len(rapidscans)}", "info", args.no_color)
        return rapidscans