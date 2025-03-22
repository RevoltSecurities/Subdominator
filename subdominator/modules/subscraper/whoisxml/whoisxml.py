import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, singlekeyloader

whoisxml_results = []

async def whoisxml(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "whoisxml" not in args.include_resources and not args.all:
            return whoisxml_results
        
        if args.exclude_resources and "whoisxml" in args.exclude_resources:
            return whoisxml_results
        
        randomkey = await singlekeyloader(configs, "whoisxmlapi")
        
        if randomkey is None:
            return whoisxml_results
        url = f"https://subdomains.whoisxmlapi.com/api/v1?apiKey={randomkey}&domainName={domain}"
        headers = {'User-Agent': UserAgents()}
        response: httpx.Response = await session.request("GET", url, headers=headers, timeout=args.timeout)
        if response.status_code != 200:
            if args.show_key_info:
                logger(f"WhoisXML API blocking our request, {username} please check your API usage for this key: {randomkey}", "warn", args.no_color)
            return whoisxml_results
        data = response.json()
        subdomains = [record["domain"] for record in data.get("result", {}).get("records", []) if "domain" in record]
        whoisxml_results.extend(subdomains)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for WhoisXML API, due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in WhoisXML API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by WhoisXML API: {len(whoisxml_results)}", "info", args.no_color)
        return whoisxml_results