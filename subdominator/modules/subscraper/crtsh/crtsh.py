import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents
crtshs = []

async def crtsh(domain: str, session: httpx.AsyncClient, args):
    try:
        if args.include_resources and "crtsh" not in args.include_resources and not args.all:
            return crtshs
        
        if args.exclude_resources and "crtsh" in args.exclude_resources:
            return crtshs

        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        headers = {
            "User-Agent": UserAgents()
        }

        timeout = httpx.Timeout(timeout=args.timeout, connect=args.timeout, read=300, write=args.timeout)
        response: httpx.Response = await session.request("GET", url, headers=headers, timeout=timeout)

        if response.status_code != 200:
            if args.verbose:
                logger(f"crt.sh API returned bad response status: {response.status_code}.", "warn", args.no_color)
            return crtshs

        data = response.json()
        for domains in data:
            for subdomain in domains["name_value"].split("\n"):
                crtshs.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for crt.sh API due to : {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in crt.sh API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by crt.sh API: {len(crtshs)}", "info", args.no_color)
        return crtshs