import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, singlekeyloader
odin_results = []

async def odin(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        
        if args.include_resources and "odin" not in args.include_resources and not args.all:
            return odin_results
        
        if args.exclude_resources and "odin" in args.exclude_resources:
            return odin_results
        
        randomkey = await singlekeyloader(configs, "odin")
        if randomkey is None:
            return odin_results
        url = "https://api.odin.io/v1/domain/subdomain/search"
        headers = {
            "X-API-Key": randomkey,
            "Content-Type": "application/json",
            "User-Agent": UserAgents(),
        }
        limit = 1000  
        start = None 

        while True:
            payload = {
                "domain": domain,
                "limit": limit,
                "start": start if start else []
            }
            response: httpx.Response = await session.request("POST", url, headers=headers, json=payload, timeout=args.timeout)
            if response.status_code != 200:
                if args.show_key_info:
                    logger(f"Odin API request failed with status {response.status_code}. Check API key or rate limits.", "warn", args.no_color)
                return odin_results

            data = response.json()
            
            if not data.get("success"):
                return odin_results
            
            subdomains = data.get("data", [])
            odin_results.extend(subdomains)

            pagination = data.get("pagination", {})
            start = pagination.get("last")
            if not start or len(subdomains) == 0: 
                break
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Odin API, due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in Odin API module: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Odin API: {len(odin_results)}", "info", args.no_color)
        return odin_results