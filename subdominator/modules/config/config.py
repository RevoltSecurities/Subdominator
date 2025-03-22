import appdirs
import os
import sqlite3
from subdominator.modules.utils.utils import *
from subdominator.modules.logger.logger import logger

yamls = """arpsyndicate:[]

bevigil: []          

binaryedge: []

bufferover: []

builtwith: []

c99: []

censys: []

certspotter: []

chaos: []

digitalyama: []

dnsdumpster: []

dnsrepo: []

facebook: []

fofa: []

fullhunt: []

google: []

huntermap: []

intelx: []

leakix: []

merklemap: []

netlas: []

odin: []

quake: []

rapidapi: []

redhuntlabs: []

rsecloud: []

virustotal: []

securitytrails: []

shodan: []

trickest: []

whoisxmlapi: []

zoomeyeapi: []

# for notifications
slack: []

pushbullet: []

"""

def Username():
    try:
        username = os.getlogin()
    except OSError:
        username = os.getenv('USER') or os.getenv('LOGNAME') or os.getenv('USERNAME') or 'User'
    except Exception as e:
        username = "User"
    return username

def config(): 
    try:
        get_config = appdirs.user_config_dir()
        subdominator_dir = os.path.join(get_config, "Subdominator")
        filename = "provider-config.yaml"
        config_path = os.path.join(subdominator_dir, filename)
        os.makedirs(subdominator_dir, exist_ok=True)

        if not os.path.exists(config_path):
            with open(config_path, "w") as w:
                w.write(yamls)
        return config_path
    except Exception as e:
        logger(f"Exception occurred at config module: {e}", "warn")

def custompath(path:str, args):
    try:
        if os.path.exists(path) and os.path.isfile(path):
            return path
        else:
            logger(f"Please check if the config path exists", "warn", args.no_color)
    except KeyboardInterrupt as e:
        quit()

def cachedir():
    try:
        cachedir = appdirs.user_cache_dir()
        return cachedir
    except Exception as e:
        pass
    
def db_config():
    try:
        get_config = cachedir()
        subdominator_db_dir = os.path.join(get_config, "SubdominatorDB")
        db_filename = "subdominator.db"
        db_path = os.path.join(subdominator_db_dir, db_filename)
        if not os.path.exists(subdominator_db_dir):
            os.makedirs(subdominator_db_dir)
        conn = sqlite3.connect(db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS subdomains (
                domain TEXT PRIMARY KEY,
                subdomains TEXT
            )
        """)
        conn.commit()
        conn.close()
        return db_path
    except Exception as e:
        logger(f"Exception occurred in db_config: {e}", "warn")
        return None

def html_config():
    """Gets the file path of the report HTML template and ensures it exists."""
    try:
        get_config = appdirs.user_config_dir()
        subdominator_dir = os.path.join(get_config, "Subdominator")
        filename = "report_template.html"
        html_path = os.path.join(subdominator_dir, filename)

        os.makedirs(subdominator_dir, exist_ok=True)

        default_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subdomain Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f4f4f4; }
    </style>
</head>
<body>
    <h1>Subdomain Report for {domain}</h1>
    <table>
        <tr>
            <th>Subdomain</th>
        </tr>
        {subdomain_rows}
    </table>
</body>
</html>"""

        if not os.path.exists(html_path):
            with open(html_path, "w") as f:
                f.write(default_html)
        return html_path
    except Exception as e:
        logger(f"Exception occurred in html_config: {e}", "warn")
        return None
