import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, dualkeyloader
dnsrepo_results = []

async def dnsrepo(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "dnsrepo" not in args.include_resources and not args.all:
            return dnsrepo_results
        
        if args.exclude_resources and "dnsrepo" in args.exclude_resources:
            return dnsrepo_results
        
        token, randomkey = await dualkeyloader(configs, "dnsrepo", False)
        
        if token is None or randomkey is None:
            return dnsrepo_results

        url = f"https://dnsarchive.net/api/?apikey={randomkey}&search={domain}"
        headers = {
            'User-Agent': UserAgents(),
            'X-API-Access': token
        }
        response: httpx.Response = await session.request("GET", url, headers=headers, timeout=args.timeout)
        
        if response.status_code != 200:
            if args.show_key_info:
                logger(f"DNSRepo API blocking our request, {username}, please check your API usage for this key: {randomkey}", "warn", args.no_color)
            return []

        data = response.json()
        if not isinstance(data, list):
            return dnsrepo_results
        subdomains = [
            entry["domain"].rstrip(".") for entry in data
            if "domain" in entry and entry["domain"].rstrip(".").endswith(f".{domain}")
        ]
        dnsrepo_results.extend(subdomains)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for DNSRepo API, due to: {e}", "warn", args.no_color)    
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in DNSRepo API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by DNSRepo API: {len(dnsrepo_results)}", "info", args.no_color)
        return dnsrepo_results