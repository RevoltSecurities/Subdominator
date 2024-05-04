from colorama import Fore, Style
import sys
def reader(filename, args):
    try:
        with open(filename, "r") as streamr:
            data = streamr.read().splitlines()
        return data
    except FileNotFoundError as e:
        if args.no_color:
            print(f"[WRN]:  {filename} could not found please check the file exists or not", file=sys.stderr)
        else:
            print(f"[{Style.BRIGHT}{Fore.RED}WRN{Style.RESET_ALL}]: {Style.BRIGHT}{Fore.WHITE}{filename} could not found please check the file exists or not{Style.RESET_ALL}", file=sys.stderr)
        quit()
    except Exception as e:
        print(f"Exception in file reader modules: {e}, {type(e)}", file=sys.stderr)