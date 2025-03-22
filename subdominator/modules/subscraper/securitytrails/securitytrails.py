import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, singlekeyloader
Securitytrails = []

async def securitytrailsapi(url: str, domain: str, session: httpx.AsyncClient, randkey: str, args):
    try:
        headers = {"User-Agent": UserAgents(), "accept": "application/json", "APIKEY": randkey}
        response: httpx.Response = await session.get(url, headers=headers, timeout=args.timeout)
        if response.status_code != 200:
            if args.show_key_info:
                logger(f"SecurityTrails blocking request, check API usage for key: {randkey}", "warn", args.no_color)
            return []
        data = response.json()
        return [f"{sub}.{domain}" for sub in data.get("subdomains", [])]
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for SecurityTrails API due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in SecurityTrails API request module due to: {e}, {type(e)}", "warn", args.no_color)
    return []

async def securitytrails(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "securitytrails" not in args.include_resources and not args.all:
            return Securitytrails

        if args.exclude_resources and "securitytrails" in args.exclude_resources:
            return Securitytrails

        randomkey = await singlekeyloader(configs, "securitytrails")
        if randomkey is None:
            return Securitytrails
        
        url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains?children_only=false&include_inactive=true"
        subdomains = await securitytrailsapi(url, domain, session, randomkey, args)
        Securitytrails.extend(subdomains)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in SecurityTrails API module: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by SecurityTrails API: {len(Securitytrails)}", "info", args.no_color)
        return Securitytrails