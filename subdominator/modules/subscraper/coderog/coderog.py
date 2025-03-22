import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader
coderogs = []

async def coderog(domain: str, session: httpx.AsyncClient, configs: str, args):
    try:
        if args.include_resources and "coderog" not in args.include_resources and not args.all:
            return coderogs
        
        if args.exclude_resources and "coderog" in args.exclude_resources:
            return coderogs

        randomkey = await singlekeyloader(configs, "rapidapi")
        if not randomkey:
            return coderogs

        url = f"https://subdomain-finder5.p.rapidapi.com/subdomain-finder?domain={domain}"
        headers = {
            "x-rapidapi-key": randomkey,
            "x-rapidapi-host": "subdomain-finder5.p.rapidapi.com"
        }

        response: httpx.Response = await session.request("GET", url, headers=headers, timeout=args.timeout)
        if response.status_code == 403:
            if args.verbose:
                logger(f"CodeRog API blocked request. Ensure you are subscribed to the API service for key: {randomkey}", "warn", args.no_color)
            return coderogs

        if response.status_code != 200:
            if args.verbose:
                logger(f"CodeRog API returned response status: {response.status_code}. Check API usage for key: {randomkey}", "warn", args.no_color)
            return coderogs

        data = response.json()
        for subdomains in data.get("data", []):
            subdomain = subdomains["subdomain"]
            if subdomain.endswith(f".{domain}"):
                coderogs.append(subdomain)
    except httpx.TimeoutException:
        if args.show_timeout_info:
            logger("Timeout reached for CodeRog API due to server-side or client-side error.", "warn", args.no_color)

    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in CodeRog API module: {e}, {type(e)}", "warn", args.no_color)

    finally:
        if args.verbose:
            logger(f"Total Subdomains found by CodeRog API: {len(coderogs)}", "info", args.no_color)
        return coderogs
