import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader
rapids = []

async def rapidapi(domain: str, session: httpx.AsyncClient, configs: str, args):
    try:
        if args.include_resources and "rapidapi" not in args.include_resources and not args.all:
            return rapids
        if args.exclude_resources and "rapidapi" in args.exclude_resources:
            return rapids

        rapidapi_key = await singlekeyloader(configs,"rapidapi")
        whoisxml_key = await singlekeyloader(configs,"whoisxmlapi")

        if not rapidapi_key or not whoisxml_key:
            return rapids

        url = "https://subdomains-lookup.p.rapidapi.com/api/v1"
        params = {"domainName": domain, "apiKey": whoisxml_key, "outputFormat": "JSON"}
        headers = {
            "X-RapidAPI-Key": rapidapi_key,
            "X-RapidAPI-Host": "subdomains-lookup.p.rapidapi.com"
        }

        response: httpx.Response = await session.request("GET",url,params=params,headers=headers,timeout=args.timeout)
        
        if response.status_code != 200:
            if args.show_key_info:
                logger(f"RapidAPI blocking request, check API usage for these keys: {whoisxml_key}, {rapidapi_key}", "warn", args.no_color)
            return rapids

        data = response.json()
        subdomains = data.get("result", {}).get("records", [])

        for sub in subdomains:
            subdomain = sub.get("domain")
            if subdomain:
                rapids.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for RapidAPI due to: {e}", "info", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in Rapid API module due to: {e}, type: {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Rapid API: {len(rapids)}", "info", args.no_color)
        return rapids