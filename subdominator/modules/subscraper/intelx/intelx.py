import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import dualkeyloader, UserAgents
intelxs = []

async def getID(domain: str, session: httpx.AsyncClient, host: str, key: str, args):
    try:
        baseurl = f"https://{host}/phonebook/search?k={key}"
        auth = {"User-Agent": UserAgents()}
        reqbody = {
            "Maxresults": 100000,
            "Media": 0,
            "Target": 1,
            "Term": domain,
            "Terminate": None,
            "Timeout": 20,
        }
        response: httpx.Response = await session.post(baseurl, headers=auth, timeout=10, json=reqbody)
        if response.status_code != 200:
            return None
        data = response.json()
        return data.get("id")
    except Exception as e:
        if args.sec_deb:
            logger(f"Exception in IntelX getID block: {e}, {type(e)}", "warn", args.no_color)
        return None

async def intelx(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try:
        if args.include_resources and "intelx" not in args.include_resources and not args.all:
            return intelxs

        if args.exclude_resources and "intelx" in args.exclude_resources:
            return intelxs

        randhost, randkey = await dualkeyloader(configs, "intelx", False)

        if not randhost or not randkey:
            return intelxs

        id = await getID(domain, session, randhost, randkey, args)
        if not id:
            return intelxs

        while True:
            baseurl = f"https://{randhost}/phonebook/search/result?k={randkey}&id={id}&limit=10000"
            headers = {"User-Agent": UserAgents()}
            response: httpx.Response = await session.get(baseurl, headers=headers, timeout=args.timeout)
            if response.status_code != 200:
                return intelxs
            data = response.json()
            for item in data.get("selectors", []):
                subdomain = item.get("selectorvalue")
                if subdomain:
                    intelxs.append(subdomain)
            if data.get("status") not in [0, 3]:
                break
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for IntelX API: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in IntelX API module: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total subdomains found by IntelX API: {len(intelxs)}", "info", args.no_color)
        return intelxs