import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader
chaoss = []

async def chaos(domain: str, session: httpx.AsyncClient, configs: str, args):
    try:
        if args.include_resources and "chaos" not in args.include_resources and not args.all:
            return chaoss
        
        if args.exclude_resources and "chaos" in args.exclude_resources:
            return chaoss

        randomkey = await singlekeyloader(configs, "chaos")
        if not randomkey:
            return chaoss

        url = f"https://dns.projectdiscovery.io/dns/{domain}/subdomains"
        headers = {"Authorization": randomkey}

        response: httpx.Response = await session.request("GET", url, headers=headers, timeout=args.timeout)
        if response.status_code != 200:
            if args.verbose:
                logger(f"Chaos API returned response status: {response.status_code}", "warn", args.no_color)
            return chaoss
        
        data = response.json()
        if "subdomains" in data:
            for subdomain in data["subdomains"]:
                if subdomain == "":
                    continue
                if not subdomain.endswith(f".{domain}"):
                    chaoss.append(f"{subdomain}.{domain}")
                else:
                    chaoss.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Chaos API due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in Chaos API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Chaos API: {len(chaoss)}", "info", args.no_color)
        return chaoss