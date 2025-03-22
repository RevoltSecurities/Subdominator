#!/usr/bin/env python3
import argparse
from subdominator.modules.logger.logger import logger, bold,blue,reset
from subdominator.modules.utils.utils import Exit

def cli():
    try:
        parser = argparse.ArgumentParser(add_help=False, usage=argparse.SUPPRESS,exit_on_error=False)
        parser.add_argument("-d", "--domain", type=str)
        parser.add_argument("-dL", "--domain-list", type=str)
        parser.add_argument("-cp", "--config-path", type=str)
        parser.add_argument("-o", "--output", type=str)
        parser.add_argument("-oD", "--output-directory", type=str)
        parser.add_argument("-t", "--timeout", type=float, default=30)
        parser.add_argument("-up", "--update", action="store_true")
        parser.add_argument("-nt", "--notify", action="store_true")
        parser.add_argument("-px", "--proxy", type=str)
        parser.add_argument("-h", "--help", action="store_true")
        parser.add_argument("-v","--version", action="store_true")
        parser.add_argument("-ski", "--show-key-info", action="store_true")
        parser.add_argument("-sti", "--show-timeout-info", action="store_true")
        parser.add_argument("-nc", "--no-color", action="store_true")
        parser.add_argument("-ls", "--list-source", action="store_true")
        parser.add_argument("-duc", "--disable-update-check", action="store_true")
        parser.add_argument("-V", "--verbose", action="store_true")
        parser.add_argument("-sup", "--show-updates", action="store_true")     
        parser.add_argument("-fw", "--filter-wildcards", action="store_true")
        parser.add_argument("-json", "--json", action="store_true")
        parser.add_argument("-s", "--silent", action="store_true")
        parser.add_argument("-ir", "--include-resources", type=str,default=None)
        parser.add_argument("-er", "--exclude-resources", type=str, default=None)
        parser.add_argument("-all", "--all", action="store_true")
        parser.add_argument("-dork", "--dork", type=str,default=None)
        parser.add_argument("-cdp", "--config-db-path", type=str)
        parser.add_argument("-shell", "--shell", action="store_true")
        return parser.parse_args()
    except argparse.ArgumentError as e:
        logger(f"Please use the command for more infromation: {bold}{blue}subdominator -h{reset}", "warn")
        Exit(1)
    except argparse.ArgumentTypeError as e:
        logger(f"Please use the command for more infromation: {bold}{blue}subdominator -h{reset}" ,"warn")
        Exit(1)        
    except Exception as e:
        logger(f"Unahandled Exception occured in the CLI module due to: {e}", "warn")
        Exit(1)