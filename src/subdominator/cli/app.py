from __future__ import annotations

import asyncio
import signal
import sys
from pathlib import Path

from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from rich.table import Table
from richparser import RichParser
from revoltlogger import LogLevel, Logger
from revoltutils import FileUtils, Banner, HealthCheck, ConnectionInfo
from gitupdater import GitUpdater

from subdominator.core.constants import APP_NAME,VERSION
from subdominator.core.provider_config import ProviderConfig
from subdominator.core.settings import RuntimeSettings
from subdominator.cli.shell import SubdominatorShell
from subdominator.http.retryable import RetryableHttpClient
from subdominator.output.writer import OutputWriter
from subdominator.resources.registry import ResourceRegistry
from subdominator.services.enumerator import EnumerationService
from subdominator.storage.database import Database
from subdominator.storage.repository import EnumerationRepository





def build_parser() -> RichParser:
    parser = RichParser(description=f"Subdominator: High-performance passive subdomain enumeration engine for effortless asset discovery and rapid reconnaissance")
    parser.add_argument("input", "-d", "--domain", type=str, help="Target domain")
    parser.add_argument("input", "-dL", "--domain-list", type=str, help="File containing domains")
    parser.add_argument("resource", "--all", action="store_true", help="Use all resources")
    parser.add_argument(
        "resource",
        "-ir",
        "--include-resources",
        type=str,
        help="Comma-separated resources to include",
    )
    parser.add_argument(
        "resource",
        "-er",
        "--exclude-resources",
        type=str,
        help="Comma-separated resources to exclude",
    )
    parser.add_argument("resource","-ls", "--list-resources", action="store_true", help="List resources")
    parser.add_argument("resource", "-sh", "--shell", action="store_true", help="Launch interactive shell")
    parser.add_argument("resource", "-dk", "--dork", type=str, help="Custom search dork for supported resources")
    parser.add_argument("runtime", "-t", "--timeout", type=float, default=20.0, help="Request timeout")
    parser.add_argument("runtime", "-rt", "--retries", type=int, default=3, help="Retry count")
    parser.add_argument("runtime", "-rb", "--retry-backoff", type=float, default=1.0, help="Retry backoff")
    parser.add_argument("runtime", "-c", "--concurrency", type=int, default=8, help="Concurrent resource execution")
    parser.add_argument(
        "runtime",
        "-rd",
        "--recursive-depth",
        type=int,
        default=0,
        help="Recursively enumerate newly discovered subdomains",
    )
    parser.add_argument("output", "-o", "--output", type=str, help="Output file path")
    parser.add_argument("output", "-oD", "--output-directory", type=str, help="Output directory")
    parser.add_argument("output", "-j","--json", action="store_true", help="Write JSONL output")
    parser.add_argument("output", "-tb","--table", action="store_true", help="Print subdomains in table format")
    parser.add_argument("output", "-rj","--report-json", type=str, help="Write a JSON summary report")
    parser.add_argument("output", "-ss","--show-summary", action="store_true", help="Print a run summary")
    parser.add_argument("output", "-srs","--show-resource-stats", action="store_true", help="Print per-resource stats")
    parser.add_argument("storage", "-dp","--db-path", type=str, help="Custom database path")
    parser.add_argument("storage", "-sd","--save-db", action="store_true", help="Persist findings to the DB")
    parser.add_argument("storage", "-nd","--no-db", action="store_true", help="Disable DB persistence")
    parser.add_argument("config", "-cp","--config-path", type=str, help="Custom provider config path")
    parser.add_argument("config", "-scp","--show-config-path", action="store_true", help="Show provider config path")
    parser.add_argument("debug", "-v", "--verbose", action="store_true", help="Verbose logging")
    parser.add_argument("debug", "-k", "--insecure", action="store_true", help="Skip SSL certificate verification")
    parser.add_argument("debug", "-p", "--proxy", type=str, help="HTTP proxy")
    parser.add_argument("debug", "-nc", "--no-color", action="store_true", help="Disable colored logs")
    parser.add_argument("update", "-up", "--update", action="store_true", help="Update Subdominator to its latest version")
    parser.add_argument("update", "-release", "--release", action="store_true", help="Show release notes of Subdominator's latest version")
    parser.add_argument("debug", "-hc", "--health-check", action="store_true", help="Check internet connectivity and API status")
    return parser


def _render_resource_markdown(name: str, label: str, url: str, requires_config: bool, has_optional_config: bool = False) -> str:
    if requires_config:
        emphasized = f"{label}*"
    elif has_optional_config:
        emphasized = f"{label} ~"
    else:
        emphasized = label
        
    return f"[***{emphasized}***]({url})" if url else f"***{emphasized}***"


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip().lower() for item in value.split(",") if item.strip()]


async def _load_domains(args) -> list[str]:
    if args.domain:
        return [args.domain.strip()]
    if args.domain_list:
        return [line.strip() for line in await FileUtils.stream(args.domain_list) if line.strip()]
    if FileUtils.is_stdin():
        return [line.strip() for line in sys.stdin if line.strip()]
    return []


def _merge_with_historical_findings(summary, historical_findings):
    if not historical_findings:
        return summary

    merged: dict[str, object] = {finding.subdomain: finding for finding in summary.findings}
    fresh_subdomains = set(merged)
    historical_subdomains = {item.subdomain for item in historical_findings}
    historical_only = 0
    for finding in historical_findings:
        if finding.subdomain not in merged:
            merged[finding.subdomain] = finding
            historical_only += 1

    summary.findings = sorted(merged.values(), key=lambda item: item.subdomain)
    summary.historical_findings_count = len(historical_findings)
    summary.new_findings_count = sum(1 for subdomain in fresh_subdomains if subdomain not in historical_subdomains)
    summary.reused_historical_findings_count = historical_only
    return summary


async def run(cancel_event: asyncio.Event | None = None) -> int:
    gitmanager = GitUpdater("RevoltSecurities/Subdominator", VERSION, "subdominator")
    banner = Banner("Subdominator", "RevoltSecurities")
    banner.render()
    parser = build_parser()
    args = parser.parse_args()
    await gitmanager.versionlog()
    level = LogLevel.DEBUG if args.verbose else LogLevel.INFO
    logger = Logger(level=level, colored=not args.no_color)
    console = Console()

    defaults = RuntimeSettings.defaults()
    settings = RuntimeSettings(
        timeout=args.timeout,
        retries=args.retries,
        retry_backoff=args.retry_backoff,
        concurrency=args.concurrency,
        recursive_depth=args.recursive_depth,
        save_db=args.save_db or not args.no_db,
        proxy=args.proxy,
        config_path=args.config_path or defaults.config_path,
        db_path=args.db_path or defaults.db_path,
        output=args.output,
        output_dir=args.output_directory,
        json_output=args.json,
        table_output=args.table,
        log_level="DEBUG" if args.verbose else "INFO",
        include_resources=_split_csv(args.include_resources),
        exclude_resources=_split_csv(args.exclude_resources),
        all_resources=args.all,
        no_color=args.no_color,
        ssl_verify=not args.insecure,
        update=args.update,
        release=args.release,
        health_check=args.health_check,
    )

    if args.config_path:
        logger.info(f"Loading provider configuration from {args.config_path}")
    else:
        logger.info(f"Loading provider configuration from {defaults.config_path}")

    if settings.health_check:
        info: ConnectionInfo = await HealthCheck.check_connection("google.com", 80)
        logger.info(f"{info.message}")
        return 0

    if settings.update:
        updated = await gitmanager.update()
        if updated:
            logger.info(f"{APP_NAME} updated to the latest version successfully")
            await gitmanager.show_update_log()
            return 0
        else:
            logger.custom("failed", f"{APP_NAME} update failed, please update manually", "CRITICAL")
            return 1

    if settings.release:
        await gitmanager.show_update_log()
        return 0

    if args.show_config_path:
        logger.stdinlog(str(settings.config_path))
        return 0

    provider_config = ProviderConfig(settings.config_path)

    async with RetryableHttpClient(
        logger=logger,
        timeout=settings.timeout,
        retries=settings.retries,
        retry_backoff=settings.retry_backoff,
        proxy=settings.proxy,
        ssl_verify=settings.ssl_verify,
    ) as client:
        registry = ResourceRegistry(client, provider_config, dork=args.dork)
        metadata = registry.all_metadata()
        if args.list_resources:
            logger.info(f"Current Available passive resources: [{len(metadata)}]")
            logger.info("Sources marked with an * needs API key(s) or token(s) configuration to works")
            logger.info("Sources marked with an ~ can optionally use API key(s) or token(s) configuration to improve results")
            logger.info(f"Configure provider keys here: {settings.config_path}")
            for item in metadata:
                console.print(
                    Markdown(
                        _render_resource_markdown(
                            str(item["name"]),
                            str(item["label"]),
                            str(item["url"]),
                            bool(item["requires_config"]),
                            bool(item.get("has_optional_config", False)),
                        )
                    )
                )
            return 0

        if args.shell:
            database = Database(settings.db_path)
            database.initialize()
            repository = EnumerationRepository(database)
            shell = SubdominatorShell(
                console=console,
                repository=repository,
                db_path=settings.db_path,
                config_path=settings.config_path,
                resource_metadata=metadata,
                gitmanager=gitmanager,
            )
            try:
                return await shell.run()
            finally:
                database.engine.dispose()

        await provider_config.load()

        resources = registry.select(
            include=settings.include_resources,
            exclude=settings.exclude_resources,
            include_all=settings.all_resources,
        )
        if not resources:
            logger.error("No resources selected. Use --all or --include-resources.")
            return 1

        domains = await _load_domains(args)
        if not domains:
            logger.error("No input domains provided.")
            return 1

        service = EnumerationService(logger, concurrency=settings.concurrency, cancel_event=cancel_event)
        writer = OutputWriter()
        repository = None
        database = None
        if settings.save_db:
            database = Database(settings.db_path)
            database.initialize()
            repository = EnumerationRepository(database)

        for domain in domains:
            historical_findings = repository.get_saved_findings(domain) if repository is not None else []
            summary = await service.enumerate(
                domain=domain,
                resources=resources,
                recursive_depth=settings.recursive_depth,
            )
            fresh_findings = list(summary.findings)
            summary = _merge_with_historical_findings(summary, historical_findings)
            if settings.json_output:
                for finding in summary.findings:
                    logger.stdinlog(f'{{"domain":"{finding.domain}","subdomain":"{finding.subdomain}","resource":"{finding.resource}"}}')
            elif not settings.table_output:
                for finding in summary.findings:
                    logger.stdinlog(finding.subdomain)
                if not summary.findings:
                    logger.warn(f"No subdomains discovered for {domain}")
            else:
                findings_table = Table(
                    title=f"Subdomains Discovered: {domain}",
                    box=box.ROUNDED,
                    header_style="bold green",
                    title_style="bold white",
                    border_style="green",
                    row_styles=["none", "dim"],
                )
                findings_table.add_column("No.", justify="right", style="bold cyan")
                findings_table.add_column("Subdomain", style="bold white")
                findings_table.add_column("Resource", style="magenta")
                
                for idx, finding in enumerate(summary.findings, start=1):
                    findings_table.add_row(str(idx), finding.subdomain, finding.resource)
                
                if summary.findings:
                    console.print(findings_table)
                else:
                    logger.warn(f"No subdomains discovered for {domain}")
            await writer.write(
                summary,
                output=settings.output,
                output_dir=settings.output_dir,
                json_output=settings.json_output,
                report_json=Path(args.report_json) if args.report_json else None,
            )
            if args.show_summary or args.show_resource_stats or args.verbose:
                _print_summary(console, summary, show_resource_stats=args.show_resource_stats or args.verbose)
            if settings.save_db and repository is not None:
                run_id = repository.save_findings(domain, fresh_findings)
                if run_id is None:
                    logger.success(f"Saved {summary.new_findings_count} new finding(s) for {domain} in legacy DB format")
                else:
                    logger.success(f"Saved {summary.new_findings_count} new finding(s) for {domain} in run {run_id}")

        if database is not None:
            database.engine.dispose()

    return 0


def main() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    cancel_event = asyncio.Event()

    def handle_sigint(*args):
        loop.call_soon_threadsafe(cancel_event.set)

    try:
        loop.add_signal_handler(signal.SIGINT, handle_sigint)
    except NotImplementedError:
        signal.signal(signal.SIGINT, handle_sigint)

    exit_code = 1
    try:
        exit_code = loop.run_until_complete(run(cancel_event=cancel_event))
    except KeyboardInterrupt:
        pass
    finally:
        pending = [task for task in asyncio.all_tasks(loop) if not task.done()]
        for task in pending:
            task.cancel()
        if pending:
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        asyncio.set_event_loop(None)
        loop.close()
    raise SystemExit(exit_code)


def _print_summary(console: Console, summary, *, show_resource_stats: bool) -> None:
    overview = Table(
        title=f"Run Summary: {summary.root_domain}",
        box=box.ROUNDED,
        header_style="bold cyan",
        title_style="bold white",
        border_style="bright_blue",
        row_styles=["none", "dim"],
    )
    overview.add_column("Metric", style="bold white")
    overview.add_column("Value", style="green")
    overview.add_row("Unique Findings", str(summary.total_unique_findings))
    overview.add_row("Fresh Resource Findings", str(summary.fresh_findings_count))
    overview.add_row("Historical Findings", str(summary.historical_findings_count))
    overview.add_row("New Since Past Data", f"[green]{summary.new_findings_count}[/green]")
    overview.add_row("Reused Historical Only", str(summary.reused_historical_findings_count))
    overview.add_row("Targets Scanned", str(len(summary.targets_scanned)))
    overview.add_row("Resource Executions", str(summary.total_resource_executions))
    overview.add_row("Successful Resources", f"[green]{summary.successful_resource_executions}[/green]")
    overview.add_row("Failed Resources", f"[red]{summary.failed_resource_executions}[/red]")
    overview.add_row("Duration", f"{summary.duration_ms} ms")
    console.print(overview)

    if show_resource_stats:
        aggregate: dict[str, dict[str, int]] = {}
        for execution in summary.resource_executions:
            bucket = aggregate.setdefault(
                execution.resource,
                {"runs": 0, "findings": 0, "duration_ms": 0, "failures": 0},
            )
            bucket["runs"] += 1
            bucket["findings"] += execution.findings_count
            bucket["duration_ms"] += execution.duration_ms
            bucket["failures"] += 0 if execution.success else 1

        aggregate_table = Table(
            title=f"Resource Aggregate Stats: {summary.root_domain}",
            box=box.ROUNDED,
            header_style="bold magenta",
            border_style="magenta",
            row_styles=["none", "dim"],
        )
        aggregate_table.add_column("Resource", style="bold white")
        aggregate_table.add_column("Runs", justify="right", style="cyan")
        aggregate_table.add_column("Findings", justify="right", style="green")
        aggregate_table.add_column("Failures", justify="right")
        aggregate_table.add_column("Total Duration", justify="right", style="yellow")
        for resource, bucket in sorted(aggregate.items()):
            failures_text = f"[red]{bucket['failures']}[/red]" if bucket["failures"] else "[green]0[/green]"
            aggregate_table.add_row(
                resource,
                str(bucket["runs"]),
                str(bucket["findings"]),
                failures_text,
                f"{bucket['duration_ms']} ms",
            )
        console.print(aggregate_table)

        resource_table = Table(
            title=f"Resource Execution Detail: {summary.root_domain}",
            box=box.SIMPLE_HEAVY,
            header_style="bold bright_blue",
            border_style="blue",
            row_styles=["none", "dim"],
        )
        resource_table.add_column("Resource", style="bold white")
        resource_table.add_column("Target", style="cyan")
        resource_table.add_column("Depth", justify="right", style="magenta")
        resource_table.add_column("Findings", justify="right", style="green")
        resource_table.add_column("Duration", justify="right", style="yellow")
        resource_table.add_column("Status", style="bold")
        for execution in summary.resource_executions:
            status = Text("ok", style="green") if execution.error is None else Text(execution.error, style="red")
            resource_table.add_row(
                execution.resource,
                execution.target,
                str(execution.recursion_depth),
                str(execution.findings_count),
                f"{execution.duration_ms} ms",
                status,
            )
        console.print(resource_table)
        

if __name__ == "__main__":
    main()
