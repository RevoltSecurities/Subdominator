import os
import json
import aiofiles
from subdominator.modules.logger.logger import logger

def file(subdomain,  domain, args):
    try:
        if args.output:
            if os.path.isdir(args.output):
                filename = os.path.join(args.output, f"{domain}.subdomains.txt")
            else:
                filename = args.output
                
        with open(filename, "a") as w:
            w.write(subdomain + '\n')
    except KeyboardInterrupt as e:        
        SystemExit

    except Exception as e:
        pass
        

def dir(subdomain,  domain, args):
    try:
        if args.json:
            ext = "json"
        else:
            ext = "txt"
            
        if os.path.isdir(args.output_directory):
            if os.path.exists(args.output_directory):
                filename = f"{args.output_directory}/{domain}.{ext}"
            else:
                os.makedirs(args.output_directory)
                filename = f"{args.output_directory}/{domain}.{ext}"
        else:
            currentdir = os.getcwd()
            filename = f"{currentdir}/{domain}.{ext}"
            
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
        for subdomain in subdomains:
            results.append({
                        "subdomain": subdomain,
                        "domain": domain
                    })
        async with aiofiles.open(filename, "a") as streamw:
            for output in results:
                await streamw.write(json.dumps(output)+"\n")
    except Exception as e:
        print(f"Excepiton occured in json output writer due to: {e}", "warn", args.no_color)