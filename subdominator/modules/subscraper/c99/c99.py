import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents,singlekeyloader
C99s = []

async def c99(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "c99" not in args.include_resources and not args.all:
            return C99s
        
        if args.exclude_resources and "c99" in args.exclude_resources:
            return C99s
        
        randomkey = await singlekeyloader(configs, "c99")
        if randomkey is None:
            return C99s

        url = f"https://api.c99.nl/subdomainfinder?key={randomkey}&domain={domain}&json=true"
        headers = {"User-Agent": UserAgents()}
        
        response: httpx.Response = await session.request("GET",url, headers=headers,timeout=args.timeout)
        if response.status_code != 200:
            return C99s
        data = response.json()
        if "subdomain" in data:
            subs= [entry["subdomain"] for entry in data]
            C99s.extend(subs)
    except httpx.TimeoutException as e:
        logger(f"Timeout Reached for C99 API due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in C99 API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by C99 API: {len(C99s)}", "info", args.no_color)
        return C99s