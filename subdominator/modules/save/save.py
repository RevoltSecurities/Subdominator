import os
import json
import aiofiles
import asyncio
import sys
from subdominator.modules.utils import red, blue, white, bold, reset

def file(subdomain,  domain, args):
    try:
        if args.output:
            if os.path.isdir(args.output):
                filename = os.path.join(args.output, f"{domain}.subdomains.txt")
            else:
                filename = args.output
        if not args.output:
            filename = f"{domain}.txt"
        with open(filename, "a") as w:
            w.write(subdomain + '\n')
    except KeyboardInterrupt as e:        
        SystemExit

    except Exception as e:
        pass
        

def dir(subdomain,  domain, args):
    try:
        
        if os.path.isdir(args.output_directory):
            if os.path.exists(args.output_directory):
                filename = f"{args.output_directory}/{domain}.txt"
            else:
                os.makedirs(args.output_directory)
                filename = f"{args.output_directory}/{domain}.txt"
        else:
            currentdir = os.getcwd()
            filename = f"{currentdir}/{domain}.txt"
            
        with open(filename, "a") as w:
            w.write(subdomain + '\n')
    except KeyboardInterrupt as e:        
        SystemExit
    except Exception as e:
        pass

async def jsonsave(domain, subdomains, filename, args):
    try:
        if args.output_json:
            if os.path.isdir(args.output_json):
                filename = os.path.join(args.output_json, f"{domain}.subdomains.json")
            else:
                filename = args.output_json
        results = []
        for subdomain, sources in subdomains.items():
            results.append({
                "subdomain": subdomain,
                "domain": domain,
                "sources": list(sorted(sources))
            })
        async with aiofiles.open(filename, "a") as streamw:
            for output in results:
                await streamw.write(json.dumps(output)+"\n")
    except Exception as e:
        print(f"[{bold}{red}WRN{reset}]: {bold}{white}Excepiton occured in json output writer due to: {e}, {type(e)}{reset}")
        