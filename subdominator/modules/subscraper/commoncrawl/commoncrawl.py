import asyncio
import httpx
from datetime import datetime
from colorama import Fore, Style
from subdominator.modules.utils.utils import extracts, UserAgents, Exit
from subdominator.modules.logger.logger import logger

Commoncrawls = set()

async def indexDB(args):
    try:
        headers = {
                "User-Agent": UserAgents()
        }
        async with httpx.AsyncClient(headers=headers, timeout=args.timeout, verify=False,proxy=args.proxy) as session:
            response = await session.request("GET", "https://index.commoncrawl.org/collinfo.json", follow_redirects=True)
            return response.json()
    except httpx.RemoteProtocolError:
        pass
    except httpx.ReadTimeout:
        pass
    except httpx.TimeoutException as e:
        logger(f"Timeout Reached for Commoncrawl API IndexDB due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in the Commoncrawl API IndexDB module due to: {e}", "warn", args.no_color)
            
async def CcClient(args,searchurl: str,domain):
    try:
        headers = {
            "User-Agent": UserAgents()
        }
        async with httpx.AsyncClient(timeout=httpx.Timeout(read=300.0, connect=args.timeout, write=None, pool=None), headers=headers, verify=False, proxy=args.proxy) as request:
            async with  request.stream("GET", f"{searchurl}?url=*.{domain}", follow_redirects=True) as response:
                async for url in response.aiter_lines():
                    subdomains = await extracts(url, domain)
                    if subdomains:
                        for subdomain in subdomains:
                            subdomain = subdomain.lstrip("25").lstrip("2F").lstrip("40").lstrip(".")
                            if subdomain not in Commoncrawls and not subdomain.startswith("%3D") and not subdomain.startswith("3D"):
                                Commoncrawls.add(subdomain)
    except httpx.RemoteProtocolError:
            pass
    except httpx.ReadTimeout:
            pass
    except httpx.TimeoutException as e:
        logger(f"Timeout Reached for Commoncrawl API Client due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred in the Commoncrawl API Client module due to: {e}", "warn", args.no_color)

async def commoncrawl(Domain, args):
    try:
        
        if not (args.all or (args.include_resources and "commoncrawl" in args.include_resources)):
            return Commoncrawls
        
        indexurls = []
        added = set()
        responsed = await indexDB(args)
        if responsed is None:
            return Commoncrawls
        ctyear = datetime.now().year
        years = [str(ctyear - i) for i in range(6)]
        for year in years:
            for index in responsed:
                if year not in added:
                    if year in index.get("name"):
                        indexurls.append(index.get('cdx-api'))
                        added.add(year)
        for url in indexurls:
            await CcClient(args, url, Domain)
    except Exception as e:
        if args.verbose:
            logger(f"Exception occurred at the Commoncrawl API core module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Commoncrawl API: {len(Commoncrawls)}")
        return Commoncrawls