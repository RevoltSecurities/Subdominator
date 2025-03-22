import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents
myssls = []

async def myssl(domain: str, session: httpx.AsyncClient, args):
    try:
        if args.include_resources and "myssl" not in args.include_resources and not args.all:
            return myssls
        if args.exclude_resources and "myssl" in args.exclude_resources:
            return myssls

        url = f"https://myssl.com/api/v1/discover_sub_domain?domain={domain}"
        headers = {"User-Agent": UserAgents()}
        response: httpx.Response = await session.get(url,headers=headers,timeout=args.timeout)

        if response.status_code != 200:
            return myssls

        data = response.json()
        for subdomain in data.get("data", []):
            sub = subdomain.get("domain")
            if sub and sub.endswith(f".{domain}"):
                myssls.append(sub)
    except httpx.TimeoutException:
        if args.show_timeout_info:
            logger("Timeout reached for MySSL API", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in MySSL API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by MySSL API: {len(myssls)}", "info", args.no_color)
        return myssls