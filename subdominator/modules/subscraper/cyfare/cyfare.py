import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents

cyfares = []

async def cyfare(domain: str, session: httpx.AsyncClient, args):
    try:
        if args.include_resources and "cyfare" not in args.include_resources and not args.all:
            return cyfares
        
        if args.exclude_resources and "cyfare" in args.exclude_resources:
            return cyfares

        url = "https://cyfare.net/apps/VulnerabilityStudio/subfind/query.php"
        headers = {
            "User-Agent": UserAgents(),  
            "Origin": "https://cyfare.net",
            "Content-Type": "application/json"
        }
        json_body = {"domain": domain}

        response: httpx.Response = await session.request("POST", url, headers=headers, json=json_body, timeout=args.timeout)
        if response.status_code != 200:
            if args.verbose:
                logger(f"Cyfare API returned bad response status: {response.status_code}.", "warn", args.no_color)
            return cyfares

        data = response.json()
        subdomains = data.get("subdomains", [])
        cyfares.extend(subdomains)
    except httpx.TimeoutException:
        if args.show_timeout_info:
            logger(f"Timeout reached for Cyfare API due to: {e}", "warn", args.no_color)

    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in Cyfare API module: {e}, {type(e)}", "warn", args.no_color)

    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Cyfare API: {len(cyfares)}", "info", args.no_color)
        return cyfares
