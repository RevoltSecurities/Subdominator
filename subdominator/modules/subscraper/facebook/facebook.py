import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import dualkeyloader
fbcerts = []

async def facebook(domain: str, session: httpx.AsyncClient, configs: str, username: str, args) -> list[str]:
    try:
        if args.include_resources and "facebook" not in args.include_resources and not args.all:
            return fbcerts
        
        if args.exclude_resources and "facebook" in args.exclude_resources:
            return fbcerts
        
        randomid , randomsecret = await dualkeyloader(configs,"facebook",False)
        if randomid is None or randomsecret is None:
            return fbcerts
        randomtoken = f"{randomid}|{randomsecret}"
        url = f"https://graph.facebook.com/v18.0/certificates?fields=domains&access_token={randomtoken}&query={domain}&limit=1000"
        while True:
            response: httpx.Response = await session.request("GET",url, timeout=args.timeout)
            if response.status_code != 200:
                return fbcerts
            data = response.json()
            for item in data['data']:
                subdomains = item['domains']
                for subdomain in subdomains:
                    if subdomain.endswith(f"{domain}"):
                        fbcerts.append(subdomain)
            pages = data.get("paging", {})
            next_page = pages.get('next')
            if next_page:
                url = next_page
            if not next_page:
                break
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Facebook API due to: {e}", "warn", args.no_color)   
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in the Facebook API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Facebook API: {len(fbcerts)}")
        return fbcerts