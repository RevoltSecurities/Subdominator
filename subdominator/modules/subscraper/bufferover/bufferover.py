import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import UserAgents,singlekeyloader
bufferovers = []

async def bufferover(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    try: 
        if args.include_resources and "bufferover" not in args.include_resources and not args.all:
            return bufferovers
        
        if args.exclude_resources and "bufferover" in args.exclude_resources:
            return bufferovers
        
        randomkey = await singlekeyloader(configs, "bufferover")
        if randomkey is None:
            return bufferovers
        url = f"https://tls.bufferover.run/dns?q=.{domain}"
        auth = {
            'User-Agent': UserAgents(),
            'x-api-key': randomkey
        }
        response: httpx.Response = await session.request("GET",url, headers=auth, timeout=args.timeout)
        if response.status_code != 200:
            if args.show_key_info:
                logger(f"Bufferover blocking our request, {username} please check your api usage for this key: {randomkey}", "warn", args.no_color)
            return bufferovers
        
        data = response.json()
        if 'Results' in data:
            results = data['Results']
            for result in results:
                elements = result.split(',')
                subdomain = elements[4].strip()
                bufferovers.append(subdomain)
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Bufferover API due to: {e}, {type(e)}", "warn", args.no_color)               
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in Bufferover API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Bufferover API: {len(bufferovers)}", "info", args.no_color)
        return bufferovers