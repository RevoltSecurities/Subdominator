import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, singlekeyloader
Shodans = []

async def shodanapi(url: str, domain: str, session: httpx.AsyncClient, randkey: str, args):
    try:
        headers = {"User-Agent": UserAgents()}
        response: httpx.Response = await session.get(url, headers=headers, timeout=args.timeout)
        if response.status_code != 200:
            if args.show_key_info:
                logger(f"Shodan blocking request, check API usage for key: {randkey}", "warn", args.no_color)
            return []
        data = response.json()
        return [f"{sub}.{domain}" for sub in data.get("subdomains", [])]
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Shodan API due to: {e}", "warn", args.no_color)
    except httpx.RequestError as e:
        if args.show_timeout_info:
            logger(f"Request error in Shodan API: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in Shodan API request module due to: {e}, {type(e)}", "warn", args.no_color)
    return []


async def shodan(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "shodan" not in args.include_resources and not args.all:
            return Shodans

        if args.exclude_resources and "shodan" in args.exclude_resources:
            return Shodans

        randomkey = await singlekeyloader(configs, "shodan")
        if randomkey is None:
            return Shodans
        url = f"https://api.shodan.io/dns/domain/{domain}?key={randomkey}"
        subdomains = await shodanapi(url, domain, session, randomkey, args)
        Shodans.extend(subdomains)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in Shodan API module: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Shodan API: {len(Shodans)}", "info", args.no_color)
        return Shodans