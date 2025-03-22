import httpx
import base64
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader
FOFA = []


async def fofa(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "fofa" not in args.include_resources and not args.all:
            return FOFA
        
        if args.exclude_resources and "fofa" in args.exclude_resources:
            return FOFA
        
        randomkey = await singlekeyloader(configs, "fofa")
        if randomkey is None:
            return FOFA
        pagenum = 1
        domain_encoded = f"""domain="{domain}" """.encode('utf-8')
        subdomains = base64.b64encode(domain_encoded).decode('utf-8')
        while True:
            url = f"https://fofa.info/api/v1/search/all?key={randomkey}&qbase64={subdomains}&page={pagenum}&full=true&size=1000"
            response: httpx.Response = await session.request("GET", url, timeout=args.timeout)
            if response.status_code != 200:
                return FOFA
            data = response.json()
            if "results" not in data:
                return FOFA
            for result in data.get('results', []):
                url = result[0]
                if url.startswith("https://"):
                    url = url.replace("https://", "")
                elif url.startswith("http://"):
                    url = url.replace("http://", "")
                subdomain = url.split(':')[0] if ':' in url else url
                FOFA.append(subdomain)
            size = data.get('size')
            if size < 1000:
                return FOFA
            pagenum += 1
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for FOFA API due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in the FOFA API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by FOFA API: {len(FOFA)}", "info", args.no_color)
        return FOFA
