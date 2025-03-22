import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents
from urllib.parse import urlparse
hudsonrocks = []

async def hudsonrock(domain: str, session: httpx.AsyncClient, args):
    try:
        if args.include_resources and "hudsonrock" not in args.include_resources and not args.all:
            return hudsonrocks

        if args.exclude_resources and "hudsonrock" in args.exclude_resources:
            return hudsonrocks

        headers = {"User-Agent": UserAgents()}
        url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/urls-by-domain?domain={domain}"
        response: httpx.Response = await session.get(url, timeout=args.timeout, headers=headers)

        if response.status_code != 200:
            return hudsonrocks
        data = response.json()
        if "data" in data:
            employees_urls = data["data"].get("employees_urls", [])
            clients_urls = data["data"].get("clients_urls", [])

            for record in employees_urls + clients_urls:
                parsed_url = urlparse(record.get("url", ""))
                subdomain = parsed_url.netloc

                if subdomain.endswith(f".{domain}") and "•" not in subdomain and subdomain not in hudsonrocks:
                    hudsonrocks.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for HudsonRock API, due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in HudsonRock API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by HudsonRock API: {len(hudsonrocks)}", "info", args.no_color)
        return hudsonrocks