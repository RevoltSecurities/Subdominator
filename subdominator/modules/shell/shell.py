import os
import json
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from subdominator.modules.models.models import AsyncSessionLocal
from subdominator.modules.crud.crud import get_all_domains, get_subdomains, get_domain, add_or_update_domain, delete_domain
from subdominator.modules.config.config import html_config
from subdominator.modules.utils.utils import Exit
from rich.console import Console
from rich.table import Table
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

console = Console()

class SubDominatorShell:
    def __init__(self):
        self.prompt = f"[subdominator]$ "
        self.session = PromptSession()
        self.db_connected = False  

    async def cmdloop(self):
        while True:
            try:
                with patch_stdout():
                    user_input = await self.session.prompt_async(self.prompt)

                if not user_input.strip():
                    continue
                
                if user_input.startswith("help"):
                    await self.do_help()
                    continue
                
                if user_input.lower() == "exit":
                    Exit(0)

                if user_input.lower() == "connect db":
                    self.db_connected = True
                    console.print("[bold green]Connected to SubDominator Database.[/bold green]")
                    continue

                if not self.db_connected:
                    console.print("[bold red]Error: Database not connected. Use 'connect db' first.[/bold red]")
                    continue

                if user_input.startswith("show domains"):
                    await self.async_show_domains()
                elif user_input.startswith("show subdomain"):
                    domain = user_input[len("show subdomain"):].strip()
                    await self.async_show_subdomain(domain)
                elif user_input.startswith("add domain"):
                    args = user_input[len("add domain"):].strip().split()
                    if len(args) == 2:
                        await self.async_add_domain(args[0], args[1])
                    else:
                        console.print("[bold yellow]Usage: add domain <domain> <subdomains_file>[/bold yellow]")
                elif user_input.startswith("update"):
                    args = user_input[len("update"):].strip().split()
                    if len(args) == 2:
                        await self.async_update_domain(args[0], args[1])
                    else:
                        console.print("[bold yellow]Usage: update <domain> <subdomains_file>[/bold yellow]")
                elif user_input.startswith("delete"):
                    domain = user_input[len("delete"):].strip()
                    if domain:
                        await self.async_delete_domain(domain)
                    else:
                        console.print("[bold yellow]Usage: delete <domain>[/bold yellow]")
                elif user_input.startswith("export"):
                    args = user_input[len("export"):].strip().split()
                    if len(args) == 3:
                        await self.async_export_data(args[0], args[1], args[2])
                    else:
                        console.print("[bold yellow]Usage: export <domain> <file> <format(txt/json)>[/bold yellow]")
                elif user_input.startswith("report"):
                    args = user_input[len("report"):].strip().split()
                    if len(args) == 3:
                        await self.generate_report(args[0], args[1], args[2])
                    else:
                        console.print("[bold yellow]Usage: report <domain> <filename> <format(pdf/html>[/bold yellow]")
                else:
                    os.system(user_input.lower())
            except KeyboardInterrupt:
                console.print("\n[bold red]Exiting SubDominator Shell...[/bold red]")
                break
            except Exception as e:
                console.print(f"[bold red]Error: {e}[/bold red]")

    async def async_show_domains(self):
        async with AsyncSessionLocal() as session:
            domains = await get_all_domains(session)
            if not domains:
                console.print("[bold yellow]No records exist.[/bold yellow]")
                return

            table = Table(title="[bold cyan]DB Stored Domains[/bold cyan]")
            table.add_column("[bold]Domain[/bold]", style="cyan", justify="left")

            for domain in domains:
                table.add_row(domain.domain)
            console.print(table)

    async def async_show_subdomain(self, domain):
        async with AsyncSessionLocal() as session:
            subdomains = await get_subdomains(session, domain)
            if not subdomains:
                console.print(f"[bold yellow]No records exist for {domain}.[/bold yellow]")
                return

            table = Table(title=f"[bold cyan]Subdomains of {domain}[/bold cyan]")
            table.add_column("[bold]Subdomain[/bold]", style="cyan", justify="left")

            for subdomain in sorted(subdomains):
                table.add_row(subdomain)
            console.print(table)

    async def async_add_domain(self, domain, subdomains_file):
        subdomains = self.load_subdomains_from_file(subdomains_file)
        if not subdomains:
            console.print("[bold red]Error: No valid subdomains found in file.[/bold red]")
            return

        async with AsyncSessionLocal() as session:
            await add_or_update_domain(session, domain, subdomains)
            console.print(f"[bold green]Domain {domain} added successfully![/bold green]")

    async def async_update_domain(self, domain, subdomains_file):
        subdomains = self.load_subdomains_from_file(subdomains_file)
        if not subdomains:
            console.print("[bold red]Error: No valid subdomains found in file.[/bold red]")
            return

        async with AsyncSessionLocal() as session:
            existing_entry = await get_domain(session, domain)
            if not existing_entry:
                console.print(f"[bold yellow]Domain {domain} does not exist.[/bold yellow]")
                return

            await add_or_update_domain(session, domain, subdomains)
            console.print(f"[bold green]Domain {domain} updated successfully![/bold green]")

    async def async_delete_domain(self, domain):
        async with AsyncSessionLocal() as session:
            success = await delete_domain(session, domain)
            if success:
                console.print(f"[bold red]Domain {domain} and all its records deleted successfully![/bold red]")
            else:
                console.print(f"[bold yellow]Domain {domain} does not exist.[/bold yellow]")

    async def async_export_data(self, domain, filename, format_type):
        async with AsyncSessionLocal() as session:
            subdomains = await get_subdomains(session, domain)
            if not subdomains:
                console.print(f"[bold yellow]No records exist for {domain}.[/bold yellow]")
                return

            if format_type.lower() == "txt":
                with open(filename, "w") as file:
                    for subdomain in sorted(subdomains):
                        file.write(f"{subdomain}\n")
            elif format_type.lower() == "json":
                with open(filename, "w") as file:
                    json.dump({"domain": domain, "subdomains": sorted(subdomains)}, file, indent=4)
            else:
                console.print("[bold red]Error: Format must be 'txt' or 'json'.[/bold red]")
                return
            console.print(f"[bold green]Data exported to {filename} successfully![/bold green]")
            
    async def generate_report(self,domain,output_file,format_type):
        htmlpath = html_config()
        if not htmlpath:
            console.print(f"[bold yellow]Unable to get the html configuration template,please check the html template file exist.[/bold yellow]")
            return
        async with AsyncSessionLocal() as session:
            subdomains = await get_subdomains(session,domain)
            if not subdomains:
                console.print(f"[bold yellow]No records exist for {domain} to generate report.[/bold yellow]")
                return
            
            report_data = {
                "domain": domain,
                "subdomains": sorted(subdomains)
            }

            html_report = self.generate_html_report(report_data=report_data, template_path=htmlpath)
            
            if format_type.lower() == "html":
                with open(output_file, "w") as f:
                    f.write(html_report)
                console.print(f"[bold green]HTML report saved as {output_file}[/bold green]")
            elif format_type.lower() == "pdf":
                self.generate_pdf_report(html_report, output_file)
                console.print(f"[bold green]PDF report saved as {output_file}[/bold green]")
            else:
                console.print(f"[bold yellow]Report generation only supports pdf/html format, please use a valid report generation format.[/bold yellow]")
                return
    def generate_html_report(self, report_data, template_path):
        env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
        template = env.get_template(os.path.basename(template_path))
        return template.render(domain=report_data["domain"], subdomains=report_data["subdomains"])
    
    def generate_pdf_report(self,html_report, output_file):
        HTML(string=html_report).write_pdf(output_file)
    
    def load_subdomains_from_file(self, filename):
        if not os.path.exists(filename):
            console.print(f"[bold red]Error: File '{filename}' not found.[/bold red]")
            return None

        with open(filename, "r") as file:
            subdomains = {line.strip() for line in file if line.strip()}
        return subdomains if subdomains else None

    async def do_help(self):
        console.print(
            """
[bold][blue]Available Commands:[/blue][/bold]
  [bold][green]connect db[/green][/bold]                            [bold]- Connect to Subdominator DataBase[/bold]
  [bold][green]show domains[/green][/bold]                          [bold]- Show all domains[/bold]
  [bold][green]show subdomain <domain>[/green][/bold]               [bold]- Show subdomains of a domain[/bold]
  [bold][green]add domain <domain> <subdomains_file>[/green][/bold] [bold]- Add a domain[/bold]
  [bold][green]update <domain> <subdomains_file>[/green][/bold]     [bold]- Update an existing domain[/bold]
  [bold][green]delete <domain>[/green][/bold]                       [bold]- Delete a domain and all subdomains[/bold]
  [bold][green]export <domain> <file> <format>[/green][/bold]       [bold]- Export data to txt/json[/bold]
  [bold][green]report <domain> <file> <format>[/green][/bold]       [bold]- Generate subdomains report in html/pdf format[/bold]
  [bold][green]exit[/green][/bold]                                  [bold]- Exit the interactive shell[/bold]
  [bold][green]help[/green][/bold]                                  [bold]- Show this help menu[/bold]
  [bold][green]System Commands[/green][/bold]                       [bold]- ls, clear, pwd, cd, cat, echo, mkdir, rm, cp, mv[/bold]
            """
        )