#!/usr/bin/python3
import httpx
import requests
from colorama import Fore,Back,Style
import argparse
import yaml
import time as t
import re
import random
import datetime
import os
import sys
from censys.search import CensysCerts
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
    

parser = argparse.ArgumentParser(description=f"{cyan}Subdominator Unleash the Power of Subdomain Enumeration{reset}")

parser.add_argument("-d", "--domain", help=f"{blue}[ALERT]:Domain name to find the Subdomains{reset}", type=str, required=True)

parser.add_argument("-cf", "--config", help=f"{green}[INFO]:Load your config API keys to find more Subdomains{reset}", action="store_true")

parser.add_argument("-o", "--output", help=f"{yellow}[INFO]: Filename to save the output", type=str)

args=parser.parse_args()

#Check the latest Version

def version_check():
    
    version = "v1.0.1"
    
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
                
                t.sleep(1)
                
        else:
            
            pass
                
    except Exception as e:
        
        pass
    

#Print ans write the unique subdomains

def unique_subdomains(subdomains):
    
    unique_subdomains = sorted(set(subdomains))
    
    for subdomain in unique_subdomains:
        
        print(f"[{random_color}Subdominator{reset}] {subdomain}")
        
        if args.output:
            
            if os.path.isfile(args.output):
                
                filename = args.output
                
            elif os.path.isdir(args.output):
                
                filename = os.path.join(args.output, f"{args.domain}.subdomains.txt")
                
            else:
                
                filename = args.output
                
        if not args.output:
            
            filename = f"{args.domain}.subdomains.txt"
            
        
        with open(filename, "a") as w:
            
            w.write(subdomain + '\n')
    
    total = len(unique_subdomains)
    
    print(f"[{blue}INFO{reset}]: Total {total} subdomains found")
    
    print(f"[{green}WISH{reset}]: Happy Hacking Hacker ☠️ 🔥 🚀")
    
    
#check the config file exist in user system if run in the other directories

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
    
    

#===============================================================API Calls ===================================================================================================

def api_virustotal(domain, filename):
    
    try:
        
        with open (filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            
                
        virus_key = data["VirusTotal"]["api_key"]
        
        
                
        if virus_key is None:
            
                print(f"[{red}ALERT{reset}]: There is no api key found for VirusTotal ")
                        
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
                            print(f"[{red}ALERT{reset}]: VirusTotal blocking our requests Check your api usage")
                            
                        
                            
                        
                        
                    else:
                        
                        print(f"[{red}ALERT{reset}]: Virustotal blocking our requests")
                        
        except Exception as e:
                    
                    print (f"[{red}Alert{reset}]: Virustotal Blocking our requests")
                
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values fo VirusTotal")
        
            return
               
               
def api_chaos(domain, filename):
    
    try:
        
        with open(filename, "r") as key:
            
            data = yaml.safe_load(key)
            
            try:
                
                chaos_api_key = data['Chaos']['api_key']
                
                if chaos_api_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api key found for Chaos ")
                        
                        return
            
            
                else:
            
                        pass

                url = f"https://dns.projectdiscovery.io/dns/{domain}/subdomains"

                headers= {
                        'Authorization': chaos_api_key
                }
    
                try:
                    
                    with httpx.Client() as requests:
                    
                        response = requests.get(url,headers=headers, timeout=10)

                    if response.status_code == 200:

                            data = response.json()
    
                            if 'subdomains' in data:
                            
                                        subdomains = data['subdomains']
                            
                                        for subdomain in subdomains:
                                
                                                subdomains_list.append(f"{subdomain}.{domain}")
                                                
                            else:
                
                                pass
                            
                            
                    else:
                            
                        print(f"[{red}ALERT{reset}]: Chaos blocking our requests check your api usage ")
            
                except Exception as e:
        
                    print(f"[{red}ALERT{reset}]: Chaos blocking our requests")
                    
            except Exception as e:
                
                print(f"[{red}ALERT{reset}]: There is no api key found for Chaos ") 
                
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Chaos")
        
            return
            
            
        
def whoisxml_api(domain, filename):
    
    try:
        with open(filename, "r") as key:
            
            data = yaml.safe_load(key)
            
        try:
        
            whois_api_key = data ['Whoisxml']['api_key']   
            
            if whois_api_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api key found for whoisxml ")
                        
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
                else:
                                
                        print(f"[{red}ALERT{reset}]: Whoisxmlapi blocking our request check your api usage")
                        
            except Exception as e:
                
                print(f"[{red}ALERT{reset}]: Whoisxmlapi blocking our request")
                
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: There is no api key found for Whoisxmlapi ")
                
        
        
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Whoisxml")
        
            return
            
            

def api_securitytrails(domain, filename):
    
    try:
        
        with open(filename, "r") as key:
            
            data = yaml.safe_load(key)
            
        try:
            
            security_api_key = data ['SecurityTrails']['api_key']
            
            if security_api_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api key found for SecurityTrails ")
                        
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
                
                else:
                    
                    print(f"[{red}ALERT{reset}]: SecurityTrails blocking our request check your api usage")
                    
            except Exception as e:
                
                print(f"[{red}ALERT{reset}]: SecurityTails blocking our request")
                    
                    
            
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: There is no api key found for SecurityTrails ")
            
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of SecurityTrails")
        
            return
            
        
        
def api_bevigil(domain, filename):
    
    try:
        
        with open(filename, "r") as key:
            
            data =  yaml.safe_load(key)
            
        bevigil_api_key = data ['Bevigil']['api_key']
        
        if bevigil_api_key is None:
            
            print(f"[{red}ALERT{reset}]: There is no api key found for Bevigil ")
            
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
                
            else:
                
                print(f"[{red}ALERT{reset}]: Bevigil blocking our request check your api usage")
                
        except Exception as e:
            
            
                    print(f"[{red}ALERT{reset}]: Bevigil blocking our request ")
            
        
        
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Bevigil")
        
            return
            
    
def api_bufferover(domain,filename):
    
    try:
        with open(filename, "r") as key:
            
            data = yaml.safe_load(key)
        
        bufferover_api_key = data['Bufferover']['api_key']
            
        if bufferover_api_key is None:
            
            print(f"[{red}ALERT{reset}]: There is no api key found for Bufferover ")
                        
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
                else:
                    
                    print(f"[{red}ALERT{reset}]: Bufferover blocking our requests check your api usage ")
                    
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: Bufferover blocking our requests")
                    
            
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Bufferover")
            
        
            return
        
        
def api_certspoter(domain, filename):
    
    try:
        
        with open(filename,"r") as keys:
            
            data = yaml.safe_load(keys)
            
        certspotter_api_key = data ['Certspotter']['api_key']
        
        if certspotter_api_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api key found for Certspotter ")
                        
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
                
            else:
                
                print(f"[{red}ALERT{reset}]: Certspotter blocking our requests check your api usage")
                
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: Certspotter blocking our requests")
            
            
            
        
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Certspotter")
            
        
            return
        
        
def rapid_whois(domain, filename):
    
    try :
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
        rapid_api_key = data['Rapidapi']['api_key']
        
        integrated_key = data['Whoisxml']['api_key']
        
        if rapid_api_key is None or integrated_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api keys found for Rapidapi and Whoisxmlapi  ")
                        
                        t.sleep(1)
            
                        print(f"[{red}ALERT{reset}]: Subdominator exiting from execution without api keys cannot execute the config mode! ")
            
                        exit()
            
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
            else:
                
                print (f"[{red}Alert{reset}]: RapidWhois Blocking our requests check your api usage of Rapid and Whoisxml api keys ")
            
        except Exception as e:
            
            print (f"[{red}Alert{reset}]: RapidWhois Blocking our requests")
                    
                    
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Rapidapi and Whoisxml")
            
        
            return
        
        
def non_api_dnsdump(domain, filename):
    
    try:
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            csrf_cookie = data['Dnsdumpter']['csrf_cookie']
            
            csrf_token = data['Dnsdumpter']['csrf_token']
            
            if csrf_cookie is None or csrf_token is None:
                
                print(f"[{red}ALERT{reset}]: There is no csrf token or csrf cookie found for the DnsDump  ")
                        
                t.sleep(1)
            
                print(f"[{red}ALERT{reset}]: Subdominator exiting from execution without api keys cannot execute the config mode! ")
            
                exit()
            
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
                    
                        response = requests.post(url, headers=headers, data=data)
                    
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


def api_leakix(domain, filename):
    
    
    try:
        
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            leakix_key = data ["Leakix"]['api_key']
            
            
            if leakix_key is None :
            
                        print(f"[{red}ALERT{reset}]: There is no api key found for leakix api ")
                        
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
                    
                    print(f"[{red}ALERT{reset}]: Leakix blocking our requests check your api usage")
                    
                    
                
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: Leakix blocking our requests")
                
                    
    
    
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Leakix")
        
            return
        
def api_censys(domain,file_path):
    
    try:
        
        filename = file_path
        
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            censys_id = data["Censys"]['api_secret_id']
            
            censys_key = data['Censys']['api_secret_key']
            
            if censys_id is None or censys_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api key or api secret id found for Censys api ")
                        
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
            
            print(f"[{red}ALERT{reset}]: Invalid credentials for your Censys api credentials")
            
        except CensysRateLimitExceededException:
            
            
            print(f"[{red}ALERT{reset}]: Censys is blocking our requests check your api usage")
            
            
        except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Censys is blocking our requests ")
    
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Censys")
        
            return
        

def api_fullhunt(domain,filename):
    
    try:
        
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            fullhunt_key = data ["Fullhunt"]['api_key']
            
            
            if fullhunt_key is None :
            
                        print(f"[{red}ALERT{reset}]: There is no api key found for Fullhunt.io api ")
                        
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
                    
                    print(f"[{red}ALERT{reset}]: Fullhunt blocking our requests check your api usage")
                    
                else:
                    
                    pass
            
            
                    
                    
                
                
                    
        except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Fullhunt blocking our requests")
            
                            
    
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Fullhunt")
        
            return
    
def api_netlas(domain, filename):
    
    
    try:
        
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            netlas_key = data ["Netlas"]['api_key']
            
            
            if netlas_key is None :
            
                        print(f"[{red}ALERT{reset}]: There is no api key found for Fullhunt.io api ")
                        
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
                
                data = response.json()
                
                for item in data['items']:
                    
                    subdomains = item['data']['domain']
                    
                    subdomains_list.append(subdomains)
                    
                    
                
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: Netlas blocking our requests")
                
                    
    
    
    except Exception as e:
        
            print(f"[{red}ALERT{reset}]: Please Check that You didnt messed up the Cofiguration files variables and it Values of Netlas.io")
        
            return
        
        
def api_zoomeye(domain, filename):
    try:
        with open(filename, "r") as keys:
            data = yaml.safe_load(keys)
            zoom_key = data["Zoomeye"]["api_key"]

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
                            subdomains_list.append(item["name"])

                        # Check if there are more pages
                        if data["total"] > current_page * data["size"]:
                            current_page += 1
                        else:
                            break
                    elif response.status_code == 429:
                        print(f"[{red}ALERT{reset}]: Zoomeye api blocking our requests, check your API usage")
                        break
                    elif response.status_code == 401:
                        print(f"[{red}ALERT{reset}]: Unauthorized Zoomeye API key, please check your API key")
                        break
                    else:
                        print(f"[{red}ALERT{reset}]: Zoomeye api blocking our requests, check your API usage")
                        break

        except Exception as e:
            
            pass


    except Exception as e:
        print(f"[{red}ALERT{reset}]: Please check your configuration file and values for Zoomeye API")
        return

        
        
def zoom_eye_login(filename):
    
    
    try:
        
        with open(filename, "r") as keys:
            
            data = yaml.safe_load(keys)
            
            zoom_username = data ["Zoomeye"]['email']
            
            zoom_password = data ["Zoomeye"]['password']
            
            
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
                    
                    print(f"[{red}ALERT{reset}]: Zoomeye JWT blocking our requests check your api usage")
                    
                elif response.status_code == 401:
                    
                    print(f"[{red}ALERT{reset}]: Unauthorized Zoomeye JWT key please check your accesstoken")
                    pass
                else:
                    
                    
                    print(f"[{red}ALERT{reset}]: Zoomeye JWT blocking our requests check your api usage ")
                    pass
                    
                    
                
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: Zoomeye JWT blocking our requests ")
                
                    


#====================================================================API Call ends====================================================================================================




#==================================================================Non api calls============================================================================================



def non_api_alienvault(domain):  
    
    try:
        url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
        
        
        with httpx.Client() as requests:
        
            response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            
            data = response.json()
            
            #samplet pattern matches and extract data in if block
            
            pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
            
            for entries in data['passive_dns']:
                
                subdomain = entries['hostname']
                
                if not pattern.match(subdomain):
                    
                    subdomains_list.append(subdomain)
                    
                else:
                    
                    pass
                    
    except Exception as e:
        
        print(f"[{red}ALERT{reset}] AlienVault blocking our requests something went wrong with AlienVault")
        
        
def crtsh(domain):
    
    try:

        url = f"https://crt.sh/?q=%25.{domain}"

        response = requests.get(url)

        if response.status_code == 200:
        
            data = response.text
        
            subdomain_pattern = re.compile(rf"\b[a-zA-Z0-9]+\b\.{domain}\b")

            subdomains = subdomain_pattern.findall(data)
            
            for subdomain in subdomains:
                
                subdomains_list.append(subdomain)

        else:
            
            print(f"[{red}ALERT{reset}]: Crtsh blocking our requests")
            
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

        #sample pattern to match
                subdomain_pattern = re.compile(rf"\b[a-zA-Z0-9]+\b\.{domain}\b")

                subdomains = subdomain_pattern.findall(content)

                for subdomain in subdomains:
                    
                    subdomains_list.append(subdomain)
                    
            else:
                
                print(f"[{red}ALERT{reset}]: C99 is blocking our requests")
                
        except requests.exceptions.RequestException as e:
            
                print(f"[{red}ALERT{reset}]: C99 is blocking our requests")
    
    except requests.exceptions.RequestException as e:
        
                print(f"[{red}ALERT{reset}]: C99 is blocking our requests")

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
            print(f"[{red}ALERT{reset}]: Seckdr blocking our request something went wrong with Seckdr")
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Seckdr blocking our request ")
        
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
            
                print(f"[{red}ALERT{reset}]: Wayback blocking our request something went wrong with Wayback")
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Wayback blocking our request ")
        
        
        
def urlscan_api(hostname):
    try:
        with httpx.Client() as requests:
            
            response =requests.get('https://urlscan.io/api/v1/search/', params={'q': f'page.domain:{hostname}', 'size': 10000})
            
            data = response.json()
            
        for domain in data['results']:
            
            subdomain = domain['page']['domain']

            
            subdomains_list.append(subdomain)
            
    except Exception as e:
        print(f'[{red}ALERT{reset}]: Urlscan Blocking our requests')
        
        return 

def rapidns(domain):
    
    try:
        
        url = f"https://rapiddns.io/subdomain/{domain}#result"

        response = requests.get(url, timeout=10)

        if response.status_code == 200:
                        
            content =  response.text
                        
            subdomains_pattern = re.compile(rf"\b[a-zA-Z0-9]+\b\.{domain}\b")
                        
            subdomains = subdomains_pattern.findall(content)
                        
            for subdomain in subdomains:
            
                subdomains_list.append(subdomain)
                
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Rapidns is blocking our requests")


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
        
        print(f"[{red}ALERT{reset}]: RapidAns is blocking our requests may because of firewall")


def hackertarget(domain):

            try:
                url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
                
                with httpx.Client() as requests:
                    
                    response = requests.get(url, timeout=10)
                    data = response.text

                if response.status_code == 200:
                    subdomains = data.splitlines()
                    for subdomain in subdomains:
                        
                        subdomain = subdomain.split(",")[0]
                        
                        subdomains_list.append(subdomain)
                else:
                    print(f"[{red}ALERT{reset}]: Hackertarget Blocking our requests")
            except Exception as e:
                print(f"[{red}ALERT{reset}]: Hackertarget Blocking our requests")
                

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


def non_anubis(domain):
    
    try:
    
        url = f"https://jonlu.ca/anubis/subdomains/{domain}"
    
        with httpx.Client() as request:
        
            response = request.get(url)
        
        
            if response.status_code == 200:
        
                data = response.json()
        
                for subdomain in data:
        
                    subdomains_list.append(subdomain)
                
            else:
            
                print(f"[{red}ALERT{reset}]: Anubis Blocking our request ")
            
                pass
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Anubis Blocking our request ")

#=====================================================================Non api ends=========================================================================================





def api(domain,  filepath):
    
    api_virustotal(domain, filepath)   
    
    api_chaos(domain,filepath)    
    
    whoisxml_api(domain,filepath) 
    
    api_securitytrails(domain,filepath) 
    
    api_bevigil(domain,filepath) 
    
    api_bufferover(domain, filepath) 
    
    api_certspoter(domain, filepath) 
    
    rapid_whois(domain, filepath)  
    
    non_api_dnsdump(domain, filepath) 
    
    api_leakix(domain,filepath) 
    
    api_censys(domain, filepath) 
    
    api_fullhunt(domain, filepath) 
    
    api_netlas(domain,filepath)
    
    api_zoomeye(domain, filepath)
    
    token = zoom_eye_login(filepath)
    
    api_zoomeye_jwt(domain,token)
    
    non_api_alienvault(domain) 
    
    crtsh(domain) 
    
    non_api_c99(domain)
    
    non_api_seckdr(domain)
    
    wayback(domain)
    
    urlscan_api(domain)
    
    rapidns(domain)
    
    new_rapidns(domain)
    
    hackertarget(domain)
    
    dnsrepo(domain)
    
    non_anubis(domain)
    
    unique_subdomains(subdomains_list) 
    
    
def non_api(domain):
    
    non_api_alienvault(domain) 
    
    crtsh(domain) 
    
    non_api_c99(domain)
    
    non_api_seckdr(domain)
    
    wayback(domain)
    
    urlscan_api(domain)
    
    rapidns(domain)
    
    new_rapidns(domain)
    
    hackertarget(domain)
    
    dnsrepo(domain)
    
    non_anubis(domain)
    
    unique_subdomains(subdomains_list)
    
    


#==================================================Call of api ends========================================================================================================





def main():
    
    domain = args.domain
        
    if args.domain and args.config:
        
        print(f"{random_color}{banner}{reset}")
        
        version_check()
        
        print(f"[{blue}INFO{reset}]: Started to collecting the subdomains for: {args.domain}")
        
        t.sleep(1)
        
        print(f"[{green}INFO{reset}]: User Enabled config mode")
        
        t.sleep(1)
        
        print(f"[{blue}INFO{reset}]: Sudominator 🔥 will collect more subdomains than non-config mode when enabling the config mode!")
        
        t.sleep(1)
         
        if args.output:
            
            print(f"[{green}INFO{reset}]: Output will be saved in the {args.output} file")
            
        if not args:
            
            print(f"[{red}ALERT{reset}]: Output file not given by user. Subdominator will save the output in {domain}.subdomains.txt file")
         
        
        filename = check_config_file()
        
        api(domain,filename)
        
        
    elif args.domain and not args.config:
        
        print(f"{random_color}{banner}{reset}")
    
        domain =  args.domain
    
        version_check()
        
        print(f"[{red}ALERT{reset}]: User not enabled the config mode")
    
        t.sleep(3)
    
        print(f"[{green}INFO{reset}]: Dont worry User! Subdominator continuing with the non-config mode :)")
    
    
        t.sleep(1)
    
        print(f"[{blue}INFO{reset}]: Started to collecting the subdomains for: {domain}")
        
        if args.output:
            
            print(f"[{green}INFO{reset}]: Output will be saved in the {args.output} file")
            
        else:
            
            print(f"[{red}ALERT{reset}]: Output file not given by user. Subdominator will save the output in {domain}.subdomains.txt file")
        
        non_api(domain)
        
    elif not args.domain:
    
        print(f"[{red}ALERT{reset}]: No domain in is given to gather subdomains")
    
        exit()
        
    else:
        
        print(f"[{red}ALERT{reset}]: Something went wrong with Subdominator may be User didnt pass the right arguments if the error came continously report your issues in Subdominator github issues")
    
        exit()
    
    
    
    
    
if __name__ == "__main__":
    
    main()
    
    