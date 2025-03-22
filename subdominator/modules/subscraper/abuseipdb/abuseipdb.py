import re
from subdominator.modules.utils.utils import check_subdomain,UserAgents
import httpx
from subdominator.modules.logger.logger import logger
abuseipdbs = []

async def abuseipdb(domain: str, session: httpx.AsyncClient, args) -> list[str]:
    try:
        
        if args.include_resources and "abuseipdb" not in args.include_resources and not args.all:
            return abuseipdbs
        
        if args.exclude_resources and "abuseipdb" in args.exclude_resources:
            return abuseipdbs
        
        parsed_domain = check_subdomain(domain)
        if parsed_domain.subdomain:
            return abuseipdbs
        url = f"https://www.abuseipdb.com/whois/{domain}" 
        headers = {
                "User-Agent": UserAgents(),
                "Cookie": "abuseipdb_session="
            }
        response: httpx.Response  =  await session.request("GET", url, timeout=args.timeout, headers=headers)
        data = response.text
        if response.status_code != 200:
            return abuseipdbs
        tags = re.findall(r'<li>\w.*</li>', data)
        subdomains = [re.sub("</?li>", "", tag) + f".{domain}" for tag in tags]
        abuseipdbs.extend(subdomains)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout exception occurred in the AbusiIpdb API due to: {e}", "warn", args.no_color)    
    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in AbuseIpdb module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Abuseipdb API: {len(abuseipdbs)}", "info")
        return abuseipdbs