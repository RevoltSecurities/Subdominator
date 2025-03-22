import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, singlekeyloader
rsecloud_subdomains = []

async def rsecloudapi(url: str, domain: str, session: httpx.AsyncClient, randkey: str, page: int, args):
    try:
        json_payload = {"domain": domain}
        headers = {"User-Agent": UserAgents(), "Content-Type": "application/json", "X-API-Key": randkey}
        url = f"{url}?page={page}"
        response: httpx.Response = await session.post(url, headers=headers, json=json_payload, timeout=args.timeout)
        if response.status_code != 200:
            if args.show_key_info:
                logger(f"RseCloud blocking request, check API usage for key: {randkey}", "warn", args.no_color)
            return []
        data = response.json()
        if "error" in data:
            return [],1
        return data.get("data", []), data.get("total_pages", 1)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for RseCloud API request due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in RseCloud API request due to: {e}, {type(e)}", "warn", args.no_color)
    return [], 1

async def rsecloud(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "rsecloud" not in args.include_resources and not args.all:
            return rsecloud_subdomains

        if args.exclude_resources and "rsecloud" in args.exclude_resources:
            return rsecloud_subdomains

        randomkey = await singlekeyloader(configs, "rsecloud")
        if randomkey is None:
            return rsecloud_subdomains

        url = "https://api.rsecloud.com/api/v1/subdomains"
        page = 1
        while True:
            subdomains, total_pages = await rsecloudapi(url, domain, session, randomkey, page, args)
            if not subdomains:
                break
            rsecloud_subdomains.extend(subdomains)
            if page >= total_pages:
                break
            page += 1
    except Exception as e:
        if args.verbose:
            logger(f"Exception in RseCloud API module: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by RseCloud API: {len(rsecloud_subdomains)}", "info", args.no_color)
        return rsecloud_subdomains