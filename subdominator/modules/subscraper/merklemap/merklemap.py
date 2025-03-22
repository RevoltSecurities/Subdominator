import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader
merklemaps = []

async def merklemap(domain: str, session: httpx.AsyncClient, configs: str, username, args):
    try:
        if args.include_resources and "merklemap" not in args.include_resources and not args.all:
            return merklemaps
        if args.exclude_resources and "merklemap" in args.exclude_resources:
            return merklemaps

        randomkey = await singlekeyloader(configs,"merklemap")
        if randomkey is None:
            return merklemaps

        url = "https://api.merklemap.com/v1/search"
        headers = {"Authorization": f"Bearer {randomkey}"}
        params = {"query": f"*.{domain}", "page": 0, "type": "wildcard"}
        while True:
            response: httpx.Response = await session.request("GET",url, headers=headers, params=params, timeout=httpx.Timeout(connect=args.timeout, read=1000.0, write=None, pool=None))

            if response.status_code != 200:
                return merklemaps
            
            data = response.json()
            results = data.get("results", [])
            if not results:
                break  
            for result in results:
                hostname = result.get("hostname", "")
                common_name = result.get("subject_common_name", "")
                if hostname and hostname.endswith(f".{domain}"):
                    merklemaps.append(hostname)
                if common_name and common_name.endswith(f".{domain}"):
                    merklemaps.append(common_name)
            params["page"] += 1  
    except httpx.TimeoutException:
        if args.show_timeout_info:
            logger("Timeout reached for Merklemap API", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in Merklemap API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total subdomains found by Merklemap API: {len(merklemaps)}", "info", args.no_color)
        return merklemaps