import httpx
from subdominator.modules.logger.logger import logger
hackertargets = []


async def hackertarget(domain: str, session: httpx.AsyncClient, args) -> list[str]:
    try:
        if args.include_resources and "hackertarget" not in args.include_resources and not args.all:
            return hackertargets

        if args.exclude_resources and "hackertarget" in args.exclude_resources:
            return hackertargets

        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        response: httpx.Response = await session.request("GET", url, timeout=args.timeout)
        if response.status_code != 200:
            return hackertargets
        data = response.text.splitlines()
        for subdomain in data:
            if "API count exceeded - Increase Quota with Membership" in subdomain:
                continue
            subdomain = subdomain.split(",")[0]
            hackertargets.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Hackertarget API, due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in Hackertarget API module: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total subdomains found by Hackertarget API: {len(hackertargets)}", "info", args.no_color)
        return hackertargets