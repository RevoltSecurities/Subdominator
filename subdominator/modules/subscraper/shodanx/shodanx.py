import httpx
import warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning, MarkupResemblesLocatorWarning
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents, check_subdomain
Shodanxs = []

async def shodanx(domain: str, session: httpx.AsyncClient, args):
    try:
        if args.include_resources and "shodanx" not in args.include_resources and not args.all:
            return Shodanxs

        if args.exclude_resources and "shodanx" in args.exclude_resources:
            return Shodanxs
        
        parsed_domain = check_subdomain(domain)
        if parsed_domain.subdomain:
            return Shodanxs

        url = f"https://www.shodan.io/domain/{domain}"
        headers = {"User-Agent": UserAgents()}

        response = await session.get(url,headers=headers,timeout=args.timeout)
        if response.status_code != 200:
            return Shodanxs
        data = response.text
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
            warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

            soup = BeautifulSoup(data, "lxml")
            ul = soup.find("ul", id="subdomains")
            if not ul:
                return Shodanxs
            subdomains = ul.find_all("li")
            for result in subdomains:
                subdomain = f"{result.text.strip()}.{domain}"
                Shodanxs.append(subdomain)
    except httpx.TimeoutException:
        if args.show_timeout_info:
            logger("Timeout reached for ShodanX", "warn", args.no_color)
    except httpx.RequestError as e:
        if args.show_timeout_info:
            logger(f"Request error in ShodanX: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in ShodanX request block: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by ShodanX: {len(Shodanxs)}", "info", args.no_color)
        return Shodanxs
