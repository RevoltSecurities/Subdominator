import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader
leakixs = []

async def leakix(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "leakix" not in args.include_resources and not args.all:
            return leakixs
        if args.exclude_resources and "leakix" in args.exclude_resources:
            return leakixs

        randomkey = await singlekeyloader(configs, "leakix")
        if not randomkey:
            return leakixs

        url = f"https://leakix.net/api/subdomains/{domain}"
        headers = {"accept": "application/json", "api-key": randomkey}
        response: httpx.Response = await session.request("GET",url, headers=headers, timeout=args.timeout)

        if response.status_code != 200:
            if args.show_key_info:
                logger(f"LeakIX blocking request, {username} check API usage for key: {randomkey}", "alert", args.no_color)
            return leakixs
        data = response.json()
        for item in data:
            subdomain = item.get("subdomain")
            if subdomain:
                leakixs.append(subdomain)
    except httpx.TimeoutException:
        if args.show_timeout_info:
            logger("Timeout reached for LeakIX API", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in LeakIX API module: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total subdomains found by LeakIX API: {len(leakixs)}", "info", args.no_color)
        return leakixs