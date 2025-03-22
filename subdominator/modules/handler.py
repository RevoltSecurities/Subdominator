import os
import sys
import time
import asyncio
from rich.console import Console
from rich.markdown import Markdown
import httpx
from colorama import Fore,Style
import random
import json

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
    from .config.config import config, custompath, Username, cachedir,db_config
    from .help.help import help
    from .source.source import sources
    from .update.update import *
    from .version.version import version
    from .logger.logger import logger
    from .utils.utils import filters,reader,split_to_list, check_directory_permission,check_file_permission, Exit
    from .subscraper.abuseipdb.abuseipdb import abuseipdb
    from .subscraper.alienvault.alientvault import alienvault
    from .subscraper.anubis.anubis import anubis
    from .subscraper.arpsyndicate.arpsyndicate import arpsyndicate
    from .subscraper.bevigil.bevigil import bevigil
    from .subscraper.binaryedge.binaryedge import binaryedge
    from .subscraper.bufferover.bufferover import bufferover
    from .subscraper.builtwith.builtwith import builtwith
    from .subscraper.c99.c99 import c99
    from .subscraper.censys.censys import censys
    from .subscraper.certspotter.certspotter import certspotter
    from .subscraper.chaos.chaos import chaos
    from .subscraper.coderog.coderog import coderog
    from .subscraper.commoncrawl.commoncrawl import commoncrawl
    from .subscraper.crtsh.crtsh import crtsh
    from .subscraper.cyfare.cyfare import cyfare
    from .subscraper.digitorus.digitorus import digitorus
    from .subscraper.dnsdumpster.dnsdumpster import dnsdumpster
    from .subscraper.dnsrepo.dnsrepo import dnsrepo
    from .subscraper.facebook.facebook import facebook
    from .subscraper.fullhunt.fullhunt import fullhunt
    from .subscraper.fofa.fofa import fofa
    from .subscraper.google.google import google
    from .subscraper.hackertarget.hackertarget import hackertarget
    from .subscraper.huntermap.huntermap import huntermap
    from .subscraper.intelx.intelx import intelx
    from .subscraper.leakix.leakix import leakix
    from .subscraper.merklemap.merklemap import merklemap
    from .subscraper.myssl.myssl import myssl
    from .subscraper.netlas.netlas import netlas
    from .subscraper.quake.quake import quake
    from .subscraper.racent.racent import racent
    from .subscraper.rapidapi.rapidapi import rapidapi
    from .subscraper.rapidfinder.rapidfinder import rapidfinder
    from .subscraper.rapidscan.rapidscan import rapidscan
    from .subscraper.rapiddns.rapiddns import rapiddns
    from .subscraper.redhuntlabs.redhuntlabs import redhuntlabs
    from .subscraper.rsecloud.rsecloud import rsecloud
    from .subscraper.securitytrails.securitytrails import securitytrails
    from .subscraper.shodan.shodan import shodan
    from .subscraper.shodanx.shodanx import shodanx
    from .subscraper.shrewdeye.shrewdeye import shrewdeye
    from .subscraper.sitedossier.sitedossier import sitedossier
    from .subscraper.trickest.trickest import trickest
    from .subscraper.urlscan.urlscan import urlscan
    from .subscraper.virustotal.virustotal import virustotal
    from .subscraper.waybackarchive.waybackarchive import waybackarchive
    from .subscraper.whoisxml.whoisxml import whoisxml
    from .subscraper.zoomeyeapi.zoomeyeapi import zoomeyeapi
    from .subscraper.digitalyama.digitalyama import digitalyama
    from .subscraper.odin.odin import odin
    from .subscraper.hudsonrock.hudsonrock import hudsonrock
    from .subscraper.threatcrowd.threatcrowd import threatcrowd
    from .save.save import file, dir, jsonsave
    from .notify.notify import notify
except ImportError as e:
    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Import Error occured in  Subdominator Module imports due to: {e}{reset}", file=sys.stderr)
    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}If you are encountering this issue more than a time please report the issues in Subdominator Github page.. {reset}", file=sys.stderr)
    sys.exit(1)
    
args = cli()
if not args.config_path:
    configpath = config()
else:
    
    configpath = custompath(args.config_path,args)
    if not configpath:
        logger(f"Unable to load the custom provider config file, please check the file exist", "warn", args.no_color)
        Exit(1)
        

if not args.config_db_path:
    dbpath = db_config()
else:
    dbpath = custompath(args.config_db_path,args)
    if not dbpath:
        logger(f"Unable to load the custom subdominator DB , please check the DB exist", "warn", args.no_color)
        Exit(1)
    
from .models.models import AsyncSessionLocal
from .crud.crud import get_all_domains,get_domain,get_subdomains,add_or_update_domain
from .shell.shell import SubDominatorShell

banners = banner()
username = Username()

async def __initiate__(domain):
    try:
        async with httpx.AsyncClient(proxy=args.proxy, verify=False) as session:
            tasks = [abuseipdb(domain, session, args), 
                     alienvault(domain, session, args), 
                     anubis(domain, session, args), 
                     arpsyndicate(domain, session, configpath,args),
                     bevigil(domain, session, configpath, username, args), 
                     binaryedge(domain, session, configpath, username, args), 
                     bufferover(domain, session, configpath, username, args), 
                     builtwith(domain, session, configpath, username, args), 
                     c99(domain, session, configpath, username, args),
                     censys(domain, session, configpath, username, args), 
                     certspotter(domain, session, configpath, args), 
                     chaos(domain, session, configpath,  args), 
                     coderog(domain, session, configpath, args), 
                     commoncrawl(domain, args), 
                     crtsh(domain, session, args), 
                     cyfare(domain, session, args), 
                     digitorus(domain, session, args), 
                     fofa(domain,session, configpath, username, args), 
                     dnsdumpster(domain, session, configpath,args), 
                     dnsrepo(domain,session, configpath, username,args), 
                     facebook(domain, session, configpath, username, args), 
                     fullhunt(domain, session, configpath, username, args), 
                     google(domain, session, configpath, username, args), 
                     hackertarget(domain, session, args), 
                     huntermap(domain, session, configpath, username, args),  
                     intelx(domain, session, configpath, username, args), 
                     leakix(domain, session, configpath, username, args), 
                     merklemap(domain, session,configpath,username,args), 
                     myssl(domain, session, args), 
                     netlas(domain, session, configpath, username, args), 
                     quake(domain, session, configpath, username, args), 
                     rapidapi(domain, session, configpath, args), 
                     rapiddns(domain, session, args),  
                     rapidfinder(domain, session, configpath, username, args),  
                     rapidscan(domain, session, configpath, username, args), 
                     redhuntlabs(domain, session, configpath, username, args) , 
                     racent(domain, session, args) ,
                     rsecloud(domain, session, configpath, username, args) , 
                     securitytrails(domain, session, configpath, username, args), 
                     shodan(domain, session, configpath, username, args), 
                     shodanx(domain, session, args), 
                     shrewdeye(domain, session, args), 
                     sitedossier(domain, session, args), 
                     trickest(domain, configpath, args), 
                     urlscan(domain, session, args), 
                     virustotal(domain, session, configpath, username, args), 
                     waybackarchive(domain, args), 
                     whoisxml(domain, session, configpath, username, args), 
                     zoomeyeapi(domain, session, configpath, username, args),
                     digitalyama(domain, session, configpath, username, args), 
                     odin(domain, session,configpath,username,args), 
                     hudsonrock(domain, session, args), 
                     threatcrowd(domain, session, args) 
                     ]             
            results = await asyncio.gather(*tasks)
            return results        
    except Exception as e:
        if args.verbose:
            logger(f"Exception handler sources: {e}, {type(e)}", "warn", args.no_color)

def gitversion():
    try:
        latest = version()
        current = "v2.1.0"
        if latest == current:
            print(f"[{blue}{bold}version{reset}]:{bold}{white}subdominator current version {current} ({green}latest{reset}{bold}{white}){reset}", file=sys.stderr)
        else:
            print(f"[{blue}{bold}version{reset}]: {bold}{white}subdominator current version {current} ({red}outdated{reset}{bold}{white}){reset}", file=sys.stderr)
    except KeyboardInterrupt as e:
        Exit(1)
    
    
def update_handler():
    try:
        if args.show_updates:
            updatelog()
            Exit()
        
        current = "v2.1.0"
        pypiold = "2.1.0"
        git = version()
        
        if current == git:
            logger(f"Hey {username} subdominator is already in new version", "info", args.no_color)
            Exit()
            
        zipurl = getzip()
        if not zipurl:
            logger(f"Hey {username} failed to update subdominator please try manually from github", "warn" , args.no_color)
            Exit()
        cache = cachedir()
        if cache:
            launch(zipurl, cache)
        else:
            launch(zipurl, os.getcwd())
        pypiversion = getverify("subdominator")
        
        if pypiold == pypiversion:
            logger(f"Hey {username} failed to update subdominator please try manually from github", "warn" , args.no_color)
            Exit()

        logger(f"Verified the latest version of subdominator from pypi and updated from {current} --> {git}", "info" , args.no_color)
        updatelog()
        Exit()
                
    except KeyboardInterrupt as e:
        Exit()

def show_sources():
    try:
        resources = sources()
        logger(f"Current Available passive resources: [{len(resources)}]", "info" , args.no_color)
        
        logger(f"Sources marked with an * needs API key(s) or token(s) configuration to works", "info" , args.no_color)
        
        logger(f"Hey {username} you can config your api keys or token here {configpath} to work", "info" , args.no_color)
        console = Console()
        for sourced in resources:
            console.print(Markdown(sourced))
        Exit()    
    except KeyboardInterrupt as e:
        Exit(1)
        
async def _domain_handler_(domain):
    try:
        start = time.time()
        results = await __initiate__(domain)
        filtered = filters(results)
        final= set()

        for subdomain in filtered:
            if subdomain.endswith(f".{domain}") and subdomain not in final:
                if args.filter_wildcards:
                    if subdomain.startswith("*."):
                        subdomain = subdomain[2:]                
                final.add(subdomain)
                    
        for subdomain in final:
            if args.json:
                output = {"domain":f"{domain}", "subdomain": f"{subdomain}"}
                output = json.dumps(output, indent=2)
            else:
                output = subdomain
                    
            print(output)
            if args.output:
                file(output, domain, args)
            elif args.output_directory:
                dir(output, domain, args)
        
        async with AsyncSessionLocal() as db:
            await add_or_update_domain(db, domain, final)
        
        if args.notify:
            await notify(domain, final, configpath, username, args)
            
        end = time.time()
        total_time = end - start
        if not args.silent:
            logger(f"Total {len(final)} subdomains found for {domain} in {total_time:.2f} seconds{reset}", "info" , args.no_color)
            logger(f"Happy Hacking {username} ☠️ 🔥 🚀{reset}", "info" , args.no_color)
    except KeyboardInterrupt as e:
        Exit(1)

async def handler():
    try:
        if args.help:
            print(banners, file=sys.stderr)
            help(configpath, dbpath)
            Exit()
            
        if args.shell:
            print(banners, file=sys.stderr)
            Shell = SubDominatorShell()
            await Shell.cmdloop()
            Exit(0)
            
        if not args.silent:
            print(banners, file=sys.stderr)
            if not args.disable_update_check:
                gitversion()
        if args.list_source:
            show_sources()
        if args.update or args.show_updates:
            update_handler()
            
        if args.include_resources:
            args.include_resources = split_to_list(args.include_resources)
        
        if args.exclude_resources:
            args.exclude_resources = split_to_list(args.exclude_resources)
        
        if args.output:
            perm = await check_file_permission(args.output, args)
            if not perm:
                Exit(1)
                
        if args.output_directory:
            perm = await check_directory_permission(args.output_directory, args)
            if not perm:
                Exit(1)
                
        if args.domain:
            if not args.silent:
                logger(f"Loading provider configuration file from {configpath}", "info" , args.no_color)
        
                logger(f"Enumerating subdomain for {args.domain}", "info" , args.no_color)
            await _domain_handler_(args.domain)
            Exit()
    
        if args.domain_list:
            if not args.silent:
                logger(f"Loading provider configuration file from {configpath}", "info" , args.no_color)
            domains = reader(args.domain_list, args)
            if domains:
                for domain in domains:
                    if not args.silent:
                        logger(f"Enumerating subdomain for {domain}", "info" , args.no_color)
                        
                    await _domain_handler_(domain)
                Exit()
            
        if sys.stdin.isatty():
            logger(f"subdominator exits due to no inputs provided, please use subdominator -h for more details", "warn", args.no_color)
            Exit()  
        else:
            if not args.silent:
                logger(f"Loading provider configuration file from {configpath}", "info" , args.no_color)
            for domain in sys.stdin:
                if domain:
                    domain = domain.strip()
                    if not args.silent:
                        logger(f"Enumerating subdomain for {domain}", "info" , args.no_color)
                    await _domain_handler_(domain)
            Exit()
    except KeyboardInterrupt as e:
        Exit()
            

def main_handler():
    try:
        asyncio.run(handler())
    except KeyboardInterrupt as e:
        sys.exit(1)