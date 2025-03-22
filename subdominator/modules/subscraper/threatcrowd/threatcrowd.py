import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents
threatcrowds = []

async def threatcrowd(domain: str, session: httpx.AsyncClient, args):
    try:
        if args.include_resources and "threatcrowd" not in args.include_resources and not args.all:
            return threatcrowds

        if args.exclude_resources and "threatcrowd" in args.exclude_resources:
            return threatcrowds

        headers = {"User-Agent": UserAgents()}
        url = f"http://ci-www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"
        response: httpx.Response = await session.get(url, timeout=args.timeout, headers=headers)
        if response.status_code != 200:
            return threatcrowds

        data = response.json()
        if "subdomains" in data:
            for subdomain in data["subdomains"]:
                if subdomain.endswith(f".{domain}"):
                    threatcrowds.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for ThreatCrowd API, due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in ThreatCrowd API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by ThreatCrowd API: {len(threatcrowds)}", "info", args.no_color)
        return threatcrowds