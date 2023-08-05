#!/usr/bin/python3
import requests
from colorama import Fore,Back,Style
import argparse
import yaml
import time as t
import re
import datetime

red =  Fore.RED

green = Fore.GREEN

yellow = Fore.MAGENTA

cyan = Fore.CYAN

mixed = Fore.RED + Fore.BLUE

blue = Fore.BLUE

yellow = Fore.YELLOW

white = Fore.WHITE

reset = Style.RESET_ALL

banner = f'''{blue} 
           _____       _         _                 _             _             
          /  ___|     | |       | |               (_)           | |            
          \ `--. _   _| |__   __| | ___  _ __ ___  _ _ __   __ _| |_ ___  _ __ 
           `--. \ | | | '_ \ / _` |/ _ \| '_ ` _ \| | '_ \ / _` | __/ _ \| '__|
          /\__/ / |_| | |_) | (_| | (_) | | | | | | | | | | (_| | || (_) | |   
          \____/ \__,_|_.__/ \__,_|\___/|_| |_| |_|_|_| |_|\__,_|\__\___/|_| 
                                                                     
                                
                                             Author : D.Sanjai Kumar
                                             {reset}           
         '''



parser = argparse.ArgumentParser(description=f"{blue}Subdominator Tool to find subdomains{reset}")

parser.add_argument("-d", "--domain", help=f"{blue}[ALERT]:Domain name to find the Subdomains{reset}", type=str, required=True)

parser.add_argument("-cf", "--config", help=f"{green}[INFO]:Load your config API keys to find more Subdomains{reset}", action="store_true")

parser.add_argument("-o", "--output", help=f"{yellow}[INFO]: Filename to save the output", type=str)

args=parser.parse_args()

#check Subdominator Version

def version_check():
    
    version = "v1.0.0"
    
    url = f"https://api.github.com/repos/sanjai-AK47/Subdominator/releases/latest"
    
    try:
        
        response = requests.get(url)
        
        if response.status_code == 200:
            
            data = response.json()
            
            latest = data.get('tag_name')
            
            if latest == version:
                
                message = "latest"
                
                print(f"[{blue}Version{reset}]: Subdominator current version {version} ({green}{message}{reset})")
                
                t.sleep(1)
                
            else:
                
                message ="outdated"
                
                print(f"[{blue}Version{reset}]: Subdominator current version {version} ({red}{message}{reset})")
                
                t.sleep(1)
                
        else:
            
            pass
                
    except Exception as e:
        
        pass
                
                



#=========================================================To get unique subdomains=============================================================
subdomains_list = []

def unique_subdomains(subdomains):
    
    unique_subdomains = sorted(set(subdomains))
    
    for subdomain in unique_subdomains:
    
        print(f"[{blue}Subdominator{reset}] {subdomain}")
        
        if args.output:
            
            filename = args.output
            
            with open(filename, "a") as w:
                
                w.write(subdomain+'\n')
        else:
            filename = f"{args.domain}.subdomains.txt"
            with open(filename, "a") as w:
                
                w.write(subdomain+'\n')
    
    total = len(unique_subdomains)

    print(f"[{blue}INFO{reset}]: Total {total} subdomains found")
    
    print(f"[{green}WISH{reset}]: Happy Hacking Hacker ☠️ 🔥")
        
        

#============================================================================API configured functions=========================================================================================

def api_virustotal(domain):
    
    try:
        with open ("config_keys.yaml", "r") as keys:
            
            data = yaml.safe_load(keys)
            
            try:
                
                virus_key = data["VirusTotal"]["api_key"]
                
                if virus_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api key found for VirusTotal ")
                        
                        t.sleep(1)
            
                        print(f"[{red}ALERT{reset}]: Subdominator exiting from execution without api keys cannot execute the config mode! ")
            
                        exit()
            
                else:
            
                        pass
                
                try:
                    
                    url = f"https://www.virustotal.com/vtapi/v2/domain/report?apikey={virus_key}&domain={domain}"
                    
                    response = requests.get(url)
                    
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
                
                print(f"[{red}ALERT{reset}]: There is no api key found for VirusTotal ")    
                
    except Exception as e:
        
        print(f"[{red}Error{reset}]: The Subdominator can't find the config file please check the file in Subdominator Folder ")
        
        
            

def api_chaos(domain):
    
    try:
        
        with open("config_keys.yaml", "r") as key:
            
            data = yaml.safe_load(key)
            
            try:
                
                chaos_api_key = data['Chaos']['api_key']
                
                if chaos_api_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api key found for Chaos ")
                        
                        t.sleep(1)
            
                        print(f"[{red}ALERT{reset}]: Subdominator exiting from execution without api keys cannot execute the config mode! ")
            
                        exit()
            
                else:
            
                        pass

                url = f"https://dns.projectdiscovery.io/dns/{domain}/subdomains"

                headers= {
                        'Authorization': chaos_api_key
                }
    
                try:

                    response = requests.get(url,headers=headers)

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
        
                    print(f"[{red}ALERT{reset}]: Chaos blocking our requests ")
                    
            except Exception as e:
                
                print(f"[{red}ALERT{reset}]: There is no api key found for Chaos ") 
                
    except Exception as e:
        
        print(f"[{red}Error{reset}]: The Subdominator can't find the config file please check the file in Subdominator Folder ")
        
def whoisxml_api(domain):
    
    try:
        with open("config_keys.yaml", "r") as key:
            
            data = yaml.safe_load(key)
            
        try:
        
            whois_api_key = data ['Whoisxml']['api_key']   
            
            if whois_api_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api key found for Chaos ")
                        
                        t.sleep(1)
            
                        print(f"[{red}ALERT{reset}]: Subdominator exiting from execution without api keys cannot execute the config mode! ")
            
                        exit()
            
            else:
            
                        pass
            
            
        
            try:
                
                url = f"https://subdomains.whoisxmlapi.com/api/v1?apiKey={whois_api_key}&domainName={domain}"
            
                response = requests.get(url)
            
                if response.status_code == 200:
                
                    data = response.json()
                    
                    subdomains = data.get('result', {}).get('records', [])
                    
                    for subdomain in subdomains:
                
                            subdomain_name = subdomain.get('domain')
                            
                            if subdomain_name:
                                
                                subdomains_list.append(subdomain_name)
                                
                            else:
                                
                                print(f"[{red}ALERT{reset}]: Whoisxmlapi blocking our request")
                else:
                                
                        print(f"[{red}ALERT{reset}]: Whoisxmlapi blocking our request check your api usage")
                        
            except Exception as e:
                
                print(f"[{red}ALERT{reset}]: Whoisxmlapi blocking our request")
                
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: There is no api key found for Whoisxmlapi ")
                
        
        
    except Exception as e:
        
        print(f"[{red}Error{reset}]: The Subdominator can't find the config file please check the file in Subdominator Folder ")
        

def api_securitytrails(domain):
    
    try:
        
        with open("config_keys.yaml", "r") as key:
            
            data = yaml.safe_load(key)
            
        try:
            
            security_api_key = data ['SecurityTrails']['api_key']
            
            if security_api_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api key found for SecurityTrails ")
                        
                        t.sleep(1)
            
                        print(f"[{red}ALERT{reset}]: Subdominator exiting from execution without api keys cannot execute the config mode! ")
            
                        exit()
            
            else:
            
                        pass
            
            
            try:
                
                url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains?children_only=false&include_inactive=true"
            
                headers = {
                "accept": "application/json",
                "APIKEY": security_api_key
                }         
                
                response = requests.get(url , headers=headers)
                
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
        
        print(f"[{red}Error{reset}]: The Subdominator can't find the config file please check the file in Subdominator Folder ")
        
        
def api_bevigil(domain):
    
    try:
        
        with open("config_keys.yaml") as key:
            
            data =  yaml.safe_load(key)
            
        bevigil_api_key = data ['Bevigil']['api_key']
        
        if bevigil_api_key is None:
            
            print(f"[{red}ALERT{reset}]: There is no api key found for Bevigil ")
            
            t.sleep(1)
            
            print(f"[{red}ALERT{reset}]: Subdominator exiting from execution without api keys cannot execute the config mode! ")
            
            exit()
        else:
            
            pass
        
        
        try:
            
            url = f"http://osint.bevigil.com/api/{domain}/subdomains/"
        
            headers = {
            'X-Access-Token': bevigil_api_key
            
            }
            
            response = requests.get(url, headers=headers)
            
            
            
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
        
        print(f"[{red}Error{reset}]: The Subdominator can't find the config file please check the file in Subdominator Folder ")
        
def api_binaryedge(domain):
    
    try:
        
        with open("config_keys.yaml") as key:
            
            data = yaml.safe_load(key)
            
        binary_api_key = data ['Binaryedge']['api_key']
        
        if binary_api_key is None:
            
                print(f"[{red}ALERT{reset}]: There is no api key found for Binaryedge ")
                        
                t.sleep(1)
            
                print(f"[{red}ALERT{reset}]: Subdominator exiting from execution without api keys cannot execute the config mode! ")
            
                exit()
            
        else:
            
                pass
            
        try:
            
            url = f"https://api.binaryedge.io/v2/query/domains/subdomain/{domain}"
            
            headers = {
            'X-Key': binary_api_key
            
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                
                data =  response.json()
                
                subdomains = data.get('events', [])
                
                for subdomain in subdomains:
                    
                        subdomains_list.append(subdomain)
                
            else:
                
                print(f"[{red}ALERT{reset}]: Binaryedge blocking our request check your api usage ")
            
        except Exception as e:
                
            print(f"[{red}ALERT{reset}]: There is no api key found for Binaryedge ") 
            
    except Exception as e:
        
        print(f"[{red}Error{reset}]: The Subdominator can't find the config file please check the file in Subdominator Folder ")
        

def api_fullhunt(domain):
    
    try:
        
        with open("config_keys.yaml") as keys:
            
            data = yaml.safe_load(keys)
        
        fullhunt_api_key = data ['Fullhunt']['api_key']
        
        if fullhunt_api_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api key found for Fullhunt ")
                        
                        t.sleep(1)
            
                        print(f"[{red}ALERT{reset}]: Subdominator exiting from execution without api keys cannot execute the config mode! ")
            
                        exit()
        
        else:
            
            pass
        
        try:
            
            url = f"https://fullhunt.io/api/v1/domain/{domain}/subdomains"
            
            headers = {
                'X-API-KEY': fullhunt_api_key
            }
            
            response = requests.get(url,headers=headers)
            
            if response.status_code == 200:
                
                data = response.json()
                
                subdomains = data.get('hosts', [])
                
                for subdomain in subdomains:
                    
                    subdomains_list.append(subdomain)
        
        except Exception as e:
            
            print(f"[{red}ALERT{reset}]: Fullhunt blocking our requests check your api usage ")
            
        
    except Exception as e:
        
        print(f"[{red}Error{reset}]: The Subdominator can't find the config file please check the file in Subdominator Folder ")
        

def api_bufferover(domain):
    
    try:
        with open("config_keys.yaml", "r") as key:
            
            data = yaml.safe_load(key)
        
        bufferover_api_key = data['Bufferover']['api_key']
            
        if bufferover_api_key is None:
            
            print(f"[{red}ALERT{reset}]: There is no api key found for Bufferover ")
                        
            t.sleep(1)
            
            print(f"[{red}ALERT{reset}]: Subdominator exiting from execution without api keys cannot execute the config mode! ")
            
            exit()
            
        else:
            pass
        try:
            
            url = f"https://tls.bufferover.run/dns?q=.{domain}"
            
            headers = {
            'x-api-key': f'{bufferover_api_key}'
            }
            
            response = requests.get(url,headers=headers)
            
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
            
            print(f"[{red}ALERT{reset}]: Bufferover blocking our requests ")
                    
            
    except Exception  as e:
        
        print(f"[{red}Error{reset}]: The Subdominator can't find the config file please check the file in Subdominator Folder ")
        
        


def api_certspoter(domain):
    
    try:
        
        with open("config_keys.yaml","r") as keys:
            
            data = yaml.safe_load(keys)
            
        certspotter_api_key = data ['Certspotter']['api_key']
        
        if certspotter_api_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api key found for Certspotter ")
                        
                        t.sleep(1)
            
                        print(f"[{red}ALERT{reset}]: Subdominator exiting from execution without api keys cannot execute the config mode! ")
            
                        exit()
        
        else:
            
            pass
        
        try:
            
            url = f"https://api.certspotter.com/v1/issuances?domain={domain}&expand=dns_names"
            
            headers = {"Authorization": f"Bearer {certspotter_api_key}"}
            
            response = requests.get(url, headers=headers)
            
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
        
        print(f"[{red}Error{reset}]: The Subdominator can't find the config file please check the file in Subdominator Folder ")
        
        
def rapid_whois(domain):
    
    try :
        
        with open("config_keys.yaml", "r") as keys:
            
            data = yaml.safe_load(keys)
            
        rapid_api_key = data['Rapidapi']['api_key']
        
        integrated_key = data['Whoisxml']['api_key']
        
        if rapid_api_key is None or integrated_key is None:
            
                        print(f"[{red}ALERT{reset}]: There is no api keys found for Rapidapi and integrated  ")
                        
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
            
            response = requests.get(url, headers=headers, params=querystring)
            
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
                
                print (f"[{red}Alert{reset}]: RapidWhois Blocking our requests check your api usage ")
            
        except Exception as e:
            
            print (f"[{red}Alert{reset}]: RapidWhois Blocking our requests")
                    
                    
    except Exception as e:
        
        print(f"[{red}Error{reset}]: The Subdominator can't find the config file please check the file in Subdominator Folder ")
        
        



def rapid_scan(domain):
    
    try :
        
        with open("config_keys.yaml", "r") as keys:
            
            data = yaml.safe_load(keys)
            
        rapid_api_key = data['Rapidapi']['api_key']
        
        
        if rapid_api_key is None :
            
                        print(f"[{red}ALERT{reset}]: There is no api keys found for Rapidapi ")
                        
                        t.sleep(1)
            
                        print(f"[{red}ALERT{reset}]: Subdominator exiting from execution without api keys cannot execute the config mode! ")
            
                        exit()
            
        else:
            
                        pass
                    
                    
        try:
            
            url = "https://subdomain-scan1.p.rapidapi.com/"

            querystring = {"domain":f"{domain}"}

            headers = {
	"X-RapidAPI-Key": f"{rapid_api_key}",
	"X-RapidAPI-Host": "subdomain-scan1.p.rapidapi.com"
}
            
            response = requests.get(url, headers=headers, params=querystring)
            
            if response.status_code == 200:
                
                data = response.json()
                
                subdomains = list(data)
                
                for subdomain in subdomains:
                    
                    subdomains_list.append(subdomain)
                    
            else:
                
                print (f"[{red}Alert{reset}]: RapidScan Blocking our requests check your api usage")
            
        except Exception as e:
            
            print (f"[{red}Alert{reset}]: RapidScan Blocking our requests")
                    
                    
    except Exception as e:
        
        print(f"[{red}Error{reset}]: The Subdominator can't find the config file please check the file in Subdominator Folder ")
        
        
def non_api_dnsdump(domain):
    
    try:
        with open("config_keys.yaml", "r") as keys:
            
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
        
        print(f"[{red}Error{reset}]: The Subdominator can't find the config file please check the file in Subdominator Folder ")
        
        
        







#==============================================================NOn-Config functions =====================================================================================================


def non_api_alienvault(domain):  
    
    try:
        url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
        
        response = requests.get(url)
        
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
        
        response = requests.post(url,headers=headers,data=data)
        
        
        if response.status_code == 200:
            
            pattern = f"https://([\w-]+\.{domain})"
            
            subdomains = re.findall(pattern, response.text)
            
            for subdomain in subdomains:
                
                subdomains_list.append(subdomain)
                
        else:
            print(f"[{red}ALERT{reset}]: Seckdr blocking our request something went wrong with Seckdr")
            
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Seckdr blocking our request ")
        
    
                
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
                
def rapidns(domain):
    
    try:
        
        url = f"https://rapiddns.io/subdomain/{domain}#result"

        response = requests.get(url)

        if response.status_code == 200:
                        
            content =  response.text
                        
            subdomains_pattern = re.compile(rf"\b[a-zA-Z0-9]+\b\.{domain}\b")
                        
            subdomains = subdomains_pattern.findall(content)
                        
            for subdomain in subdomains:
            
                subdomains_list.append(subdomain)
                
    except Exception as e:
        
        print(f"[{red}ALERT{reset}]: Rapidns is blocking our requests")
        


#========================================================calling functions==========================================================================================

if args.domain and args.config:
    
    print(banner)
    
    version_check()
    
    t.sleep(1)
    
    print(f"[{blue}INFO{reset}]: Started to collecting the subdomains for: {args.domain}")
    
    t.sleep(1)
    
    print(f"[{green}INFO{reset}]: User Enabled config mode")
    
    t.sleep(1)
    print(f"[{blue}INFO{reset}]: Sudominator 🔥 will collect more subdomains than non-config mode when enabling the config mode!")
    
    domain = args.domain
    
    
    api_chaos(domain)
    
    api_virustotal(domain)
    
    whoisxml_api(domain)
    
    api_securitytrails(domain)
    
    api_bevigil(domain)
    
    api_binaryedge(domain)
    
    api_fullhunt(domain)
    
    api_certspoter(domain)
        
    non_api_alienvault(domain)
    
    non_api_seckdr(domain)
    
    non_api_dnsdump(domain)
    
    non_api_c99(domain)
    
    rapidns(domain)
    
    api_bufferover(domain)
    
    api_certspoter(domain)
    
    rapid_whois(domain)
    
    rapid_scan(domain)
    
    unique_subdomains(subdomains_list)
    
elif args.domain and not args.config:
    
    print(banner)
    
    domain =  args.domain
    
    version_check()
    
    
    print(f"[{red}ALERT{reset}]: User not enabled the config mode")
    
    t.sleep(3)
    
    print(f"[{green}INFO{reset}]: Dont worry User! Subdominator continuing with the non-config mode :)")
    
    
    t.sleep(1)
    
    print(f"[{blue}INFO{reset}]: Started to collecting the subdomains for: {domain}")
    
    non_api_alienvault(domain)
    
    non_api_c99(domain)
    
    non_api_seckdr(domain)
    
    rapidns(domain)
    
    non_api_c99(domain)
    
    unique_subdomains(subdomains_list)
    
elif not args.domain:
    
    print(f"[{red}ALERT{reset}]: No domain in is given to gather subdomains")
    
    exit()
    
else:
    pass
    
    
    
    
    



