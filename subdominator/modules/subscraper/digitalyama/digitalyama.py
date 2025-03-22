import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, singlekeyloader
digitalyamas = []

async def digitalyama(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:

        if args.include_resources and "digitalyama" not in args.include_resources and not args.all:
            return digitalyamas
        
        if args.exclude_resources and "digitalyama" in args.exclude_resources:
            return digitalyamas
        
        randomkey = await singlekeyloader(configs, "digitalyama")
        if randomkey is None:
            return digitalyamas
        
        url = "https://api.digitalyama.com/subdomain_finder"
        params = {"domain": domain}
        headers = {
            "User-Agent": UserAgents(),
            "x-api-key": randomkey
        }
        response: httpx.Response = await session.request("GET", url, headers=headers, params=params, timeout=args.timeout)
        if response.status_code != 200:
            if args.show_key_info:
                logger(f"DigitalYama blocking our request, {username} please check your API usage for this key: {randomkey}", "warn", args.no_color)
            return []

        data = response.json()
        subdomains = data.get("subdomains", [])
        for subdomain in subdomains:
            digitalyamas.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for DigitalYama API, due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in DigitalYama API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by DigitalYama API: {len(digitalyamas)}", "info", args.no_color)
        return digitalyamas