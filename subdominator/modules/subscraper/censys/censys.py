import httpx
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import dualkeyloader
censyss = []

async def censys(domain: str, session: httpx.AsyncClient, configs: str, username: str, args):
    
    try:
        if args.include_resources and "censys" not in args.include_resources and not args.all:
            return censyss
        
        if args.exclude_resources and "censys" in args.exclude_resources:
            return censyss
        
        randomtoken,randomsecret = await dualkeyloader(configs, "censys", False)
        
        if randomtoken is None or randomsecret is None:
            return censyss
        
        url = "https://search.censys.io/api/v2/certificates/search"
        maxpage = 10
        maxdata = 100
        cursor = None
        params = {'q': domain, 'per_page': maxdata}
            
        for _ in range(maxpage+1):
            if cursor:
                params['cursor'] = cursor
            response: httpx.Response = await session.request("GET",url, auth=httpx.BasicAuth(randomtoken, randomsecret), params=params, timeout=args.timeout) 
            if response.status_code != 200:
                if args.show_key_info:
                    logger(f"Censys blocking our request, {username} please check your api usage for this keys: {randomsecret}, {randomtoken}", "warn", args.no_color)
                return censyss
            
            data = response.json()
            if 'result' in data and 'hits' in data['result']:
                for hit in data['result']['hits']:
                    for name in hit.get('names', []):
                        censyss.append(name)
                cursor = data['result']['links'].get('next')
                if not cursor:
                    break    
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Censys API due to: {e}", "warn", args.no_color)    
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in Censys API module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains Found by Censys API: {len(censyss)}", "info", args.no_color)