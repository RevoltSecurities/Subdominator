#!/usr/bin/python3
import httpx
import pywebio
import requests
from colorama import Fore,Back,Style
import argparse
import yaml
import time as t
import re
import random
import datetime
import os
from plyer import notification
import sys
from censys.search import CensysCerts
import concurrent.futures
from censys.common.exceptions import CensysUnauthorizedException, CensysRateLimitExceededException,CensysException


red =  Fore.RED

green = Fore.GREEN

magenta = Fore.MAGENTA

cyan = Fore.CYAN

mixed = Fore.RED + Fore.BLUE

blue = Fore.BLUE

yellow = Fore.YELLOW

white = Fore.WHITE

reset = Style.RESET_ALL

colors = [red, green, yellow, cyan, blue, magenta]

random_color = random.choice(colors)

banner = """

                  _____       __        __                _             __            
                 / ___/__  __/ /_  ____/ /___  ____ ___  (_)___  ____ _/ /_____  _____
                 \__ \/ / / / __ \/ __  / __ \/ __ `__ \/ / __ \/ __ `/ __/ __ \/ ___/
                ___/ / /_/ / /_/ / /_/ / /_/ / / / / / / / / / / /_/ / /_/ /_/ / /    
               /____/\__,_/_.___/\__,_/\____/_/ /_/ /_/_/_/ /_/\__,_/\__/\____/_/     
             
             
                            
                            
                                        Author  : D.Sanjai Kumar
                                                                

"""


subdomains_list = []

start = t.time()




#creating new and old arguments to pass values:

parser = argparse.ArgumentParser(description=f"{cyan}Subdominator Unleash the Power of Subdomain Enumeration{reset}")

parser.add_argument("-d", "--domain", help=f"[{green}ALERT{reset}]:Domain name to find the Subdomains", type=str)

parser.add_argument("-dL", "--domains-list", help=f"[{green}ALERT{reset}]:Filename that contains list of domains to find Subdomains", type=str)

parser.add_argument("-nt", "--notify", help=f"[{green}ALERT{reset}]:Send Push notification to your Android Phone or Desktop when Subdominator finished its processs", action="store_true")

parser.add_argument("-r", "--recursive", help=f"[{green}ALERT{reset}]:Do recursive enumeration for wildcards in found subdomains",action="store_true")

parser.add_argument("-vrs", "--version", help=f"[{green}ALERT{reset}]: Checks for the latest version of Subdominator",action="store_true")

parser.add_argument("-cf", "--config", help=f"[{green}INFO{reset}]:Subdominator find subdomain with the configured api keys", action="store_true")

parser.add_argument("-o", "--output", help=f"[{green}INFO{reset}]: Filename to save the output", type=str)

args=parser.parse_args()

list = args.domains_list

domain = args.domain

config = args.config 

recursive =  args.recursive 

version = args.version 

notify = args.notify 

output = args.output 



#get version for version flag



# get the latest version when given domains or domain
def check_version():
    
    version = "v1.0.4"
    
    url = f"https://api.github.com/repos/sanjai-AK47/Subdominator/releases/latest"
    
    try:
        
        response = requests.get(url)
        
        if response.status_code == 200:
            
            data = response.json()
            
            latest = data.get('tag_name')
            
            if latest == version:
                
                
                print(f"[{blue}Version{reset}]: Subdominator current version {version} ({green}latest{reset})")
                
                t.sleep(1)
                
                
            else:
                
                print(f"[{blue}Version{reset}]: Subdominator current version {version} ({red}outdated{reset})")
                
                print(f"[{red}ALERT{reset}]: Subdominator new version detected update to latest version")
                
                t.sleep(1)
                
        else:
            
            pass
                
    except Exception as e:
        
        pass
    
    
# get unique subdomains for file that contains list of domains

def list_unique_subdomains(subdomains):
    
    unique_subdomains = sorted(set(subdomains))
    
    for subdomain in unique_subdomains:
        
            
        print(f"[{random_color}Subdominator{reset}]: {subdomain}")
            

        if args.output:
            
            if os.path.isfile(args.output):
                
                filename = args.output
                
            elif os.path.isdir(args.output):
                
                filename = os.path.join(args.output, f"{domain}.subdomains.txt")
                
            else:
                
                filename = args.output
                
        if not args.output:
            
            filename = f"{domain}.subdomains.txt"
            
        
        with open(filename, "a") as w:
            
            w.write(subdomain + '\n')
    
    total = len(unique_subdomains) 
    
    end = t.time()
    
    temp_time = end - start
    
    if temp_time > 60:
        
        total_time_taken = temp_time/60
        
        print(f"[{blue}INFO{reset}]: Total subdomains found {total} in {total_time_taken:.2f} minutes ")
        
    elif temp_time < 60:
        
        total_time_taken = temp_time
        
        print(f"[{blue}INFO{reset}]: Total subdomains found {total} in {total_time_taken:.2f} seconds ")
    
    print(f"[{blue}INFO{reset}]: Output for {domain} save in {filename}")
    
    print(f"[{green}WISH{reset}]: Happy Hacking Hacker ☠️ 🔥 🚀")
    
    subdomains_list.clear()
    
#get unique subdomains for single domain 

def single_unique_subdomains(subdomains):
    
    unique_subdomains = sorted(set(subdomains))
    
    for subdomain in unique_subdomains:
        
        
        if subdomain.endswith(args.domain):
        
            
            print(f"[{random_color}Subdominator{reset}]: {subdomain}")
            
        else:
            
            pass 
        
        
        if args.output:
            
            if os.path.isfile(args.output):
                
                filename = args.output
                
            elif os.path.isdir(args.output):
                
                filename = os.path.join(args.output, f"{domain}.subdomains.txt")
                
            else:
                
                filename = args.output
                
        if not args.output:
            
            filename = f"{domain}.subdomains.txt"
            
        
        with open(filename, "a") as w:
            
            w.write(subdomain + '\n')
    
    total = len(unique_subdomains)
    
    end = t.time()
    
    temp_time = end - start
    
    if temp_time > 60:
        
        total_time_taken = temp_time/60
        
        print(f"[{blue}INFO{reset}]: Total {total} subdomains found for {args.domain} in {total_time_taken:.2f} minutes ")
        
    elif temp_time < 60:
        
        total_time_taken = temp_time
        
        print(f"[{blue}INFO{reset}]: Total {total} subdomains found for {args.domain} in {total_time_taken:.2f} seconds ")
    
    
    print(f"[{blue}INFO{reset}]: Output for {args.domain} save in {filename}")
    
    print(f"[{green}WISH{reset}]: Happy Hacking Hacker ☠️ 🔥 🚀")
    
    
    
    
#check for user config
def check_config_file():
    
    filename = "config_keys.yaml"
    
    path = "/"
    
    for root,dirs,files in os.walk(path):
        
        if filename in files:
            
            file_path = os.path.join(root, filename)
            
            print(f"[{blue}INFO{reset}]: Loading the configuration file from {file_path}")
            
            return file_path
        
    print(f"[{red}ALERT{reset}]: Config File not found please kindly install the Subdomiantor with its {filename} file")
    
    exit()
    

#=================================================================================API calls here========================================================================================================================================

#virustotal works good with random api keys 
def api_virustotal(domain, filename):
    
    try:
        
        with open (filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            
                
        virus_key = random.choice(data.get("Virustotal", []))
        
        
                
        if virus_key is None:
            
                print(f"[{red}ALERT{reset}]: There is no api keys found for VirusTotal ")
                        
                return
            
        else:
            
                pass 
                
        try:
                    
                    url = f"https://www.virustotal.com/vtapi/v2/domain/report?apikey={virus_key}&domain={domain}"
                    
                    with httpx.Client() as requests:
                    
                        response = requests.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        
                        data = response.json()
                        
                        if 'subdomains' in data:
                            
                            subdomains = data['subdomains']
                            
                            for subdomain in subdomains:
                                
                                subdomains_list.append(subdomain)
                        
                                
                            
                        else:
                            print(f"[{red}ALERT{reset}]: VirusTotal Unable to find subdomains for {domain}")
                            
                        
                            
                        
                        
                    else:
                        
                        print(f"[{red}ALERT{reset}]: VirusTotal blocking our requests Check your api usage: {virus_key}")
                        
        except Exception as e:
                    
                    print (f"[{red}Alert{reset}]: Virustotal Blocking our requests")
                
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values fo VirusTotal")
        
            return



#Chaos works good 

def api_chaos(domain, filename):
    
    try:
        
        with open(filename, "r") as key:
            
            data = yaml.safe_load(key)
            
            
                
        chaos_api_key = random.choice(data.get('Chaos', []))
                
        if chaos_api_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api keys found for Chaos ")
                        
                        return
            
            
        else:
            
                        pass

        url = f"https://dns.projectdiscovery.io/dns/{domain}/subdomains"

        headers= {
                        'Authorization': chaos_api_key
                }
    
        try:
                    
                    with httpx.Client() as requests:
                    
                        response = requests.get(url,headers=headers, timeout=15)

                    if response.status_code == 200:

                            data = response.json()
    
                            if 'subdomains' in data:
                            
                                        subdomains = data['subdomains']
                            
                                        for subdomain in subdomains:
                                            
                                            if not subdomain.endswith(f".{domain}"):
                                
                                                subdomains_list.append(f"{subdomain}.{domain}")
                                                
                                            else:
                                                
                                                subdomains_list.append(f"{subdomain}")
                                                
                            else:
                
                                pass
                            
                            
                    else:
                            
                        print(f"[{red}ALERT{reset}]: Chaos blocking our requests check your api usage {chaos_api_key} ")
            
            
                    
        except Exception as e:
                
                print(f"[{red}ALERT{reset}]: Chaos Blocking our requests {e}") 
                
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Chaos")
        
            return  
        
        
#whoisxml works good 


def whoisxml_api(domain, filename):
    
    try:
        
        with open(filename, "r") as key:
            
            data = yaml.safe_load(key)
            
        
        whois_api_key = random.choice(data.get('Whoisxml', []))
            
        if whois_api_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api keys found for whoisxml api ")
                        
                        pass
        else:
            
                        pass
            
            
        
        try:
                
                url = f"https://subdomains.whoisxmlapi.com/api/v1?apiKey={whois_api_key}&domainName={domain}"
                
                
                with httpx.Client() as requests:
                
                    response = requests.get(url, timeout=10)
            
                if response.status_code == 200:
                
                    data = response.json()
                    
                    subdomains = data.get('result', {}).get('records', [])
                    
                    for subdomain in subdomains:
                
                            subdomain_name = subdomain.get('domain')
                            
                            if subdomain_name:
                                
                                subdomains_list.append(subdomain_name)
                                
                            else:
                                
                                pass
                elif response.status_code == 402:
                                
                        print(f"[{red}ALERT{reset}]: Whoisxmlapi blocking our request check your api usage {whois_api_key}")
                        
                else:
                    
                    pass 
                        
        except Exception as e:
                
                print(f"[{red}ALERT{reset}]: Whoisxmlapi blocking our request")
                
        
                
        
        
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Whoisxml")
        
            return
    
#security trails works good now 
def api_securitytrails(domain, filename):
    
    try:
        
        with open(filename, "r") as key:
            
            data = yaml.safe_load(key)
            
            
        security_api_key = random.choice(data.get('SecurityTrails', []))
            
        if security_api_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api keys found for SecurityTrails ")
                        
                        return
        else:
            
                        pass
            
            
        try:
                
                url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains?children_only=false&include_inactive=true"
            
                headers = {
                "accept": "application/json",
                "APIKEY": security_api_key
                }         
                
                
                with httpx.Client() as requests: 
                
                    response = requests.get(url , headers=headers, timeout=10)
                
                if response.status_code ==  200:
                    
                    data = response.json()
                    
                    subdomains = data.get("subdomains", [])
                    
                    for subdomain in subdomains:
                            
                            subdomains_list.append(f"{subdomain}.{domain}")
                
                elif response.status_code == 429:
                    
                    print(f"[{red}ALERT{reset}]: SecurityTrails blocking our request check your api usage {security_api_key}")
                    
                else:
                    
                    pass 
                    
                    
        except Exception as e:
                
                print(f"[{red}ALERT{reset}]: SecurityTails blocking our request")
                    
                    
            
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of SecurityTrails")
        
            return
    
    
#bevigil works good

def api_bevigil(domain, filename):
    
    try:
        
        with open(filename, "r") as key:
            
            data =  yaml.safe_load(key)
            
        bevigil_api_key = random.choice(data.get('Bevigil', []))
        
        if bevigil_api_key is None:
            
            print(f"[{red}ALERT{reset}]: There is no api keys found for Bevigil ")
            
            pass
        else:
            
            pass
        
        
        try:
            
            
            
            url = f"http://osint.bevigil.com/api/{domain}/subdomains"
        
            headers = {
            'X-Access-Token': bevigil_api_key
            
            }
            
            
            response = requests.get(url, headers=headers, timeout=10)
            
            
            
            if response.status_code == 200:
                
                data =  response.json()
                
                
                subdomains = data.get("subdomains", [])
                
                for subdomain in subdomains:
                    
                    subdomains_list.append(subdomain)
                
            elif response.status_code == 429:
                
                print(f"[{red}ALERT{reset}]: Bevigil blocking our request check your api usage {bevigil_api_key}")
                
            else:
                
                pass  
                
        except Exception as e:
            
            
                    print(f"[{red}ALERT{reset}]: Bevigil blocking our request ")
            
        
        
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Bevigil")
        
            return
    
    
#bufferover

def api_bufferover(domain,filename):
    
    try:
        with open(filename, "r") as key:
            
            data = yaml.safe_load(key)
        
        bufferover_api_key = random.choice(data.get('Bufferover', []))
            
        if bufferover_api_key is None:
            
            print(f"[{red}ALERT{reset}]: There is no api keys found for Bufferover ")
                        
            return
            
        else:
            
            pass
            
        try:
            
            url = f"http://tls.bufferover.run/dns?q=.{domain}"
            
            headers = {
            'x-api-key': f'{bufferover_api_key}'
            }
            
            with httpx.Client() as requests:
                
                response = requests.get(url,headers=headers, follow_redirects=True)
                
            
            if response.status_code == 200:
                
                data = response.json()
                
                if 'Results' in data:
                    
                    results = data['Results']
                    
                    for result in results:
                        
                            elements = result.split(',')
                            
                            subdomain = elements[4].strip()

                            subdomains_list.append(subdomain)
                            
                elif response.status_code == 500:
                    
                    
                    print(f"[{red}INFO{reset}]: Buffer over Internal Error occured")
                    
                else:
                    
                    print(f"[{blue}INFO{reset}]: Bufferover not able to find subdomains for {domain}")
                    
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: Bufferover blocking our requests")
                    
            
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Bufferover")
            
        
            return
        
#missInteg binary edge works good

def api_binaryegde(domain, binaryedge_api_key, page_number, pagesize):
    
    try:
        
        url = f"https://api.binaryedge.io/v2/query/domains/subdomain/{domain}?page={page_number}&pagesize={pagesize}"
        
        headers = {
            'X-Key': f'{binaryedge_api_key}'
        }
        with httpx.Client() as requests:
            
            response = requests.get(url, headers=headers, timeout=10)
            
        if response.status_code == 200:
            
            data = response.json()
            
            subdomains = data.get("events", [])
            
            
            if not subdomains:
                
                
                return False
            
            for subdomain in subdomains:
                
                subdomains_list.append(subdomain)
                
            return True
        else:
            
            pass
             
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: BinaryEdge blocking our requests")
        
        return False

def send_binaryedge(domain, filepath):
    
    try:
        
        with open(filepath, "r") as key:
            
            data = yaml.safe_load(key)
            
        binaryedge_api_key = random.choice(data.get('Binaryedge', []))
        
        if binaryedge_api_key is None:
            
            print(f"[{red}ALERT{reset}]: There is no API key found for BinaryEdge ")
            
            return
        else:
            
            pass
        
        pagesize = 100
        
        page_number = 1
        while True:
            
            if not api_binaryegde(domain, binaryedge_api_key, page_number, pagesize):
                
                break  
            
            page_number += 1
            
            t.sleep(1) 
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Please Check that You didn't mess up the Configuration files variables and their Values of BinaryEdge")
        
        return

        
#Certspotter  works good 

def api_certspoter(domain, filename):
    
    try:
        
        with open(filename,"r") as keys:
            
            data = yaml.safe_load(keys)
            
        certspotter_api_key = random.choice(data.get('Certspotter', []))
        
        if certspotter_api_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api keys found for Certspotter ")
                        
                        pass
        else:
            
            pass
        
        try:
            
            url = f"https://api.certspotter.com/v1/issuances?domain={domain}&expand=dns_names"
            
            headers = {"Authorization": f"Bearer {certspotter_api_key}"}
            
            with httpx.Client() as requests:
            
                response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                
                data = response.json()
                
                for entry in data :
                    
                    dns_names = entry.get('dns_names',[])
                    
                    for dns_name in dns_names:
                        
                        if dns_name.startswith("*.") and dns_name.endswith(domain):
                            
                            subdomain = dns_name[2:]
                            
                            subdomains_list.append(subdomain)
                        
                        elif dns_name.endswith(domain):
                            
                            subdomains_list.append(dns_name)
                        else:
                            pass
                        
            elif response.status_code >= 400:
                
                print(f"[{red}ALERT{reset}]: Certspotter blocking our request check your api usage {certspotter_api_key}")
                
                
                
            else:
                
                pass 
                
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: Certspotter blocking our requests")
            
            
            
        
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Certspotter")
            
        
            return
        
        
#rapidwhois works execellent

def rapid_whois(domain, filename):
    
    try :
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
        rapid_api_key = random.choice(data.get('Rapidapi', []))
        
        integrated_key = random.choice(data.get('Whoisxml', []))
        
        if rapid_api_key is None or integrated_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api keys found for Rapidapi and Whoisxmlapi")
                        
                        return 
            
        else:
            
                        pass
                    
                    
        try:
            
            url = "https://subdomains-lookup.p.rapidapi.com/api/v1"

            querystring = {"domainName": domain,"apiKey": integrated_key ,"outputFormat":"JSON"}

            headers = {
	"X-RapidAPI-Key": rapid_api_key,
	"X-RapidAPI-Host": "subdomains-lookup.p.rapidapi.com"
}
            
            with httpx.Client() as requests:
                
                response = requests.get(url, headers=headers, params=querystring, timeout=10)
            
            if response.status_code == 200:
                
                data = response.json()
                
                records = data.get('result', {}).get('records', [])
                
                for record in records:
                    
                    subdomain= record.get('domain')
                    
                    if subdomain:
                        
                        subdomains_list.append(subdomain)
                    else:
                        
                        pass
            elif response.status_code == 402:
                
                print (f"[{red}Alert{reset}]: RapidWhois Blocking our requests check your api usage of Rapid {rapid_api_key} and Whoisxml {integrated_key} api keys ")
                
            else: 
                
                pass 
            
        except Exception as e:
            
            print (f"[{red}Alert{reset}]: RapidWhois Blocking our requests")
                    
                    
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Rapidapi and Whoisxml")
            
        
            return
    
    
#Dnsdumpster works good 

def non_api_dnsdump(domain, filename):
    
    try:
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
        data = random.choice(data.get("Dnsdumpter", []))
            
        csrf_cookie , csrf_token = data.split(":")
            
        if csrf_cookie is None or csrf_token is None:
                
                print(f"[{red}ALERT{reset}]: There is no csrf token or csrf cookie found for the DnsDump  ")
                        
                pass 
            
        else:
            
                pass
                
                
            
        try:
                
                url = f"https://dnsdumpster.com/"
                
                headers = headers = {
                'Cookie': f'csrftoken={csrf_cookie}',
                'Referer': 'https://dnsdumpster.com/'
                }
                data = {
                'csrfmiddlewaretoken': f'{csrf_token}',
                'targetip': domain,
                'user': 'free'
               }
                try:
                    
                    with httpx.Client() as requests:
                    
                        response = requests.post(url, headers=headers, data=data, timeout=10)
                    
                    if response.status_code == 200:
                        
                        content =  response.text
                        
                        subdomains_pattern = re.compile(rf"\b[a-zA-Z0-9]+\b\.{domain}\b")
                        
                        subdomains = subdomains_pattern.findall(content)
                        
                        for subdomain in subdomains:
                            
                            subdomains_list.append(subdomain)
                    else:
                        
                        print(f"[{red}ALERT{reset}]: DnsDumpster Blocking our requests check the csrf token and csrf cookie")
                        
                            
                except Exception as e:
                    print(f"[{red}ALERT{reset}]: DnsDumpster Blocking our requests")
                    
        except Exception as e:
                
                print(f"[{red}ALERT{reset}]: There is no csrf cookie and csrf token found for DsnDumpster")
    
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of DnsDumpster")
            
        
            return
        
#leakix works good 

def api_leakix(domain, filename):
    
    
    try:
        
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            leakix_key = random.choice(data.get("Leakix", []))
            
            
            if leakix_key is None :
            
                        print(f"[{red}ALERT{reset}]: There is no api keys found for leakix api ")
                        
                        return 
            
            else:
            
                        pass
                    
        try:
            
            url = f"https://leakix.net/api/subdomains/{domain}"
            
            headers = {"accept": "application/json", 
                    "api-key": f"{leakix_key}",
                    }
            
            with httpx.Client() as requests:

                response = requests.get(url, headers=headers, timeout=10)
                
                data = response.json()
                
                if response.status_code == 200:
                
                    for subdomains in data:
                    
                        subdomain = subdomains.get('subdomain', {} )
                    
                        subdomains_list.append(subdomain)
                        
                elif response.status_code == 429:
                    
                    print(f"[{red}ALERT{reset}]: Leakix blocking our requests check your api usage")
                    
                else:
                    
                    pass 
                    
                    
                
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: Leakix blocking our requests")
                
                    
    
    
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Leakix")
        
            return
        
#The Censys api works execellent with it results

def api_censys(domain,file_path):
    
    try:
        
        filename = file_path
        
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
        data = random.choice(data.get('Censys', []))
            
        censys_id,censys_key = data.split(':')
            
        if censys_id is None or censys_key is None:
            
                        print(f"[{red}ALERT{reset}]: May be There is no api key or api secret id found for Censys api ")
                        
                        return 
            
        else:
            
                        pass
                    
        try:            
            
            USER_agent=f"{CensysCerts.DEFAULT_USER_AGENT} Subdominator/1.1 (+https://github.com/sanjai-AK47/Subdominator)"
            
            censys_query = CensysCerts(api_id=censys_id,api_secret=censys_key, user_agent=USER_agent)
            
            get_domains = f"names: {domain}"
            
            max_limits = 100
            
            min_limits = 10
            
            censys_subdomains = censys_query.search(get_domains, per_page=max_limits, pages=min_limits)
            
            
            data = censys_subdomains
            
            temp_list = []
            
            for subdomains in data:
                
                for subdomain in subdomains: 
                    
                        temp_list.extend(subdomain.get("names", []))
                        
            for subdomain in temp_list:
                
                if subdomain.startswith("*.") and subdomain.endswith(domain):
                    
                    
                    subdomain = subdomain[2:]
                            
                    subdomains_list.append(subdomain)
                        
                elif subdomain.endswith(domain):
                            
                            subdomains_list.append(subdomain)
                            
                else:
                    
                    pass
                        
                        
            
                        
                        
                        
        except CensysUnauthorizedException:
            
            print(f"[{red}ALERT{reset}]: Censys is blocking our requests check your api usage")
            
        except CensysRateLimitExceededException:
            
            
            print(f"[{red}ALERT{reset}]: Censys is blocking our requests check your api usage")
            
            
        except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Censys is blocking our requests ")
    
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Censys")
        
            return
        
#fullhunt api 

def api_fullhunt(domain,filename):
    
    try:
        
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            fullhunt_key = random.choice(data.get("Fullhunt", []))
            
            
            if fullhunt_key is None :
            
                        print(f"[{red}ALERT{reset}]: There is no api keys found for Fullhunt.io api ")
                        
                        return 
            
            else:
            
                        pass
                    
        
                    
        try:
            
            url = f"https://fullhunt.io/api/v1/domain/{domain}/subdomains"
            
            headers = {"X-API-KEY": f"{fullhunt_key}"}
            
            with httpx.Client() as requests:

                response = requests.get(url, headers=headers, timeout=10)
                
                data = response.json()
                
                if response.status_code == 200:
                    
                    subdomains = data.get('hosts', [])
                    
                    for subdomain in subdomains:
                        
                        subdomains_list.append(subdomain)
                        
                    
                elif response.status_code == 429:
                    
                    print(f"[{red}ALERT{reset}]: Fullhunt blocking our requests check your api usage {fullhunt_key}")
                    
                else:
                    
                    pass
            
                
                    
        except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Fullhunt blocking our requests")
            
                            
    
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Fullhunt")
        
            return


#netlas works good

def api_netlas(domain, filename):
    
    
    try:
        
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            netlas_key = random.choice(data.get("Netlas", []))
            
            
            if netlas_key is None :
            
                        print(f"[{red}ALERT{reset}]: There is no api keys found for Fullhunt api ")
                        
                        return 
            
            else:
            
                        pass
                    
        try:
            
            url = f"https://app.netlas.io/api/domains/?q=(domain:*.{domain}+AND+NOT+domain:{domain})&host={domain}"          
            
            headers = {
                    "X-API-Key": f"{netlas_key}",
                    }
            
            with httpx.Client() as requests:

                response = requests.get(url, headers=headers, timeout=10)
                
                
                if response.status_code == 200:
                
                    data = response.json()
                
                    for item in data['items']:
                    
                        subdomains = item['data']['domain']
                    
                        subdomains_list.append(subdomains)
                        
                else:
                    
                    print(f"[{red}ALERT{reset}]: Netlas api blocking our request, check your api usage of {netlas_key}  ")
                    
                    
                    
                
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: Netlas blocking our requests")
                
                    
    
    
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Netlas.io")
        
            return

#zoomEYE Auth works good with access token and JWT

def zoom_eye_login(filename):
    
    
    try:
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
        data = random.choice(data.get("Zoomeye-Auth", []))
            
        zoom_username ,zoom_password = data.split(':')
            
            
        if zoom_username is None or zoom_password is None:
            
                        print(f"[{red}ALERT{reset}]: There is no email and password found for Zoomeye api ")
                        
                        return 
            
        else:
            
                        pass 
        
    
        url = "https://api.zoomeye.org/user/login"
        data = {
        "username": zoom_username,
        "password": zoom_password
        }
    
        try:
            
            with httpx.Client() as client:
                response = client.post(url, json=data)
            
                if response.status_code == 200:
                    
                    return response.json().get("access_token")
             
                else:
                
                    print(f"[{red}ALERT{reset}]: Invalid Zoomeye login credentials Please check the Zoomeye email or password is correct")
                    
                    
                    return None
                
        except Exception as e:
            
            
            print(f"[{red}ALERT{reset}]: Zoomeye login blocking our requests")
            
    except Exception as e:
        print(f"[{red}ALERT{reset}]: Please check your configuration file and values for Zoomeye API email and password")
        return 
                


def api_zoomeye_jwt(domain,token):
    
                    
        try:
            zoom_jwt = token
            
            current_page = 2
            
            
            url=f"https://api.zoomeye.org/domain/search?q={domain}&type=1&page={current_page}"
            
            headers = {
    "Authorization": f"JWT {zoom_jwt}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
            
            
            with httpx.Client() as requests:

                response = requests.get(url, headers=headers)
                
                data = response.json()
                
                if response.status_code == 200:
                
                    for item in data['list']:
                        
                        subdomains_list.append(item['name'])
                    
                elif response.status_code == 429:
                    
                    print(f"[{red}ALERT{reset}]: Zoomeye JWT blocking our requests")
                    
                elif response.status_code == 401:
                    
                    print(f"[{red}ALERT{reset}]: Unauthorized Zoomeye JWT key please check your accesstoken")
                    
                    pass
                
                else:
                    
                    
                    print(f"[{red}ALERT{reset}]: Zoomeye JWT blocking our requests check your api usage ")
                    
                    pass
                    
                    
                
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: Zoomeye JWT blocking our requests")
                
                    
#zoom eye api works good

def api_zoomeye(domain, filename):
    
    try:
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            zoom_key = random.choice(data.get("Zoomeye-API", []))

            if zoom_key is None:
                
                print("[ALERT]: There is no API key found for Zoomeye API")
                
                return
            else:
                pass

        try:
            
            current_page = 1

            while True:
                
                url = f"https://api.zoomeye.org/domain/search?q={domain}&type=1&s=1000&page={current_page}"
                
                headers = {
                    "API-KEY": f"{zoom_key}",
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }

                with httpx.Client() as requests:
                    
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    data = response.json()
                    

                    if response.status_code == 200:
                        
                        for item in data["list"]:
                            
                            if "API count exceeded - Increase Quota with Membership" in  item:
                                
                                pass
                            
                            else:
                                
                            
                                subdomains_list.append(item["name"])

                        # Check if there are more pages
                        if data["total"] > current_page * data["size"]:
                            
                            current_page += 1
                        else:
                            
                            break
                        
                    elif response.status_code == 429:
                        
                        print(f"[{red}ALERT{reset}]: Zoomeye api blocking our requests, check your API usage {zoom_key}")
                        
                        break
                    
                    elif response.status_code == 401:
                        
                        print(f"[{red}ALERT{reset}]: Unauthorized Zoomeye API key, please check your API key {zoom_key}")
                        
                        break
                    
                    else:
                        print(f"[{red}ALERT{reset}]: Zoomeye api blocking our requests, check your API usage {zoom_key}")
                        
                        break

        except Exception as e:
            
            pass 
        
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Please check your configuration file and values for Zoomeye API")
        
        return


#new integ


def api_redhunt(domain, filepath):
    
    try:
        
        with open(filepath, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            redhunt_key = random.choice(data.get("Redhunt", []))

            if redhunt_key is None:
                
                print("[ALERT]: There is no API key found for Redhunt API")
                
                return
            else:
                pass
    
        page_number = 1
    
        while True:
        
            page_subdomains = send_request(domain,redhunt_key,page_number)
        
            if not page_subdomains:
            
                break
        
            subdomains_list.extend(page_subdomains)
    
            page_number += 1
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values fo Redhunt api")
        
        return
    
def send_request(domain, api_key, page_number):
    
    page_size = 1000
    
    url = f"https://reconapi.redhuntlabs.com/community/v1/domains/subdomains?domain={domain}&page_size={page_size}&page={page_number}"
    
    headers = {
        "X-BLOBR-KEY": api_key
    }
    
    with httpx.Client() as requests:
        
        response =  requests.get(url, headers=headers, timeout=10)
        
    data = response.json()
        
    if response.status_code == 200:
        
        
        
        if 'subdomains' in data:
            
            return data['subdomains']
            
            
        
        else:
            
            pass
        
    elif response.status_code ==  403 or "The limit has been reached for this product, please contact your data provider" in data :
        
        
        print(f"[{red}ALERT{reset}]: Redhunt api blocking our requests Check your api usage: {api_key}")
        
    elif response.status_code == 404 or 'No data product found. Please contact your data provider' in data:
        
        print(f"[{red}ALERT{reset}]: Check that you have subscriber to Redhunt api free access for this api key: {api_key}")
        
    else:
        
        pass
    





#======================================================Notifier==============================================================================================================

#notify works good

def notify(domain,filename):
    
    
    try:
        
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            push_key = random.choice(data.get("Pushbullet-Notify", []))
            
            
            if push_key is None :
            
                        print(f"[{red}ALERT{reset}]: There is no api keys found for Notification, Subdominator will not send any notification")
                        
                        return 
            
            else:
            
                        pass
                    
        try:
            
            url = f'https://api.pushbullet.com/v2/pushes'          
            
            headers = {
            'Access-Token': push_key,
            
            'Content-Type': 'application/json'
            }
            data = {
            'type': 'note',
            'title': f"Subdominator Task Alert",
            'body': f"Subdominator completed to enumerate subdomains for {domain}"
            }
            
            try:
                
                with httpx.Client() as client:
                
                    response = client.post(url, json=data, headers=headers)
                
                    response.raise_for_status()
                
                    print(f'[{blue}INFO{reset}]:Notification sent successfully!')
                    
            except httpx.HTTPError as e:
                
                    print(f'Error occured when sending notification to you')
                    
                    
                    
                
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: PushBullet blocking our requests to send notification to you")
                
                    
    
    
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Pushbullet-notify")
        
            return

#=============================================================================NON API Start=================================================================================================

# alienvault recu

def alien_api(domain):
    
    try:
    
        url = f"https://otx.alienvault.com/api/v1/indicators/hostname/{domain}/passive_dns"
        
        headers = {
            "Authorization": "c8e97cc74172274aa6c258fe844d81f47b4a2cddfd475626c7ea63c6015d0623"
        }
    
        with httpx.Client() as request:
        
            response = request.get(url, headers=headers, timeout=15)
        
        
            if response.status_code == 200:
        
                data = response.json()
        
                pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
            
                for entries in data['passive_dns']:
                
                    subdomain = entries['hostname']
                
                    if not pattern.match(subdomain):
                        
                        if subdomain.endswith(domain):
                    
                            subdomains_list.append(subdomain)
                    
                    else:
                    
                        pass
                
            else:
            
                pass
            
    except httpx.ReadTimeout:
        
        pass
    
    except httpx.RequestError as e:
        
        pass
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Alienvault Blocking our request")

#new Integ:

def subdomain_center(domain):
    
    try:
    
        url = f"https://api.subdomain.center/?domain={domain}"
    
        with httpx.Client() as request:
        
            response = request.get(url, timeout=10)
        
        
            if response.status_code == 200:
        
                data = response.json()
        
                for subdomain in data:
        
                    subdomains_list.append(subdomain)

                
            else:
            
                pass
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Subdomain Center Blocking our requests")

#new Integ

def columbus_center(domain):
    
    try:
    
        url = f"https://columbus.elmasy.com/api/lookup/{domain}?days=-1"
    
        with httpx.Client() as request:
        
            response = request.get(url, timeout=15)
        
        
            if response.status_code == 200:
        
                data = response.json()
        
                for subdomain in data:
        
                    subdomains_list.append(f"{subdomain}.{domain}")

                
            else:
            
                pass
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Columbus api Blocking our requests")
        
#anubis

def anubis(domain):
    
    try:
    
        url = f"https://jonlu.ca/anubis/subdomains/{domain}"
    
        with httpx.Client() as request:
        
            response = request.get(url)
        
        
            if response.status_code == 200:
        
                data = response.json()
        
                for subdomain in data:
        
                    subdomains_list.append(subdomain)
                
            else:
            
                pass
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Anubis Blocking our request ")
        
#dnsrepo

def dnsrepo(domain):
    
    try:
        url = f"https://dnsrepo.noc.org/?domain={domain}"
        
        with httpx.Client() as requests:
            
            response = requests.get(url, timeout=10)
            
        if response.status_code == 200:
                        
                content =  response.text
                        
                subdomains_pattern = re.compile(rf"\b[a-zA-Z0-9]+\b\.{domain}\b")
                        
                subdomains = subdomains_pattern.findall(content)
                        
                for subdomain in subdomains:
            
                    subdomains_list.append(subdomain)
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Dnsrepo is blocking our requests")
        
        
#hacktarg

def hackertarget(domain):

            try:
                url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
                
                with httpx.Client() as requests:
                    
                    response = requests.get(url, timeout=10)
                    
                    data = response.text

                if response.status_code == 200:
                    
                    subdomains = data.splitlines()
                    
                    for subdomain in subdomains:
                        
                        if "API count exceeded - Increase Quota with Membership" in subdomain:
            
                            pass
                        
                        else:
                        
                            subdomain = subdomain.split(",")[0]
                        
                            subdomains_list.append(subdomain)
                else:
                    
                    pass 
                    
            except Exception as e:
                
                print(f"[{red}ALERT{reset}]: Hackertarget Blocking our requests")
                

#rapidns

def new_rapidns(domain):
    
    try:
        
        url = f"https://rapiddns.io/subdomain/{domain}?full=1"
        
        
        with httpx.Client() as requests:

            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                        
                content =  response.text
                        
                subdomains_pattern = re.compile(rf"\b[a-zA-Z0-9]+\b\.{domain}\b")
                        
                subdomains = subdomains_pattern.findall(content)
                        
                for subdomain in subdomains:
            
                    subdomains_list.append(subdomain)
                
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: RapidAns is blocking our requests may be because of firewall")

#urlscan

def urlscan_api(domain):
    try:
        with httpx.Client() as requests:
            
            response =requests.get(f'https://urlscan.io/api/v1/search/?q=page.domain:{domain}&size=10000', timeout=10)
            
            if response.status_code == 200:
                
            
               data = response.json()
            
               for domain in data['results']:
            
                subdomain = domain['page']['domain']

            
                subdomains_list.append(subdomain)
            
    except Exception as e:
        
        print(f'[{red}ALERT{reset}]: Urlscan Blocking our requests')
        
        return 

#wayback

def wayback(domain):
    
    try:
        url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=txt&fl=original&collapse=urlkey"
        
        with httpx.Client() as requests:
            
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                
                pattern = f"https://([\w-]+\.{domain})"
            
                subdomains = re.findall(pattern, response.text)
            
                for subdomain in subdomains:
                
                    subdomains_list.append(subdomain)               
            else:
            
                pass 
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Wayback blocking our request ")
        
#seckdr

def non_api_seckdr(domain):
    
    url = 'https://seckrd.com/subdomain-finder.php'
    
    headers = {

    'User-Agent': 'Mozilla/5.0 (X11; subdominatorOS x86_64; rv:102.0) Gecko/20100101 Firefox/100.0',
    'Accept-Language': 'en-US,en;q=0.5',
}
    
    data = {
    'domain': domain,
    'submit': ''
}
    try:
        
        with httpx.Client() as requests:
        
            response = requests.post(url,headers=headers,data=data, timeout=10)
        
        
        if response.status_code == 200:
            
            pattern = f"https://([\w-]+\.{domain})"
            
            subdomains = re.findall(pattern, response.text)
            
            for subdomain in subdomains:
                
                subdomains_list.append(subdomain)
                
        else:
            
            print(response.status_code)
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Seckdr blocking our request ")
        
        
#crtsh

def crtsh(domain):
    
    try:

        url = f"https://crt.sh/?q=%25.{domain}"

        response = requests.get(url)

        if response.status_code == 200:

            data = response.text

            pattern = rf"\b[a-zA-Z0-9.*-]+\.{re.escape(domain)}\b"

            subdomain_pattern = re.compile(pattern)


            subdomains = subdomain_pattern.findall(data)
            
            for subdomain in subdomains:
                
                subdomains_list.append(subdomain)

        else:
            
            pass  
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Crtsh blocking our requests")
        
        
def non_api_c99(domain):
    
    try:
        today = datetime.date.today()


        yesterday = today - datetime.timedelta(days=1)

        url = f"https://subdomainfinder.c99.nl/scans/{yesterday}/{domain}"

        response = requests.get(url)

        try:
            
            if response.status_code == 200:
            
                content = response.text

                subdomain_pattern = re.compile(rf"\b[a-zA-Z0-9]+\b\.{domain}\b")

                subdomains = subdomain_pattern.findall(content)

                for subdomain in subdomains:
                    
                    subdomains_list.append(subdomain)
                    
            else:
                
                pass
                
        except requests.exceptions.RequestException as e:
            
                print(f"[{red}ALERT{reset}]: C99 is blocking our requests")
    
    except Exception as e:
        
                print(f"[{red}ALERT{reset}]: C99 is blocking our requests")
        
#============================================calling api===========================================================================================================================


def api(domain,  filepath):
    
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        
        
        futures = [executor.submit(api_virustotal, domain, filepath),
                  executor.submit(api_chaos, domain, filepath),
                  executor.submit(whoisxml_api, domain, filepath),
                  executor.submit(api_securitytrails, domain, filepath),
                  executor.submit(api_bevigil, domain, filepath),
                  executor.submit(api_bufferover, domain, filepath),
                  executor.submit(send_binaryedge, domain, filepath),
                  executor.submit(api_certspoter, domain, filepath),
                  executor.submit(rapid_whois, domain, filepath),
                  executor.submit(non_api_dnsdump, domain, filepath),
                  executor.submit(api_leakix, domain, filepath),
                  executor.submit(api_censys, domain, filepath),
                  executor.submit(api_fullhunt, domain, filepath),
                  executor.submit(api_netlas, domain, filepath),
                  executor.submit(api_zoomeye, domain, filepath),
                  executor.submit(api_redhunt, domain, filepath),
                  executor.submit(crtsh,domain), 
                   executor.submit(non_api_c99,domain),
                   executor.submit(non_api_seckdr,domain),
                   executor.submit(wayback,domain),
                   executor.submit(urlscan_api,domain),
                   executor.submit(new_rapidns,domain),
                   executor.submit(subdomain_center,domain),
                   executor.submit(columbus_center,domain),
                   executor.submit(hackertarget,domain),
                   executor.submit(dnsrepo,domain),
                   executor.submit(alien_api,domain),
                   executor.submit(anubis,domain)]
        
    
    concurrent.futures.wait(futures)
    
    token = zoom_eye_login(filepath)
    
    api_zoomeye_jwt(domain,token)
    
    if args.recursive:
        
        print(f"[{green}INFO{reset}]: Subdominator recursion module initiated")
        
        
        wild_cards = []
        
        
        for domain in subdomains_list:
            
            if domain.startswith("*.") and domain.endswith(domain):
                
                if domain not in wild_cards:
                
                    wild_cards.append(domain)
                
                
        print(f"[{blue}INFO{reset}]: Total wildcard loaded for recursive enumeration: {len(wild_cards)}")
            
            
        
        for domain in wild_cards:
        
            if domain.startswith("*.") and domain.endswith(domain):
                
                subdomain = domain[2:]
                
                
                print(f"[{green}INFO{reset}]: Recursive enumeration running for {domain}")
                
                
            
                recursive(subdomain)
                
        
            else:
                
                pass
            
        if args.domain:
            
            single_unique_subdomains(subdomains_list)
            
        elif args.domains_list:
            
            
            list_unique_subdomains(subdomains_list)
            
    elif not args.recursive:
        
        if args.domain:
            
            single_unique_subdomains(subdomains_list)
            
        elif args.domains_list:
            
            list_unique_subdomains(subdomains_list)
                
    
    
def non_api(domain):
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        
        futures = [executor.submit(crtsh,domain), 
                   executor.submit(non_api_c99,domain),
                   executor.submit(non_api_seckdr,domain),
                   executor.submit(wayback,domain),
                   executor.submit(urlscan_api,domain),
                   executor.submit(new_rapidns,domain),
                   executor.submit(subdomain_center,domain),
                   executor.submit(columbus_center,domain),
                   executor.submit(hackertarget,domain),
                   executor.submit(dnsrepo,domain),
                   executor.submit(alien_api,domain),
                   executor.submit(anubis,domain)]
        
        concurrent.futures.wait(futures)
    
    if args.recursive:
        
        print(f"[{green}INFO{reset}]: Subdominator recursion module initiated")
        
        wild_cards = []
        
        
        for domain in subdomains_list:
            
            if domain.startswith("*.") and domain.endswith(domain):
                
                if domain not in wild_cards:
                
                    wild_cards.append(domain)
                
                
        print(f"[{blue}INFO{reset}]: Total wildcard loaded for recursive enumeration: {len(wild_cards)}")
        
        
        
        for domain in wild_cards:
        
            if domain.startswith("*.") and domain.endswith(domain):
                
                
                subdomain = domain[2:]
                
                print(f"[{green}INFO{reset}]: Recursive enumeration running for {domain}")
            
                recursive(subdomain)
                
                
        
            else:
                
                pass
            
        if args.domain:
            
            single_unique_subdomains(subdomains_list)
            
        elif args.domains_list:
            
            
            list_unique_subdomains(subdomains_list)
            
    elif not args.recursive:
        
        if args.domain:
            
            single_unique_subdomains(subdomains_list)
            
        elif args.domains_list:
            
            list_unique_subdomains(subdomains_list)

def recursive(domain):
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        
        futures = [executor.submit(crtsh,domain),
                   executor.submit(alien_api,domain),
                   executor.submit(anubis,domain),
                   executor.submit(non_api_seckdr,domain),
                   executor.submit(urlscan_api,domain),
                   executor.submit(wayback,domain)]
        
        concurrent.futures.wait(futures)

#main function to check arguments and do it process
def main():
    
    
    printed = False
    
    version = False
    
    if args.domain and args.domains_list:
        
        if not printed:
        
            print(f"{random_color}{banner}{reset}")
            
            printed = True
        
        print(f"[{red}ALERT{reset}]: Please provide either --domain flag or --domains-list flag for Subdominator to find subdomains")
        
        exit()
    
        
    if args.version and not args.domain or args.domains_list:
        
        if not printed:
        
            print(f"{random_color}{banner}{reset}")
            
            printed = True
            
        if not version:
        
            check_version()
            
            version = True
        
    if not args.version:
        
        pass
        
    
    if args.domain and args.config:
        
        if not printed:
        
            print(f"{random_color}{banner}{reset}")
            
            printed = True
        
        if not version:
        
            check_version()
            
            version = True
        
        print(f"[{blue}INFO{reset}]: Started to collecting the subdomains for: {args.domain}")
        
        
        print(f"[{green}INFO{reset}]: Subdominator config mode enabled")
        
        
        print(f"[{blue}INFO{reset}]: Sudominator🔥 Swtiched to Config mode using full resources to enumerate subdomains !")
        
        
        if args.output:
            
            print(f"[{green}INFO{reset}]: Output will be saved in the {args.output} file")
            
        if not output:
            
            print(f"[{red}ALERT{reset}]: Output file not given by user. Subdominator will save the output in {args.domain}.subdomains.txt file")
            
        if args.recursive:
            
            print(f"[{green}INFO{reset}]: Subdominator recursive mode enabled")
            
        elif not args.recursive:
            
            print(f"[{blue}INFO{reset}]: Subdominator recursive mode disabled")
            
        if args.notify:
            
            print(f"[{green}INFO{reset}]: Subdominator Notifier enabled")
            
        elif not args.notify:
            
            print(f"[{blue}INFO{reset}]: Subdominator Notifier disabled")
            
        
        filename = check_config_file()
        
        domain = args.domain
        
        api(domain,filename)
        
        if args.notify:
            
            notify(domain,filename)
            
            notification.notify(
            title = "Subdominator",
            message=f"Subdominator completed subdomain enumeration {domain}" ,
            timeout=5
)
            
        elif not args.notify:
            
            pass
        
    elif args.domain:
        
        if not printed:
        
            print(f"{random_color}{banner}{reset}")
            
            printed = True
        
        if not version:
        
            check_version()
            
            version = True
        
        print(f"[{blue}INFO{reset}]: Started to collecting the subdomains for: {args.domain}")
        
        
        print(f"[{blue}INFO{reset}]: Subdominator config mode disabled 🙁")
        
        
        print(f"[{blue}INFO{reset}]: Subdominator swtiching to OSINT 💀 mode, due to config mode disabled")
        
        
        if args.output:
            
            print(f"[{green}INFO{reset}]: Output will be saved in the {args.output} file")
            
        if not args.output:
            
            print(f"[{red}ALERT{reset}]: Output file not given by user. Subdominator will save the output in {args.domain}.subdomains.txt file")
            
        if args.recursive:
            
            print(f"[{green}INFO{reset}]: Subdominator recursive mode enabled")
            
        elif not args.recursive:
            
            print(f"[{blue}INFO{reset}]: Subdominator recursive mode disabled")
            
        if args.notify:
            
            print(f"[{green}INFO{reset}]: Subdominator Notifier enabled")
            
            
            filename = check_config_file()
            
        elif not args.notify:
            
            print(f"[{blue}INFO{reset}]: Subdominator Notifier disabled")
        
        domain = args.domain     
            
        non_api(domain)
        
        if args.notify:
            
            notify(domain,filename)
            
            notification.notify(
            title = "Subdominator",
            message=f"Subdominator completed subdomain enumeration {domain}" ,
        
            timeout=5
)
            
        elif not args.notify:
            
            pass
        
    
    if args.domains_list and args.config:
        
        if not printed:
        
            print(f"{random_color}{banner}{reset}")
            
            printed = True
        
        if not version:
        
            check_version()
            
            version = True
        
        print(f"[{blue}INFO{reset}]: Started to collecting the subdomains from the {args.domains_list} file")
    
        
        print(f"[{green}INFO{reset}]: Subdominator config mode enabled")
        
        
        print(f"[{blue}INFO{reset}]: Sudominator🔥 Swtiched to Config mode using full resources to enumerate subdomains !")
        
        
        if args.output:
            
            print(f"[{green}INFO{reset}]: Output will be saved in the {args.output} file")
            
        if not args.output:
            
            print(f"[{red}ALERT{reset}]: Output file not given by user. Subdominator will save the output in {args.domain}.subdomains.txt file")
            
        if args.recursive:
            
            print(f"[{green}INFO{reset}]: Subdominator recursive mode enabled")
            
        elif not args.recursive:
            
            print(f"[{blue}INFO{reset}]: Subdominator recursive mode disabled")
            
        if args.notify:
            
            print(f"[{green}INFO{reset}]: Subdominator Notifier enabled")
            
        elif not args.notify:
            
            print(f"[{blue}INFO{reset}]: Subdominator Notifier disabled")
            
        
        filename = check_config_file()
        
        try:
            
            with open(list, "r") as d:
                
                domains = d.read().splitlines()
                
                
            for domain in domains:
                
                print(f"[{blue}INFO{reset}]: Started to collecting the subdomains for {domain}")
        
                api(domain,filename)
                
                if args.notify:
            
                        notify(domain,filename)
                        
                        notification.notify(
            title = "Subdominator",
            message=f"Subdominator completed subdomain enumeration {domain}" ,
           
            # displaying time
            timeout=5
)
            
                elif not args.notify:
            
                    pass
                
                
                
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: Provided {args.domains_list} file not found, Please check the path of file or the file name")
            
            exit()
            
    elif args.domains_list and not args.config:
        
        if not printed:
        
            print(f"{random_color}{banner}{reset}")
            
            printed = True
        
        if not version:
        
            check_version()
            
            version = True
        
        print(f"[{blue}INFO{reset}]: Started to collecting the subdomains from the {args.domains_list} file")
        
        
        print(f"[{blue}INFO{reset}]: Subdominator config mode disabled 🙁")
        
        
        print(f"[{blue}INFO{reset}]: Subdominator swtiching to OSINT 💀 mode, due to config mode disabled")
        
        
        
        if args.output:
            
            print(f"[{green}INFO{reset}]: Output will be saved in the {args.output} file")
            
        if not args.output:
            
            print(f"[{red}ALERT{reset}]: Output file not given by user. Subdominator will save the output in {args.domain}.subdomains.txt file")
            
        if args.recursive:
            
            print(f"[{green}INFO{reset}]: Subdominator recursive mode enabled")
            
        elif not args.recursive:
            
            print(f"[{blue}INFO{reset}]: Subdominator recursive mode disabled")
            
        if args.notify:
            
            print(f"[{green}INFO{reset}]: Subdominator Notifier enabled")
            
        elif not args.notify:
            
            print(f"[{blue}INFO{reset}]: Subdominator Notifier disabled")
            
        
        filename = check_config_file()
        
        try:
            
            with open(list, "r") as d:
                
                domains = d.read().splitlines()
                
                
            for domain in domains:
                
                print(f"[{blue}INFO{reset}]: Started to collecting the subdomains for {domain}")
        
                non_api(domain)
                
                if args.notify:
            
                        notify(domain,filename)
                        
                        notification.notify(
            title = "Subdominator",
            message=f"Subdominator completed subdomain enumeration {domain}" ,
            # displaying time
            timeout=5
)
            
                elif not args.notify:
            
                    pass
                
                
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: Provided {args.domains_list} file not found, Please check the path of file or the file name")
            
            exit()
            
                
        
        

if __name__ == "__main__":
    
    main()




