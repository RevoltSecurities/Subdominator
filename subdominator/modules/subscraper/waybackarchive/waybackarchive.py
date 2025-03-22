import httpx
from subdominator.modules.utils.utils import extracts, UserAgents
from subdominator.modules.logger.logger import logger
Waybackurls = set()

async def waybackarchive(domain, args):
    try:
        if not (args.all or (args.include_resources and "waybackarchive" in args.include_resources)):
            return Waybackurls
        headers = {
           "User-Agent": UserAgents()
       }
        async with httpx.AsyncClient(verify=False, proxy=args.proxy) as request:
           async with request.stream(
               "GET", f"https://web.archive.org/cdx/search/cdx?url=*.{domain}&collapse=urlkey&fl=original", 
               headers=headers, 
               timeout=httpx.Timeout(read=300.0, connect=args.timeout, write=None, pool=None), 
               follow_redirects=True
               ) as response:
               async for url in response.aiter_lines():
                   subdomains = await extracts(url, domain)
                   if subdomains:
                       for subdomain in subdomains:
                           subdomain = subdomain.lstrip("25").lstrip("2F").lstrip("40").lstrip(".").lstrip("B0")
                           if subdomain not in Waybackurls and not subdomain.startswith("%3D") and not subdomain.startswith("3D"):
                               Waybackurls.add(subdomain)    
    except httpx.TimeoutException as e:
        if args.show_timeout_info:
            logger(f"Timeout reached for Webarchive due to: {e}", "warn", args.no_color)
    except Exception as e:
        if args.verbose:
            logger(f"Exception in Waybackarchive module due to: {e}, {type(e)}", "warn", args.no_color)
    finally:
        if args.verbose:
            logger(f"Total Subdomains found by Waybackarchive: {len(Waybackurls)}", "info", args.no_color)
        return Waybackurls