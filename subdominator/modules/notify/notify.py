import aiohttp
from subdominator.modules.logger.logger import logger, bold,red,white,reset
from subdominator.modules.utils.utils import singlekeyloader
            
async def slack(domain, subdomains, url, session, args):
    try:
        results = '\n'.join(subdomains)
        payloads = {"text": f"Total subdomains {len(subdomains)} found for {domain}:\n{results}"}
        async with session.post(url, json=payloads) as response:
            pass
    except aiohttp.ClientConnectionError as e:
        pass
    except TimeoutError as e:
        pass
    except Exception as e:
        if args.sec_deb:
            logger(f"Exception in slack notify pusher module due to : {e}, {type(e)}","warn",args.no_color)
            

async def pushbullet(domain, subdomains, randomkey, session, args):
    try:
        url = f'https://api.pushbullet.com/v2/pushes'  
        results = '\n'.join(subdomains)
        headers = {
            'Access-Token': randomkey,
            
            'Content-Type': 'application/json'
            }
        jdata = {
            'type': 'note',
            'title': f"Total subdomains {len(subdomains)} found for {domain}:",
            'body': f"{results}"
        }
        async with session.post(url, headers=headers, json=jdata) as response:
            pass
        
    except aiohttp.ClientConnectionError as e:
        pass
    except TimeoutError as e:
        pass
    except Exception as e:
        if args.sec_deb:
            logger(f"Exception in pushbullet module due to : {e}, {type(e)}","warn",args.no_color)
            
async def notify(domain, subdomains, configpath, username, args):
    try:
        url = await singlekeyloader(configpath,"slack")
        randomkey = await singlekeyloader(configpath,"pushbullet")
        async with aiohttp.ClientSession() as session:
            if url:
                await slack(domain, subdomains, url,session, args)
            if randomkey:
                await pushbullet(domain, subdomains, randomkey, session, args)
    except Exception as e:
        if args.sec_deb:
            logger(f"[{bold}{red}WRN{reset}]: {bold}{white}exception in notify: {e}, {type(e)}","warn",args.no_color)