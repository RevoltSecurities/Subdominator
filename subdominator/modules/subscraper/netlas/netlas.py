import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader
netlass = []

async def netlas(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):    
    try:
        start = 0
        page_size = 20
        if args.include_resources and "netlas" not in args.include_resources and not args.all:
            return netlass
        if args.exclude_resources and "netlas" in args.exclude_resources:
            return netlass

        randomkey = await singlekeyloader(configs, "netlas")
        if randomkey is None:
            return netlass

        headers = {"accept": "application/json", "X-API-Key": randomkey}
        while True:
            req_url = f"https://app.netlas.io/api/domains/?q=domain:*.{domain}+AND+NOT+domain:{domain}&source_type=include&start={start}"
            response: httpx.Response = await session.request(
                "GET",
                req_url,
                headers=headers,
                timeout=httpx.Timeout(timeout=args.timeout, connect=args.timeout, pool=None, write=None, read=120),
            )
            if response.status_code != 200:
                if args.show_key_info:
                    logger(f"Netlas API request failed. {username}, check API key usage: {randomkey}", "warn", args.no_color)
                return netlass
            data = response.json()
            items = data.get("items", [])
            if not items:
                break  
            for item in items:
                netlass.append(item["data"]["domain"])
            start += page_size 
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Netlas API: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in Netlas API module: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Netlas API: {len(netlass)}", "info", args.no_color)
        return netlass