import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, singlekeyloader
virustotal_results = []

async def virustotal(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "virustotal" not in args.include_resources and not args.all:
            return virustotal_results
        
        if args.exclude_resources and "virustotal" in args.exclude_resources:
            return virustotal_results
        
        randomkey = await singlekeyloader(configs, "virustotal")
        
        if randomkey is None:
            return virustotal_results
        
        cursor = None
        while True:
            url = f"https://www.virustotal.com/api/v3/domains/{domain}/subdomains?limit=40"
            if cursor:
                url = f"{url}&cursor={cursor}"
            
            headers = {
                'User-Agent': UserAgents(),
                'x-apikey': randomkey
            }
            response: httpx.Response = await session.request("GET", url, headers=headers, timeout=args.timeout)
            if response.status_code != 200:
                if args.show_key_info:
                    logger(f"VirusTotal blocking our request, {username} please check your API usage for this key: {randomkey}", "warn", args.no_color)
                return virustotal_results
            
            data = response.json()
            subdomains = [item["id"] for item in data.get("data", [])]
            virustotal_results.extend(subdomains)
            cursor = data.get("meta", {}).get("cursor", "")
            if not cursor:
                break
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for VirusTotal API, due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in VirusTotal API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by VirusTotal API: {len(virustotal_results)}", "info", args.no_color)
        return virustotal_results
