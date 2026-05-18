from __future__ import annotations

import asyncio
import json
import shlex
from dataclasses import dataclass
from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from subdominator.core.constants import VERSION
from subdominator.core.models import EnumerationSummary, Finding, ResourceExecution
from subdominator.output.reports import ReportGenerator
from subdominator.storage.repository import EnumerationRepository
from gitupdater import GitUpdater


@dataclass(slots=True)
class ShellCommand:
    name: str
    args: list[str]


def parse_shell_command(raw: str) -> ShellCommand | None:
    raw = raw.strip()
    if not raw:
        return None
    parts = shlex.split(raw)
    return ShellCommand(name=parts[0].lower(), args=parts[1:])


class SubdominatorShell:
    def __init__(
        self,
        *,
        console: Console,
        repository: EnumerationRepository,
        db_path: Path,
        config_path: Path,
        resource_metadata: list[dict[str, str | bool]],
        gitmanager: GitUpdater,
    ) -> None:
        self.console = console
        self.repository = repository
        self.db_path = db_path
        self.config_path = config_path
        self.resource_metadata = resource_metadata
        self.gitmanager = gitmanager

    async def run(self) -> int:
        self._print_welcome()
        while True:
            try:
                raw = await asyncio.to_thread(
                    self.console.input,
                    "[bold cyan]subdominator-shell[/bold cyan]> ",
                )
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[bold yellow]Exiting shell.[/bold yellow]")
                return 0
            try:
                command = parse_shell_command(raw)
            except ValueError as exc:
                self.console.print(f"[bold yellow]Input parse error:[/bold yellow] {exc}")
                continue
            if command is None:
                continue
            if command.name in {"exit", "quit"}:
                return 0
            if command.name == "help":
                self._print_help()
                continue
            if command.name == "clear":
                self.console.clear()
                continue
            if command.name == "domains":
                self._show_domains()
                continue
            if command.name == "runs":
                self._show_runs(command.args)
                continue
            if command.name in {"domain", "show"}:
                self._show_domain(command.args)
                continue
            if command.name == "findings":
                self._show_findings(command.args)
                continue
            if command.name == "add":
                self._add_domain(command.args)
                continue
            if command.name == "delete":
                self._delete_domain(command.args)
                continue
            if command.name == "export":
                self._export_domain(command.args)
                continue
            if command.name == "resources":
                self._show_resources()
                continue
            if command.name == "config":
                self.console.print(f"[bold white]Config:[/bold white] {self.config_path}")
                self.console.print(f"[bold white]Database:[/bold white] {self.db_path}")
                continue
            if command.name == "update":
                await self.gitmanager.update()
                continue
            if command.name == "release":
                await self.gitmanager.show_update_log()
                continue
            self.console.print(f"[bold red]Unknown command:[/bold red] {command.name}")
            self.console.print("[dim]Type 'help' to see supported commands.[/dim]")

    def _print_welcome(self) -> None:
        self.console.print(
            Panel.fit(
                "\n".join(
                    [
                        f"[bold white]Subdominator Shell {VERSION}[/bold white]",
                        f"[dim]DB[/dim] {self.db_path}",
                        f"[dim]Config[/dim] {self.config_path}",
                        "[dim]Type 'help' for commands.[/dim]",
                    ]
                ),
                border_style="bright_blue",
            )
        )

    def _print_help(self) -> None:
        table = Table(title="Shell Commands", box=box.ROUNDED, header_style="bold cyan")
        table.add_column("Command", style="bold white")
        table.add_column("Description", style="green")
        table.add_row("domains", "List stored root domains")
        table.add_row("domain <root>", "Show stored domain summary")
        table.add_row("findings <root>", "Show stored findings for a root domain")
        table.add_row("add <root> <file>", "Add or merge findings from a text file")
        table.add_row("add domain <root> <file>", "Legacy-style alias for text-file import")
        table.add_row("runs [root]", "Show recent stored runs, optionally filtered by root")
        table.add_row("export <root> <path> [txt|json|html]", "Export findings to a file")
        table.add_row("delete <root>", "Delete a root domain and its stored runs/findings")
        table.add_row("resources", "List current resource catalog markers")
        table.add_row("config", "Show config and database paths")
        table.add_row("update", "Update Subdominator to its latest version")
        table.add_row("release", "Show release notes of Subdominator's latest version")
        table.add_row("clear", "Clear the screen")
        table.add_row("exit", "Exit the shell")
        self.console.print(table)

    def _show_domains(self) -> None:
        domains = self.repository.list_domains()
        if not domains:
            self.console.print("[bold yellow]No stored domains found.[/bold yellow]")
            return

        table = Table(title="Stored Domains", box=box.ROUNDED, header_style="bold magenta")
        table.add_column("Root Domain", style="bold white")
        table.add_column("Findings", justify="right", style="green")
        table.add_column("Latest Run", justify="right", style="cyan")
        table.add_column("Last Discovered", style="yellow")
        for item in domains:
            table.add_row(
                item.root_domain,
                str(item.findings_count),
                str(item.latest_run_id or "-"),
                item.last_discovered_at.isoformat(timespec="seconds") if item.last_discovered_at else "-",
            )
        self.console.print(table)

    def _show_domain(self, args: list[str]) -> None:
        if len(args) != 1:
            self.console.print("[bold yellow]Usage:[/bold yellow] domain <root-domain>")
            return
        stats = self.repository.get_domain_stats(args[0])
        if stats is None:
            self.console.print(f"[bold yellow]No stored data for {args[0]}.[/bold yellow]")
            return

        table = Table(title=f"Domain Summary: {stats.root_domain}", box=box.ROUNDED, header_style="bold cyan")
        table.add_column("Metric", style="bold white")
        table.add_column("Value", style="green")
        table.add_row("Stored Findings", str(stats.findings_count))
        table.add_row("Unique Resources", str(stats.unique_resources))
        table.add_row("Latest Run", str(stats.latest_run_id or "-"))
        table.add_row(
            "Latest Run At",
            stats.latest_run_at.isoformat(timespec="seconds") if stats.latest_run_at else "-",
        )
        table.add_row(
            "First Discovered",
            stats.first_discovered_at.isoformat(timespec="seconds") if stats.first_discovered_at else "-",
        )
        table.add_row(
            "Last Discovered",
            stats.last_discovered_at.isoformat(timespec="seconds") if stats.last_discovered_at else "-",
        )
        self.console.print(table)

    def _show_findings(self, args: list[str]) -> None:
        if len(args) != 1:
            self.console.print("[bold yellow]Usage:[/bold yellow] findings <root-domain>")
            return
        findings = self.repository.get_findings(args[0])
        if not findings:
            self.console.print(f"[bold yellow]No stored findings for {args[0]}.[/bold yellow]")
            return

        table = Table(title=f"Findings: {args[0]}", box=box.SIMPLE_HEAVY, header_style="bold bright_blue")
        table.add_column("Subdomain", style="bold white")
        table.add_column("Resource", style="magenta")
        table.add_column("Target", style="cyan")
        table.add_column("Depth", justify="right", style="green")
        for item in findings:
            table.add_row(item.subdomain, item.resource, item.query_target, str(item.recursion_depth))
        self.console.print(table)

    def _show_runs(self, args: list[str]) -> None:
        if len(args) > 1:
            self.console.print("[bold yellow]Usage:[/bold yellow] runs [root-domain]")
            return
        self.console.print("[bold yellow]Run history is unavailable for the legacy DB format.[/bold yellow]")
        return

    def _add_domain(self, args: list[str]) -> None:
        if len(args) == 3 and args[0].lower() == "domain":
            root_domain = args[1].strip().lower()
            input_path = Path(args[2])
        elif len(args) == 2:
            root_domain = args[0].strip().lower()
            input_path = Path(args[1])
        else:
            self.console.print("[bold yellow]Usage:[/bold yellow] add <root-domain> <txt-file>")
            self.console.print("[bold yellow]Usage:[/bold yellow] add domain <root-domain> <txt-file>")
            return

        findings = self._load_findings_file(root_domain, input_path)
        if not findings:
            self.console.print(f"[bold yellow]No valid findings found in {input_path} for {root_domain}.[/bold yellow]")
            return

        before_count = self.repository.count_findings(root_domain)
        self.repository.save_findings(root_domain, findings)
        after_count = self.repository.count_findings(root_domain)
        added_count = after_count - before_count

        if before_count == 0:
            self.console.print(
                f"[bold green]Added[/bold green] {after_count} finding(s) for [bold white]{root_domain}[/bold white]."
            )
        else:
            self.console.print(
                f"[bold green]Merged[/bold green] {len(findings)} input finding(s) into [bold white]{root_domain}[/bold white]."
            )
            self.console.print(
                f"[bold white]Newly added:[/bold white] {added_count}  [bold white]Already present:[/bold white] {len(findings) - added_count}"
            )

    def _delete_domain(self, args: list[str]) -> None:
        if len(args) != 1:
            self.console.print("[bold yellow]Usage:[/bold yellow] delete <root-domain>")
            return
        deleted = self.repository.delete_domain(args[0])
        if deleted == 0:
            self.console.print(f"[bold yellow]No stored data for {args[0]}.[/bold yellow]")
            return
        self.console.print(
            f"[bold green]Deleted[/bold green] {deleted} stored finding(s) for [bold white]{args[0]}[/bold white]."
        )

    def _export_domain(self, args: list[str]) -> None:
        if len(args) not in {2, 3}:
            self.console.print("[bold yellow]Usage:[/bold yellow] export <root-domain> <path> [txt|json]")
            return
        root_domain, output_path = args[0], Path(args[1])
        export_format = (args[2] if len(args) == 3 else output_path.suffix.lstrip(".") or "txt").lower()
        findings = self.repository.get_findings(root_domain)
        if not findings:
            self.console.print(f"[bold yellow]No stored findings for {root_domain}.[/bold yellow]")
            return
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if export_format == "txt":
            output_path.write_text(
                "\n".join(item.subdomain for item in findings) + "\n",
                encoding="utf-8",
            )
        elif export_format == "json":
            payload = {
                "root_domain": root_domain,
                "findings": [
                    {
                        "subdomain": item.subdomain,
                        "resource": item.resource,
                        "query_target": item.query_target,
                        "recursion_depth": item.recursion_depth,
                        "discovered_at": item.discovered_at.isoformat(),
                    }
                    for item in findings
                ],
            }
            output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        elif export_format == "html":
            summary = self._generate_synthetic_summary(root_domain, findings)
            ReportGenerator.to_html(output_path, summary)
        else:
            self.console.print("[bold yellow]Export format must be txt, json, or html.[/bold yellow]")
            return
        self.console.print(f"[bold green]Exported[/bold green] {len(findings)} finding(s) to {output_path}")

    def _generate_synthetic_summary(self, root_domain: str, findings: list[Finding]) -> EnumerationSummary:
        """Create a synthetic EnumerationSummary from historical findings."""
        from datetime import UTC, datetime
        
        # Sort findings by subdomain for the report
        sorted_findings = sorted(findings, key=lambda f: f.subdomain)
        
        # Pull seen targets from findings
        seen_targets = {f.domain for f in findings} | {f.query_target for f in findings}
        
        # Find earliest/latest dates
        if findings:
            started_at = min(f.discovered_at for f in findings)
            completed_at = max(f.discovered_at for f in findings)
        else:
            started_at = completed_at = datetime.now(UTC)

        # Build dummy resource executions based on unique resources seen
        resources = {f.resource for f in findings}
        resource_executions = [
            ResourceExecution(
                resource=res,
                target="[multiple]",
                recursion_depth=0,
                findings_count=sum(1 for f in findings if f.resource == res),
                duration_ms=0,
                error=None
            )
            for res in resources
        ]

        return EnumerationSummary(
            root_domain=root_domain,
            recursive_depth=0,
            started_at=started_at,
            completed_at=completed_at,
            targets_scanned=list(seen_targets),
            findings=sorted_findings,
            resource_executions=resource_executions,
            historical_findings_count=len(findings),
        )

    def _show_resources(self) -> None:
        table = Table(title="Resources", box=box.ROUNDED, header_style="bold cyan")
        table.add_column("Name", style="bold white")
        table.add_column("Auth", style="green")
        for item in self.resource_metadata:
            marker = "-"
            if bool(item["requires_config"]):
                marker = "*"
            elif bool(item.get("has_optional_config", False)):
                marker = "~"
            table.add_row(str(item["name"]), marker)
        self.console.print(table)

    def _load_findings_file(self, root_domain: str, input_path: Path) -> list[Finding]:
        if not input_path.exists() or not input_path.is_file():
            self.console.print(f"[bold yellow]File not found:[/bold yellow] {input_path}")
            return []

        findings: list[Finding] = []
        seen: set[str] = set()
        for line in input_path.read_text(encoding="utf-8").splitlines():
            value = line.strip().lower().lstrip("*.")
            if not value:
                continue
            if value != root_domain and not value.endswith(f".{root_domain}"):
                continue
            if value in seen:
                continue
            seen.add(value)
            findings.append(
                Finding(
                    domain=root_domain,
                    subdomain=value,
                    resource="shell-add",
                    query_target=root_domain,
                    recursion_depth=0,
                )
            )
        return findings
