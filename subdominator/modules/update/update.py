import requests
import subprocess
import os
from rich.console import Console
from rich.markdown import Markdown
from subdominator.modules.logger.logger import logger
from subdominator.modules.utils.utils import Exit
import importlib.metadata as data

console = Console()

def getverify(pkg):
    version = data.version(pkg)
    return version

def getzip(): 
    try:
        url = "https://api.github.com/repos/RevoltSecurities/Subdominator/releases/latest"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()['zipball_url']
        else:
            logger(f"Hey Update Failed for Subdominator, Please try to update the Subdominator manually", "warn")
            Exit(1)
    except Exception as e:
        pass
    
def launch(url,config):
    try:
        response = requests.get(url, timeout=20, stream=True)
        filepath = f"{config}/Subdominator.zip"
        if response.status_code == 200:
            logger(f"Downloading Subdominator latest version with PIPX", "info")
            with open(f"{filepath}", "wb") as streamw:
                for data in response.iter_content():
                    if data:
                        streamw.write(data)
            try:
                subprocess.run(["pipx", "install", f"{filepath}", "--force"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                logger(f"Update Failed for Subdominator, Please try to update the Subdominator manually", "warn")
                os.remove(filepath)
                Exit(1)
            finally:
                os.remove(filepath)
        else:
            logger(f"Update Failed for Subdominator, Please try to update the Subdominator manually", "info")
            Exit(1)
    except Exception as e:
        pass

def updatelog():
    try:
        url = f"https://api.github.com/repos/RevoltSecurities/Subdominator/releases/latest"
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            loader = response.json()["body"]
            console.print(Markdown(loader))
        else:
            logger(f"Hey  unable to fetch update logs so please visit here --> https://github.com/RevoltSecurities/Subdominator", "info")
            Exit(1)
    except Exception as e:
        pass