import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, dualkeyloader
redhuntlabs_subdomains = []

async def redhuntapi(url: str, domain: str, session: httpx.AsyncClient, randkey: str, pagenum: int, pagesize: int, args):
    try:
        base_url = f"{url}?domain={domain}&page_size={pagesize}&page={pagenum}"
        headers = {"User-Agent": UserAgents(), "X-BLOBR-KEY": randkey}
        response: httpx.Response = await session.get(base_url, headers=headers, timeout=args.timeout)
        if response.status_code != 200:
            return []
        data = response.json()
        return data.get("subdomains", [])
    except httpx.TimeoutException:
        if args.show_timeout_info:
            logger("Timeout reached for RedHuntLabs API", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in RedHuntLabs API request: {e}, {type(e)}", "warn", args.no_color)
    return []


async def redhuntlabs(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "redhuntlabs" not in args.include_resources and not args.all:
            return redhuntlabs_subdomains

        if args.exclude_resources and "redhuntlabs" in args.exclude_resources:
            return redhuntlabs_subdomains

        url,randkeys = await dualkeyloader(configs, "redhuntlabs", True)
        if url is None or randkeys is None:
            return redhuntlabs_subdomains
        pagenum = 1
        pagesize = 1000
        while True:
            subdomains = await redhuntapi(url, domain, session, randkeys, pagenum, pagesize, args)
            if not subdomains:
                break
            redhuntlabs_subdomains.extend(subdomains)
            pagenum += 1
    except Exception as e:
        if args.verbose:
            logger(f"Exception in RedHuntLabs API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by RedHuntLabs API: {len(redhuntlabs_subdomains)}", "info", args.no_color)
        return redhuntlabs_subdomains