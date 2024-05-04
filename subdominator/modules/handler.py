import os
import sys
import random
from colorama import Fore, Style
import time
import asyncio
from rich.console import Console
from rich.markdown import Markdown
import aiohttp

red =  Fore.RED
green = Fore.GREEN
magenta = Fore.MAGENTA
cyan = Fore.CYAN
mixed = Fore.RED + Fore.BLUE
blue = Fore.BLUE
yellow = Fore.YELLOW
white = Fore.WHITE
reset = Style.RESET_ALL
bold = Style.BRIGHT
colors = [ green, cyan, blue]
random_color = random.choice(colors)

try:
    from .banner.banner import banner
    from .cli.cli import cli
    from .config.config import config, custompath, cachedir
    from .help.help import help
    from .source.source import sources
    from .update.update import *
    from .verify.verify import getverify
    from .version.version import version
    from .enumerates.abuseipdb.abuseipdb import abuseipdb
    from .enumerates.alienvault.alienvault import alienvault
    from .enumerates.anubis.anubis import anubis
    from .enumerates.bevigil.bevigil import bevigil
    from .enumerates.binaryedge.binaryedge import binaryedge
    from .enumerates.bufferover.bufferover import bufferover
    from .enumerates.censys.censys import censys
    from .enumerates.certspotter.certspotter import certspotter
    from .enumerates.chaos.chaos import chaos
    from .enumerates.columbusapi.columbusapi import columbusapi
    from .enumerates.crtsh.crtsh import crtsh
    from .enumerates.digitorus.digitorus import digitorus
    from .enumerates.dnsdumpster.dnsdumpster import dnsdumpster
    from .enumerates.dnsrepo.dnsrepo import dnsrepo
    from .enumerates.facebook.facebook import facebook
    from .enumerates.fullhunt.fullhunt import fullhunt
    from .enumerates.google.google import google
    from .enumerates.hackertarget.hackertarget import hackertarget
    from .enumerates.huntermap.huntermap import huntermap
    from .enumerates.intelx.intelx import intelx
    from .enumerates.leakix.leakix import leakix
    from .enumerates.netlas.netlas import netlas
    from .enumerates.quake.quake import quake
    from .enumerates.rapidapi.rapidapi import rapidapi
    from .enumerates.rapidfinder.rapidfinder import rapidfinder
    from .enumerates.rapidscan.rapidscan import rapidscan
    from .enumerates.rapiddns.rapiddns import rapiddns
    from .enumerates.redhuntlabs.redhuntlabs import redhuntlabs
    from .enumerates.securitytrails.securitytrails import securitytrails
    from .enumerates.shodan.shodan import shodan
    from .enumerates.shodanx.shodanx import shodanx
    from .enumerates.shrewdeye.shrewdeye import shrewdeye
    from .enumerates.sitedossier.sitedossier import sitedossier
    from .enumerates.subdomaincenter.subdomaincenter import subdomaincenter
    from .enumerates.urlscan.urlscan import urlscan
    from .enumerates.virustotal.virustotal import virustotal
    from .enumerates.waybackarchive.waybackarchive import waybackarchive
    from .enumerates.whoisxml.whoisxml import whoisxml
    from .enumerates.zoomeyeapi.zoomeyeapi import zoomeyeapi
    from .username.username import get_username
    from .extract.extract import  filters
    from .save.save import file, dir
    from .file.file import reader
    from .notify.notify import notify
except ImportError as e:
    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Import Error occured in  Subdominator Module imports due to: {e}{reset}", file=sys.stderr)
    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}If you are encountering this issue more than a time please report the issues in Subdominator Github page.. {reset}", file=sys.stderr)
    exit()
    
args = cli()
start = time.time()
if not args.config_path:
    configpath = config()
else:
    
    configpath = custompath(args)
    if not configpath:
        quit()
    
banners = banner()
username = get_username()

async def __initiate__(domain):
    try:
        async with aiohttp.ClientSession() as session:
            tasks = [abuseipdb(domain, session, args),alienvault(domain, session, args), anubis(domain, session, args), bevigil(domain, session, configpath, username, args), binaryedge(domain, session, configpath, username, args),
                     bufferover(domain, session, configpath, username, args), censys(domain, session, configpath, username, args), certspotter(domain, session, configpath, username, args), chaos(domain, session, configpath, username, args),
                     columbusapi(domain, session, args), crtsh(domain, session, args), digitorus(domain, session, args), dnsdumpster(domain, session, configpath, username, args), dnsrepo(domain, session, args),
                     facebook(domain, session, configpath, username, args), fullhunt(domain, session, configpath, username, args), google(domain, session, configpath, username, args),hackertarget(domain, session, args), huntermap(domain, session, configpath, username, args), 
                     intelx(domain, session, configpath, username, args), leakix(domain, session, configpath, username, args), netlas(domain, session, configpath, username, args), quake(domain, session, configpath, username, args),
                     rapidapi(domain, session, configpath, username, args), rapiddns(domain, session, args), rapidfinder(domain, session, configpath, username, args), rapidscan(domain, session, configpath, username, args),redhuntlabs(domain, session, configpath, username, args), securitytrails(domain, session, configpath, username, args),
                     shodan(domain, session, configpath, username, args), shodanx(domain, session, args), shrewdeye(domain, session, args), sitedossier(domain, session, args), subdomaincenter(domain, session, args),
                     urlscan(domain, session, args), virustotal(domain, session, configpath, username, args), waybackarchive(domain, session, args), whoisxml(domain, session, configpath, username, args), zoomeyeapi(domain, session, configpath, username, args)]
            
            results = await asyncio.gather(*tasks)
            return results
        
    except KeyboardInterrupt as e:
        SystemExit
    
    except Exception as e:
        if args.sec_deb:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Exception handler sources: {e}, {type(e)}{reset}", file=sys.stderr)


def gitversion():
    try:
        latest = version()
        current = "v1.0.7"
        if latest == current:
            print(f"[{blue}{bold}Version{reset}]:{bold}{white}Subdominator current version {latest} ({green}latest{reset}{bold}{white}){reset}", file=sys.stderr)
        else:
        
            print(f"[{blue}{bold}Version{reset}]: {bold}{white}Subdominator current version {latest} ({red}outdated{reset}{bold}{white}){reset}", file=sys.stderr)
    except KeyboardInterrupt as e:
        SystemExit
    
    
def update_handler():
    try:
        if args.show_updates:
            updatelog()
            quit()
        
        current = "v1.0.7"
        pypiold = "1.0.7"
        git = version()
        
        if current == git:
            if args.no_color:
                print(f"[INFO]: Hey {username} subdominator is already in new version", file=sys.stderr)
            else:
                print(f"[{bold}{green}INFO{reset}]: {bold}{white}Hey {username} subdominator is already in new version{reset}", file=sys.stderr)
            quit()

        zipurl = getzip()
        if not zipurl:
            if args.no_color:
                print(f"[WRN]: Hey {username} failed to update subdominator please try manually from github", file=sys.stderr)
            else:
                print(f"[{bold}{green}INFO{reset}]: {bold}{white}Hey {username} failed to update subdominator please try manually from github{reset}", file=sys.stderr)
            quit()
        cache = cachedir()
        launch(zipurl, cache)
        pypiversion = getverify("subdominator")
        
        if pypiold == pypiversion:
            if args.no_color:
                print(f"[WRN]: Hey {username} failed to update subdominator please try manually from github", file=sys.stderr)
            else:
                print(f"[{bold}{green}INFO{reset}]: {bold}{white}Hey {username} failed to update subdominator please try manually from github{reset}", file=sys.stderr)
            quit()
        if args.no_color:
            print(f"[INFO]: Verified the latest version of subdominator from pypi and updated from {current} --> {git}", file=sys.stderr)
        else:
            print(f"[{bold}{green}INFO{reset}]: {bold}{white}Verified the latest version of subdominator from pypi and updated from {current} --> {git}{reset}", file=sys.stderr)
        updatelog()
        quit()
                
        
    except KeyboardInterrupt as e:
        quit()

def show_sources():
    try:
        resources = sources()
        if not args.no_color:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Current Available free passive resources: [{len(resources)}]{reset}", file=sys.stderr)
        else:
            print(f"[INFO]: Current Available free passive resources: [{len(resources)}]", file=sys.stderr)
        
        
        if not args.no_color:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Sources marked with an * needs API key(s) or token(s) configuration to works{reset}", file=sys.stderr)
        else:
            print(f"[INFO]: Sources marked with an * needs API key(s) or token(s) configuration to works", file=sys.stderr)
        
        if not args.no_color:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Hey {username} you can config your api keys or token here {configpath} to work{reset}", file=sys.stderr)
        else:
            print(f"[INFO]: Hey {username} you can config your api keys or token here {configpath} to work", file=sys.stderr)
        
        console = Console()
        for sourced in resources:
            console.print(Markdown(sourced))
        quit()    
    except KeyboardInterrupt as e:
        SystemExit
        
        
async def _domain_handler_(domain):
    try:
        results = await __initiate__(domain)
        filtered = filters(results)
        final= []

        for subdomain in filtered:
            if subdomain.endswith(f".{domain}"):
                print(subdomain)
                final.append(subdomain)
                if args.output:
                    file(subdomain, domain, args)
                elif args.output_directory:
                    dir(subdomain, domain, args)
        
        if args.notify:
            await notify(domain, final, configpath, username, args)
            
        end = time.time()
        total_time = end - start
        
        if args.no_color:
            print(f"[INFO]: Total {len(final)} subdomains found for {domain} in {total_time:.2f} seconds", file=sys.stderr)
        else:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Total {len(final)} subdomains found for {domain} in {total_time:.2f} seconds{reset}", file=sys.stderr)
        
        if args.no_color:
            print(f"[WISH]: Happy Hacking {username} ☠️ 🔥 🚀", file=sys.stderr)
        else:
            print(f"[{bold}{green}WISH{reset}]: {bold}{white}Happy Hacking {username} ☠️ 🔥 🚀{reset}", file=sys.stderr)

    except KeyboardInterrupt as e:
        SystemExit


async def handler():
    try:
        print(banners, file=sys.stderr)
        if args.help:
            help(configpath)
            quit()
    
        if args.list_source:
            if not args.disable_update_check:
                gitversion()
            show_sources()
        
        if args.update or args.show_updates:
            if not args.disable_update_check:
                gitversion()
                
            update_handler()

        if args.domain:
            if not args.disable_update_check:
                gitversion()
            if not args.no_color:
                print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Loading provider configuration file from {configpath}{reset}", file=sys.stderr)
            else:
                print(f"[INFO]: Loading provider configuration file from {configpath}", file=sys.stderr)
        
            if not args.no_color:
                print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Enumerating subdomain for {args.domain}{reset}", file=sys.stderr)
            else:
                print(f"[INFO]: Enumerating subdomain for {args.domain}", file=sys.stderr)
            await _domain_handler_(args.domain)
            quit()
    
        if args.domain_list:
        
            if not args.disable_update_check:
                gitversion()
        
            if not args.no_color:
                print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Loading provider configuration file from {configpath}{reset}", file=sys.stderr)
            else:
                print(f"[INFO]: Loading provider configuration file from {configpath}", file=sys.stderr)
        
            domains = reader(args.domain_list, args)
            for domain in domains:
                if not args.no_color:
                    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Enumerating subdomain for {domain}{reset}", file=sys.stderr)
                else:
                    print(f"[INFO]: Enumerating subdomain for {domain}", file=sys.stderr)
                await _domain_handler_(domain)
            
            quit()
            
        if sys.stdin.isatty():
            if not args.no_color:
                    print(f"[{bold}{red}WRN{reset}]: {bold}{white}subdominator exits due to no inputs provided, please use subdominator -h for more details", file=sys.stderr)
            else:
                    print(f"[WRN]: subdominator exits due to no inputs provided, please use subdominator -h for more details", file=sys.stderr)
            quit()     
           
    except KeyboardInterrupt as e:
        SystemExit
            

def main_handler():
    try:
        asyncio.run(handler())
    except KeyboardInterrupt as e:
        SystemExit