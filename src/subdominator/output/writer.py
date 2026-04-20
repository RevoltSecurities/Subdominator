from __future__ import annotations

import asyncio
import json
from pathlib import Path

import aiofiles
from revoltutils import FolderUtils

from subdominator.core.models import EnumerationSummary, Finding
from subdominator.output.reports import ReportGenerator


class OutputWriter:
    async def write_findings(
        self,
        findings: list[Finding],
        *,
        output: Path | None = None,
        output_dir: Path | None = None,
        json_output: bool = False,
        root_domain: str,
    ) -> None:
        if output_dir is not None:
            await FolderUtils.create_folder(str(output_dir), exist_ok=True)
            suffix = "jsonl" if json_output else "txt"
            output = output_dir / f"{root_domain}.{suffix}"

        if output is None:
            return

        lines = []
        for finding in findings:
            if json_output:
                lines.append(
                    json.dumps(
                        {
                            "domain": finding.domain,
                            "subdomain": finding.subdomain,
                            "resource": finding.resource,
                            "query_target": finding.query_target,
                            "recursion_depth": finding.recursion_depth,
                            "discovered_at": finding.discovered_at.isoformat(),
                        }
                    )
                )
            else:
                lines.append(finding.subdomain)

        async with aiofiles.open(output, "w", encoding="utf-8") as fh:
            await fh.write("\n".join(lines) + "\n")

    async def write(
        self,
        summary: EnumerationSummary,
        *,
        output: Path | None = None,
        output_dir: Path | None = None,
        json_output: bool = False,
        report_json: Path | None = None,
    ) -> None:
        await self.write_findings(
            summary.findings,
            output=output,
            output_dir=output_dir,
            json_output=json_output,
            root_domain=summary.root_domain,
        )

        if output_dir is not None and report_json is None:
            report_json = output_dir / f"{summary.root_domain}.summary.json"

        if report_json is not None:
            await FolderUtils.create_folder(str(report_json.parent), exist_ok=True)
            text = (
                json.dumps(
                    {
                        "root_domain": summary.root_domain,
                        "recursive_depth": summary.recursive_depth,
                        "started_at": summary.started_at.isoformat(),
                        "completed_at": summary.completed_at.isoformat(),
                        "duration_ms": summary.duration_ms,
                        "targets_scanned": summary.targets_scanned,
                        "total_unique_findings": summary.total_unique_findings,
                        "fresh_findings_count": summary.fresh_findings_count,
                        "historical_findings_count": summary.historical_findings_count,
                        "new_findings_count": summary.new_findings_count,
                        "reused_historical_findings_count": summary.reused_historical_findings_count,
                        "total_resource_executions": summary.total_resource_executions,
                        "successful_resource_executions": summary.successful_resource_executions,
                        "failed_resource_executions": summary.failed_resource_executions,
                        "resource_executions": [
                            {
                                "resource": execution.resource,
                                "target": execution.target,
                                "recursion_depth": execution.recursion_depth,
                                "findings_count": execution.findings_count,
                                "duration_ms": execution.duration_ms,
                                "error": execution.error,
                            }
                            for execution in summary.resource_executions
                        ],
                    },
                    indent=2,
                )
                + "\n"
            )
            async with aiofiles.open(report_json, "w", encoding="utf-8") as fh:
                await fh.write(text)

    async def write_html(self, summary: EnumerationSummary, output: Path) -> None:
        """Write an HTML report, offloading synchronous file I/O to a thread."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, ReportGenerator.to_html, output, summary)


    @staticmethod
    def resolve_report_path(
        base: Path,
        root_domain: str,
        suffix: str,
        multi_domain: bool,
    ) -> Path:
        """
        If running against a single domain, return ``base`` as-is.
        If running against multiple domains, insert the domain name before the
        suffix so each domain gets its own file, e.g.::

            report.html  →  report.example.com.html
        """
        if not multi_domain:
            return base
        stem = base.stem
        return base.with_name(f"{stem}.{root_domain}{suffix}")
