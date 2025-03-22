from subdominator.modules.utils.utils import bold, white, blue, reset, Exit

def help(path, dbpath):
    print(f"""
{bold}{white}[{reset}{bold}{blue}DESCRIPTION{reset}{bold}{white}]{reset}: 

    {bold}{white}Subdominator is a passive subdomain enumeration tool that discovers subdomains for your targets using passive and open-source resources.{reset}

{bold}{white}[{reset}{bold}{blue}USAGE{reset}{bold}{white}]{reset}: 

    {bold}{white}subdominator [flags]{reset}

{bold}{white}[{reset}{bold}{blue}FLAGS{reset}{bold}{white}]{reset}:

    {bold}{white}[{reset}{bold}{blue}INPUT{reset}{bold}{white}]{reset}:
    
        {bold}{white}-d,   --domain                :  Target domain name for subdomain enumeration.
        -dL,  --domain-list           :  File containing multiple domains for bulk enumeration.
        stdin/stdout                  :  Supports input/output redirection.

    {bold}{white}[{reset}{bold}{blue}OUTPUT{reset}{bold}{white}]{reset}:
    
        {bold}{white}-o,   --output                :  Save results to a file.
        -oD,  --output-directory      :  Directory to save results (useful when -dL is specified).
        -json, --json                 :  Output results in JSON format.{reset}
        
    {bold}{white}[{reset}{bold}{blue}MODE{reset}{bold}{white}]{reset}:
    
        {bold}{white}-shell, --shell               :  Enable interactive shell mode to work with subdominator Database,generate report and etc.{reset}

    {bold}{white}[{reset}{bold}{blue}OPTIMIZATION{reset}{bold}{white}]{reset}:
    
        {bold}{white}-t,   --timeout               :  Set timeout value for API requests (default: 30s).
        -fw,  --filter-wildcards      :  Filter out wildcard subdomains.{reset}

    {bold}{white}[{reset}{bold}{blue}CONFIGURATION{reset}{bold}{white}]{reset}:
    
        {bold}{white}-cp,  --config-path           :  Custom config file path for API keys (default: {path}).
        -cdp, --config-db-path        :  Custom database config path (default: {dbpath}).
        -nt,  --notify                :  Send notifications for found subdomains via Slack, Pushbullet.
        -px,  --proxy                 :  Use an HTTP proxy for debugging requests.
        -dork, --dork                 :  Use a custom google dork for google resource (ex: -ir google --dork 'site:target.com -www -dev intext:secrets'){reset}

    {bold}{white}[{reset}{bold}{blue}RESOURCE CONFIGURATION{reset}{bold}{white}]{reset}:
    
        {bold}{white}-ir,  --include-resources     :  Specify sources to include (comma-separated).
        -er,  --exclude-resources     :  Specify sources to exclude (comma-separated).
        -all, --all                   :  Use all available sources for enumeration.{reset}

    {bold}{white}[{reset}{bold}{blue}UPDATE{reset}{bold}{white}]{reset}:
    
        {bold}{white}-up,  --update                :  Update Subdominator to the latest version (manual YAML update required).
        -duc, --disable-update-check  :  Disable automatic update checks.
        -sup, --show-updates          :  Show the latest update details.{reset}

    {bold}{white}[{reset}{bold}{blue}DEBUGGING{reset}{bold}{white}]{reset}:
    
        {bold}{white}-h,   --help                  :  Show this help message and exit.
        -v,   --version               :  Show the current version and check for updates.
        -s,   --silent                :  Show only subdomains in output.
        -ski, --show-key-info         :  Show API key errors (e.g., out of credits).
        -sti, --show-timeout-info     :  Show timeout errors for sources.
        -nc,  --no-color              :  Disable colorized output.
        -ls,  --list-source           :  List available subdomain enumeration sources.
        -V,   --verbose               :  Enable verbose output.{reset}
""")
    Exit()