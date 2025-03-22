import httpx
import base64
from datetime import datetime, timedelta
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader
import time
hunterhows = []

async def huntermap(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "huntermap" not in args.include_resources and not args.all:
            return hunterhows

        if args.exclude_resources and "huntermap" in args.exclude_resources:
            return hunterhows

        endtime = datetime.now().strftime("%Y-%m-%d")
        yeartime = datetime.now() - timedelta(days=27.8 * 12)
        inititatetime = yeartime.strftime("%Y-%m-%d")
        query = base64.urlsafe_b64encode(domain.encode("utf-8")).decode("ascii")
        page_size = 100
        page = 1
        
        while True:
            randomapikey = await singlekeyloader(configs, "huntermap")
            if not randomapikey:
                return hunterhows
            time.sleep(2.5)
            url = f"https://api.hunter.how/search?api-key={randomapikey}&query={query}&start_time={inititatetime}&end_time={endtime}&page={page}&page_size={page_size}"
            response: httpx.Response = await session.request("GET", url, timeout=args.timeout)
            if response.status_code != 200:
                if args.show_key_info:
                    logger(f"Huntermap blocking our request, {username}, check your API usage for this key: {randomapikey}", "warn", args.no_color)
                return hunterhows
            data = response.json()
            subdomains = data.get("data", {}).get("list", [])
            total = data.get("data", {}).get("total", 0)

            for subdomain in subdomains:
                subdomain = subdomain["domain"]
                if subdomain.endswith(f".{domain}"):
                    hunterhows.append(subdomain)
            if total <= len(hunterhows):
                break
            page += 1
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Huntermap API: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in Huntermap API module: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total subdomains found by Huntermap API: {len(hunterhows)}", "info", args.no_color)
        return hunterhows