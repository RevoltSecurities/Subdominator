import os

def file(subdomain,  domain, args):
    try:
        if args.output:
            if os.path.isfile(args.output):
                filename = args.output
            elif os.path.isdir(args.output):
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
        