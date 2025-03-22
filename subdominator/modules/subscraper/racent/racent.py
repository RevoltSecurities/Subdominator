import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents
racents = []

async def racent(domain: str, session: httpx.AsyncClient, args):
    try:
        if args.include_resources and "racent" not in args.include_resources and not args.all:
            return racents
        if args.exclude_resources and "racent" in args.exclude_resources:
            return racents
        url = f"https://face.racent.com/tool/query_ctlog?keyword={domain}"
        headers = {"User-Agent": UserAgents()}
        response: httpx.Response = await session.get(url,headers=headers,timeout=args.timeout)
        if response.status_code != 200:
            return racents
        data = response.json()
        if "CTLog 查询超过限制" in data:
            return racents
        for subdomains in data.get['data']['list']:
            for subdomain in subdomains.get("dnsnames", []):
                racents.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Racent API due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception at Racent API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Racent API: {len(racents)}", "info", args.no_color)
        return racents