import asyncio
import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import singlekeyloader, UserAgents
sem = asyncio.Semaphore(50)
Trickest = set()


async def get_count(session, offset, domain, args):
    try:
        url = f"https://api.trickest.io/solutions/v1/public/solution/a7cba1f1-df07-4a5c-876a-953f178996be/view?q=hostname ~ '.{domain}'&dataset_id=a0a49ca9-03bb-45e0-aa9a-ad59082ebdfc&limit=50&offset={offset}&select=hostname&orderby=hostname"
        response = await session.get(url, timeout=args.timeout)
        if response.status_code == 200:
            data = response.json()
            return data.get("total_count", 0)
    except httpx.TimeoutException:
        if args.show_timeout_info:
            logger("Timeout reached for Trickest API while fetching count.", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in Trickest get_count: {e}, {type(e)}", "warn", args.no_color)

async def fetcher(session, offset, domain, args):
    try:
        async with sem:
            url = f"https://api.trickest.io/solutions/v1/public/solution/a7cba1f1-df07-4a5c-876a-953f178996be/view?q=hostname ~ '.{domain}'&dataset_id=a0a49ca9-03bb-45e0-aa9a-ad59082ebdfc&limit=50&offset={offset}&select=hostname&orderby=hostname"
            response = await session.get(url, timeout=httpx.Timeout(read=300.0, connect=args.timeout))
            if response.status_code == 200:
                data = response.json()
                for result in data.get("results", []):
                    subdomain = result["hostname"]
                    if subdomain.endswith(f".{domain}"):
                        Trickest.add(subdomain)
    except httpx.TimeoutException:
        if args.show_timeout_info:
            logger("Timeout reached for Trickest API while fetching data.", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in Trickest fetcher: {e}, {type(e)}", "warn", args.no_color)

async def trickest(domain: str, configs: str,args):
    try:
        if not (args.all or (args.include_resources and "trickest" in args.include_resources)):
            return Trickest

        randomapikey = await singlekeyloader(configs, "trickest")
        if not randomapikey:
            return Trickest

        headers = {
            "User-Agent": UserAgents(),
            "Authorization": f"Token {randomapikey}"
        }
        tasks = []
        async with httpx.AsyncClient(verify=False, proxy=args.proxy, headers=headers) as session:
            total = await get_count(session, 10, domain, args)
            if not total or total == 0:
                return Trickest
            offset = 10
            for _ in range(0, int(total / 10) + 1):
                tasks.append(fetcher(session, offset, domain, args))
                offset += 10
            await asyncio.gather(*tasks, return_exceptions=False)
    except httpx.TimeoutException:
        if args.show_timeout_info:
            logger("Timeout reached while connecting to Trickest API.", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in Trickest main function: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total subdomains found by Trickest: {len(Trickest)}", "info", args.no_color)
        return Trickest