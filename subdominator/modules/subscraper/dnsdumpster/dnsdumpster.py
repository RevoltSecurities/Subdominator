import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader
dnsdumpsters = []

async def dnsdumpster(domain: str, session: httpx.AsyncClient, configs: str, args):    
    try:
        if args.include_resources and "dnsdumpster" not in args.include_resources and not args.all:
            return dnsdumpsters

        if args.exclude_resources and "dnsdumpster" in args.exclude_resources:
            return dnsdumpsters

        sections = ["a", "cname", "mx", "ns"]
        url = f"https://api.dnsdumpster.com/domain/{domain}"
        page = 1

        while True:
            randomkey = await singlekeyloader(configs, "dnsdumpster")
            if not randomkey:
                break
            params = {"page": page}
            headers = {"X-API-Key": randomkey}
            response: httpx.Response = await session.request("GET", url, headers=headers, params=params, timeout=args.timeout)
            if response.status_code != 200:
                return dnsdumpsters
            data = response.json()
            if "error" in data:
                return dnsdumpsters
            for section in sections:
                if section in data:
                    dnsdumpsters.extend(
                        record["host"]
                        for record in data[section]
                        if record["host"].endswith(f".{domain}")
                    )
            page += 1
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Dnsdumpster API due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in Dnsdumpster API module: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Dnsdumpster API: {len(dnsdumpsters)}", "info", args.no_color)
        return dnsdumpsters
