import asyncio
import warnings
from urllib.parse import urljoin
from bs4 import XMLParsedAsHTMLWarning
from playwright.async_api import async_playwright
from subdominator.modules.logger.logger import logger

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

async def check_sourcemap_leakage(subdomain, timeout=15):
    """
    Uses Playwright to load a site and listen for all JS requests.
    Checks for .map files for every JS resource discovered.
    """
    found_maps = []
    url = f"http://{subdomain}"
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(ignore_https_errors=True)
            page = await context.new_page()

            js_urls = set()

            page.on("request", lambda request: js_urls.add(request.url) 
                    if request.resource_type == "script" else None)

            try:
                await page.goto(url, timeout=timeout * 1000, wait_until="networkidle")
            except Exception:
                await page.goto(f"https://{subdomain}", timeout=timeout * 1000, wait_until="networkidle")

            await browser.close()

            import httpx
            async with httpx.AsyncClient(verify=False, timeout=5.0) as client:
                for js_url in js_urls:
                    map_url = f"{js_url}.map"
                    try:
                        res = await client.get(map_url)
                        if res.status_code == 200 and "application/json" in res.headers.get("Content-Type", ""):
                            found_maps.append(map_url)
                    except Exception:
                        continue

            if len(found_maps) > 3:
                return {
                    "subdomain": subdomain,
                    "vulnerable": True,
                    "count": len(found_maps),
                    "files": found_maps
                }
    except Exception:
        pass
        
    return None
