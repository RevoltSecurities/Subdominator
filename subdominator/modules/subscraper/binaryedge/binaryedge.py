import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents,singlekeyloader
binaryedges = []

async def binaryget(domain: str, session: httpx.AsyncClient, randkey: str, pagenum: int, pagesize: int, args):
    try:
        url = f"https://api.binaryedge.io/v2/query/domains/subdomain/{domain}?page={pagenum}&pagesize={pagesize}"
        auth = {
            'User-Agent': UserAgents(),
            'X-Key': f'{randkey}'
        }
        response: httpx.Response = await  session.request("GET",url, timeout=args.timeout, headers=auth) 
        if response.status_code != 200:
            return 
        data = response.json()
        subdomains = data.get("events", [])
        if subdomains:
            return subdomains
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Binaryegde API, due to: {e}", "warn", args.no_color)                        
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in the Binaryedge request module due to: {e}, {type(e)}","warn", args.no_color)

async def binaryedge(domain, session, configs, username, args) -> list[str]:
    try:
        if args.include_resources and "binaryedge" not in args.include_resources and not args.all:
            return binaryedges
        if args.exclude_resources and "binaryedge" in args.exclude_resources:
            return binaryedges
        pagenum = 1
        pagesize = 100
        while True:
            randomkey = await singlekeyloader(configs, "binaryedge")
            if randomkey is None:
                break
            subdomains = await binaryget(domain, session, randomkey, pagenum, pagesize, args)
            if subdomains:
                for subdomain in subdomains:
                    binaryedges.append(subdomain)
            if not subdomains:
                break
            pagenum += 1
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in the Binaryedge API due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Binaryedge API: {len(binaryedges)}", "info", args.no_color)
        return binaryedges