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
    from .enumerates.builtwith.builtwith import builtwith
    from .enumerates.c99.c99 import c99
    from .enumerates.censys.censys import censys
    from .enumerates.certspotter.certspotter import certspotter
    from .enumerates.chaos.chaos import chaos
    from .enumerates.coderog.coderog import coderog
    from .enumerates.columbusapi.columbusapi import columbusapi
    from .enumerates.commoncrawl.commoncrawl import commoncrawl
    from .enumerates.crtsh.crtsh import crtsh
    from .enumerates.cyfare.cyfare import cyfare
    from .enumerates.digitorus.digitorus import digitorus
    from .enumerates.dnsdumpster.dnsdumpster import dnsdumpster
    from .enumerates.dnsrepo.dnsrepo import dnsrepo
    from .enumerates.facebook.facebook import facebook
    from .enumerates.fullhunt.fullhunt import fullhunt
    from .enumerates.fofa.fofa import fofa
    from .enumerates.google.google import google
    from .enumerates.hackertarget.hackertarget import hackertarget
    from .enumerates.huntermap.huntermap import huntermap
    from .enumerates.intelx.intelx import intelx
    from .enumerates.leakix.leakix import leakix
    from .enumerates.merkelmap.merklemap import merklemap
    from .enumerates.myssl.myssl import myssl
    from .enumerates.netlas.netlas import netlas
    from .enumerates.passivetotal.passivetotal import passivetotal
    from .enumerates.quake.quake import quake
    from .enumerates.racent.racent import racent
    from .enumerates.rapidapi.rapidapi import rapidapi
    from .enumerates.rapidfinder.rapidfinder import rapidfinder
    from .enumerates.rapidscan.rapidscan import rapidscan
    from .enumerates.rapiddns.rapiddns import rapiddns
    from .enumerates.redhuntlabs.redhuntlabs import redhuntlabs
    from .enumerates.rsecloud.rsecloud import rsecloud
    from .enumerates.securitytrails.securitytrails import securitytrails
    from .enumerates.shodan.shodan import shodan
    from .enumerates.shodanx.shodanx import shodanx
    from .enumerates.shrewdeye.shrewdeye import shrewdeye
    from .enumerates.sitedossier.sitedossier import sitedossier
    from .enumerates.subdomaincenter.subdomaincenter import subdomaincenter
    from .enumerates.trickest.trickest import trickest
    from .enumerates.urlscan.urlscan import urlscan
    from .enumerates.virustotal.virustotal import virustotal
    from .enumerates.waybackarchive.waybackarchive import waybackarchive
    from .enumerates.whoisxml.whoisxml import whoisxml
    from .enumerates.zoomeyeapi.zoomeyeapi import zoomeyeapi
    from .username.username import get_username
    from .extract.extract import  filters
    from .save.save import file, dir, jsonsave
    from .file.file import reader
    from .notify.notify import notify
except ImportError as e:
    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Import Error occured in  Subdominator Module imports due to: {e}{reset}", file=sys.stderr)
    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}If you are encountering this issue more than a time please report the issues in Subdominator Github page.. {reset}", file=sys.stderr)
    exit()
    
args = cli()
if not args.config_path:
    configpath = config()
else:
    
    configpath = custompath(args)
    if not configpath:
        quit()
    
banners = banner()
username = get_username()

async def __initiate__(domain, provided_sources):
    valid_sources = [
        'abuseipdb', 'alienvault', 'anubis', 'bevigil', 'binaryedge', 'bufferover', 'builtwith', 'c99', 'censys', 
        'certspotter', 'chaos', 'coderog', 'columbusapi', 'commoncrawl', 'crtsh', 'cyfare', 'digitorus', 'fofa', 
        'dnsdumpster', 'dnsrepo', 'facebook', 'fullhunt', 'google', 'hackertarget', 'huntermap', 'intelx', 'leakix', 
        'merklemap', 'myssl', 'netlas', 'passivetotal', 'quake', 'rapidapi', 'rapiddns', 'rapidfinder', 'rapidscan', 
        'redhuntlabs', 'racent', 'rsecloud', 'securitytrails', 'shodan', 'shodanx', 'shrewdeye', 'sitedossier', 
        'subdomaincenter', 'trickest', 'urlscan', 'virustotal', 'waybackarchive', 'whoisxml', 'zoomeyeapi'
    ]
    
    # If provided_sources is not None, validate each source
    if provided_sources:
        invalid_sources = [source for source in provided_sources if source not in valid_sources]
        if invalid_sources:
            print(f"[{bold}{red}WRN{reset}]: {bold}{white}Error: The following sources are not valid: [{green}{', '.join(invalid_sources)}{bold}{white}]{reset}", file=sys.stderr)
            exit()
        
        # Filter the valid sources based on provided_sources
        valid_sources = [source for source in valid_sources if source in provided_sources]

    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            if 'abuseipdb' in valid_sources: tasks.append(abuseipdb(domain, session, args))
            if 'alienvault' in valid_sources: tasks.append(alienvault(domain, session, args))
            if 'anubis' in valid_sources: tasks.append(anubis(domain, session, args))
            if 'bevigil' in valid_sources: tasks.append(bevigil(domain, session, configpath, username, args))
            if 'binaryedge' in valid_sources: tasks.append(binaryedge(domain, session, configpath, username, args))
            if 'bufferover' in valid_sources: tasks.append(bufferover(domain, session, configpath, username, args))
            if 'builtwith' in valid_sources: tasks.append(builtwith(domain, session, configpath, username, args))
            if 'c99' in valid_sources: tasks.append(c99(domain, session, configpath, username, args))
            if 'censys' in valid_sources: tasks.append(censys(domain, session, configpath, username, args))
            if 'certspotter' in valid_sources: tasks.append(certspotter(domain, session, configpath, username, args))
            if 'chaos' in valid_sources: tasks.append(chaos(domain, session, configpath, username, args))
            if 'coderog' in valid_sources: tasks.append(coderog(domain, session, configpath, username, args))
            if 'columbusapi' in valid_sources: tasks.append(columbusapi(domain, session, args))
            if 'commoncrawl' in valid_sources: tasks.append(commoncrawl(domain, args))
            if 'crtsh' in valid_sources: tasks.append(crtsh(domain, session, args))
            if 'cyfare' in valid_sources: tasks.append(cyfare(domain, session, args))
            if 'digitorus' in valid_sources: tasks.append(digitorus(domain, session, args))
            if 'fofa' in valid_sources: tasks.append(fofa(domain, session, configpath, username, args))
            if 'dnsdumpster' in valid_sources: tasks.append(dnsdumpster(domain, session, configpath, username, args))
            if 'dnsrepo' in valid_sources: tasks.append(dnsrepo(domain, session, args))
            if 'facebook' in valid_sources: tasks.append(facebook(domain, session, configpath, username, args))
            if 'fullhunt' in valid_sources: tasks.append(fullhunt(domain, session, configpath, username, args))
            if 'google' in valid_sources: tasks.append(google(domain, session, configpath, username, args))
            if 'hackertarget' in valid_sources: tasks.append(hackertarget(domain, session, args))
            if 'huntermap' in valid_sources: tasks.append(huntermap(domain, session, configpath, username, args))
            if 'intelx' in valid_sources: tasks.append(intelx(domain, session, configpath, username, args))
            if 'leakix' in valid_sources: tasks.append(leakix(domain, session, configpath, username, args))
            if 'merklemap' in valid_sources: tasks.append(merklemap(domain, args))
            if 'myssl' in valid_sources: tasks.append(myssl(domain, session, args))
            if 'netlas' in valid_sources: tasks.append(netlas(domain, session, configpath, username, args))
            if 'passivetotal' in valid_sources: tasks.append(passivetotal(domain, session, configpath, username, args))
            if 'quake' in valid_sources: tasks.append(quake(domain, session, configpath, username, args))
            if 'rapidapi' in valid_sources: tasks.append(rapidapi(domain, session, configpath, username, args))
            if 'rapiddns' in valid_sources: tasks.append(rapiddns(domain, session, args))
            if 'rapidfinder' in valid_sources: tasks.append(rapidfinder(domain, session, configpath, username, args))
            if 'rapidscan' in valid_sources: tasks.append(rapidscan(domain, session, configpath, username, args))
            if 'redhuntlabs' in valid_sources: tasks.append(redhuntlabs(domain, session, configpath, username, args))
            if 'racent' in valid_sources: tasks.append(racent(domain, session, args))
            if 'rsecloud' in valid_sources: tasks.append(rsecloud(domain, session, configpath, username, args))
            if 'securitytrails' in valid_sources: tasks.append(securitytrails(domain, session, configpath, username, args))
            if 'shodan' in valid_sources: tasks.append(shodan(domain, session, configpath, username, args))
            if 'shodanx' in valid_sources: tasks.append(shodanx(domain, session, args))
            if 'shrewdeye' in valid_sources: tasks.append(shrewdeye(domain, session, args))
            if 'sitedossier' in valid_sources: tasks.append(sitedossier(domain, session, args))
            if 'subdomaincenter' in valid_sources: tasks.append(subdomaincenter(domain, session, args))
            if 'trickest' in valid_sources: tasks.append(trickest(domain, configpath, username, args))
            if 'urlscan' in valid_sources: tasks.append(urlscan(domain, session, args))
            if 'virustotal' in valid_sources: tasks.append(virustotal(domain, session, configpath, username, args))
            if 'waybackarchive' in valid_sources: tasks.append(waybackarchive(domain, args))
            if 'whoisxml' in valid_sources: tasks.append(whoisxml(domain, session, configpath, username, args))
            if 'zoomeyeapi' in valid_sources: tasks.append(zoomeyeapi(domain, session, configpath, username, args))

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
        current = "v2.0.0"
        if latest == current:
            print(f"[{blue}{bold}version{reset}]:{bold}{white}subdominator current version {current} ({green}latest{reset}{bold}{white}){reset}", file=sys.stderr)
        else:
            print(f"[{blue}{bold}version{reset}]: {bold}{white}subdominator current version {current} ({red}outdated{reset}{bold}{white}){reset}", file=sys.stderr)
            
    except KeyboardInterrupt as e:
        SystemExit
    
    
def update_handler():
    try:
        if args.show_updates:
            updatelog()
            quit()
        
        current = "v2.0.0"
        pypiold = "2.0.0"
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
        if cache:
            launch(zipurl, cache)
        else:
            launch(zipurl, os.getcwd())
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
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Current Available passive resources: [{len(resources)}]{reset}", file=sys.stderr)
        else:
            print(f"[INFO]: Current Available passive resources: [{len(resources)}]", file=sys.stderr)
        
        if not args.no_color:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Sources marked with an * needs API key(s) or token(s) configuration to works{reset}", file=sys.stderr)
        else:
            print(f"[INFO]: Sources marked with an * needs API key(s) or token(s) configuration to works", file=sys.stderr)
        
        if not args.no_color:
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Hey {username} you can config your api keys or token here {configpath} to work{reset}", file=sys.stderr)
        else:
            print(f"[INFO]: Hey {username} you can config your api keys or token here {configpath} to work", file=sys.stderr)
        print()
        console = Console()
        for sourced in resources:
            console.print(Markdown(sourced))
        quit()    
    except KeyboardInterrupt as e:
        SystemExit
        
        
async def _domain_handler_(domain, provided_sources):
    try:
        start = time.time()
        results = await __initiate__(domain, provided_sources)
        filtered = filters(results)
        final= set()

        for subdomain in filtered:
            if args.filter_wildcards:
                if subdomain.startswith("*."):
                    subdomain = subdomain[2:]
            if subdomain.endswith(f".{domain}") and subdomain not in final:
                print(subdomain)
                final.add(subdomain)
                if args.output:
                    file(subdomain, domain, args)
                elif args.output_directory:
                    dir(subdomain, domain, args)

        if args.output_json:
            await jsonsave(domain, final,args.output_json, args)
        
        if args.notify:
            await notify(domain, final, configpath, username, args)
            
        end = time.time()
        total_time = end - start
        if not args.silent:
            if args.no_color:
                print(f"[WISH]: Happy Hacking {username} ☠️ 🔥 🚀", file=sys.stderr)
                if args.sources:
                    print(f"[INFO]: Total {len(final)} subdomains found for {domain} in {total_time:.2f} from {len(args.sources)} sources [{', '.join(args.sources)}]", file=sys.stderr)
                else:
                    print(f"[INFO]: Total {len(final)} subdomains found for {domain} in {total_time:.2f} seconds from all sources", file=sys.stderr)
            else:
                print(f"[{bold}{green}WISH{reset}]: {bold}{white}Happy Hacking {username} ☠️ 🔥 🚀{reset}", file=sys.stderr)
                if args.sources:
                    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Total {len(final)} subdomains found for {domain} in {total_time:.2f} seconds from {len(args.sources)} sources [{green}{', '.join(args.sources)}{reset}{bold}{white}]{reset}", file=sys.stderr)
                else:
                    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Total {len(final)} subdomains found for {domain} in {total_time:.2f} seconds seconds from all sources{reset}", file=sys.stderr)

    except KeyboardInterrupt as e:
        SystemExit

async def handler():
    try:
        if args.help:
            print(banners, file=sys.stderr) #cannot be silent in help menu
            help(configpath)
            quit()
        if not args.silent:
            print(banners, file=sys.stderr)
            if not args.disable_update_check:
                gitversion()
        if args.list_source:
            show_sources()
        if args.update or args.show_updates:
            update_handler()
        if args.sources:
            if not args.silent:
                if not args.no_color:
                    # Print info on sources provided
                    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Sources Provided: {len(args.sources)} [{green}{', '.join(args.sources)}{reset}{bold}{white}] {reset}", file=sys.stderr)
                else:
                    print(f"[INFO]: Sources Provided: {len(args.sources)} [{', '.join(args.sources)}]", file=sys.stderr)
        else:
            if not args.silent:
                if not args.no_color:
                    # Print info on sources provided
                    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Using all sources for enumeration [{green}Default{reset}{bold}{white}] {reset}", file=sys.stderr)
                else:
                    print(f"[INFO]: Using all sources for enumeration [Default]", file=sys.stderr)

        if args.domain:
            if not args.silent:
                if not args.no_color:
                    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Loading provider configuration file from {configpath}{reset}", file=sys.stderr)
                    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Enumerating subdomain for {args.domain}{reset}", file=sys.stderr)

                else:
                    print(f"[INFO]: Loading provider configuration file from {configpath}", file=sys.stderr)
                    print(f"[INFO]: Enumerating subdomain for {args.domain}", file=sys.stderr)
        
            await _domain_handler_(args.domain, args.sources)
            quit()

        if args.domain_list:
            if not args.silent:
                if not args.no_color:
                    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Loading provider configuration file from {configpath}{reset}", file=sys.stderr)
                else:
                    print(f"[INFO]: Loading provider configuration file from {configpath}", file=sys.stderr)
                
            domains = reader(args.domain_list, args)
            if domains:
                for domain in domains:
                    if not args.silent:
                        if not args.no_color:
                            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Enumerating subdomain for {domain}{reset}", file=sys.stderr)
                        else:
                            print(f"[INFO]: Enumerating subdomain for {domain}", file=sys.stderr)
                    await _domain_handler_(domain, args.sources)
                quit()
            
        if sys.stdin.isatty():
            if not args.no_color:
                    print(f"[{bold}{red}WRN{reset}]: {bold}{white}subdominator exits due to no inputs provided, please use subdominator -h for more details", file=sys.stderr)
            else:
                    print(f"[WRN]: subdominator exits due to no inputs provided, please use subdominator -h for more details", file=sys.stderr)
            quit()  
        else:
            for domain in sys.stdin:
                if domain:
                    domain = domain.strip()
                    if not args.silent:
                        if not args.no_color:
                            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Enumerating subdomain for {domain}{reset}", file=sys.stderr)
                        else:
                            print(f"[INFO]: Enumerating subdomain for {domain}", file=sys.stderr)
                    await _domain_handler_(domain, args.sources)
            quit()
    except KeyboardInterrupt as e:
        quit()
            

def main_handler():
    try:
        asyncio.run(handler())
    except KeyboardInterrupt as e:
        quit()