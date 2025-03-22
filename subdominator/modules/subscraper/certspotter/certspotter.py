import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader
certspotters = []

async def certspotter(domain: str, session: httpx.AsyncClient, configs: str, args):
    try:
        if not (args.all or (args.include_resources and "certspotter" in args.include_resources)):
            return certspotters

        randomkey = await singlekeyloader(configs, "certspotter")
        if not randomkey:
            return certspotters

        headers = {"Authorization": f"Bearer {randomkey}"}
        base_url = f"https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names"

        while base_url:
            response : httpx.Response = await session.request("GET",base_url, headers=headers, timeout=args.timeout)
            if response.status_code != 200:
                if args.verbose:
                    logger(f"CertSpotter API returned base response status : {response.status_code}", "warn", args.no_color)
                return certspotters

            data = response.json()
            if not isinstance(data, list) or not data:
                return certspotters

            for entry in data:
                certspotters.extend(entry.get("dns_names", []))

            last_id = data[-1].get("id")
            if last_id:
                base_url = f"https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names&after={last_id}"
            else:
                base_url = None

    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for CertSpotter API due to: {e}", "warn", args.no_color)

    except Exception as e:
        if args.verbose:
            logger(f"Exception error occurred in CertSpotter API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by CertSpotter API: {len(certspotters)}", "info", args.no_color)
        return certspotters
