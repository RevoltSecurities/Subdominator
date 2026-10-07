from __future__ import annotations

import asyncio
import json
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from revoltlogger import LogLevel, Logger

from subdominator.cli.app import _load_domains, build_parser
from subdominator.core.models import EnumerationSummary, Finding, ResourceResult
from subdominator.core.settings import RuntimeSettings
from subdominator.output.writer import OutputWriter
from subdominator.resources.base import BaseResource
from subdominator.resources.providers.github import TokenManager
from subdominator.services.enumerator import EnumerationService
from subdominator.storage.database import Database
from subdominator.storage.repository import EnumerationRepository


def _summary(domain: str, subdomains: list[str]) -> EnumerationSummary:
    now = datetime.now(UTC)
    return EnumerationSummary(
        root_domain=domain,
        recursive_depth=0,
        started_at=now,
        completed_at=now,
        targets_scanned=[domain],
        findings=[Finding(domain, sub, "fake", domain, 0) for sub in subdomains],
        resource_executions=[],
    )


class CancelOnReturnResource(BaseResource):
    name = "cancel-on-return"

    def __init__(self, cancel_event: asyncio.Event) -> None:
        super().__init__(client=None, provider_config=None)  # type: ignore[arg-type]
        self.cancel_event = cancel_event

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        self.cancel_event.set()
        return ResourceResult(self.name, target, recursion_depth, [f"done.{target}"])


class EnumeratorRegressionTests(unittest.TestCase):
    def test_zero_concurrency_is_rejected(self) -> None:  # issue #57
        with self.assertRaises(ValueError):
            EnumerationService(Logger(name="test", level=LogLevel.NONE), concurrency=0)

    def test_cancel_keeps_results_completed_in_same_wait(self) -> None:  # issue #59
        async def scenario() -> EnumerationSummary:
            cancel_event = asyncio.Event()
            service = EnumerationService(
                Logger(name="test", level=LogLevel.NONE), cancel_event=cancel_event
            )
            return await service.enumerate("example.com", [CancelOnReturnResource(cancel_event)])

        summary = asyncio.run(scenario())
        self.assertEqual([f.subdomain for f in summary.findings], ["done.example.com"])


class GithubTokenManagerTests(unittest.TestCase):
    def test_returns_none_when_all_tokens_rate_limited(self) -> None:  # issue #54
        tokens = TokenManager(["a", "b", "c"])
        tokens.current = 7  # cursor already advanced past the pool length
        for key in ("a", "b", "c"):
            tokens.set_exceeded(key, 3600)
        self.assertIsNone(tokens.get())


class CliRegressionTests(unittest.TestCase):
    def test_parser_defaults_come_from_runtime_settings(self) -> None:  # issue #52
        parser = build_parser(RuntimeSettings(timeout=30.0, concurrency=16))
        with patch.object(sys, "argv", ["subdominator"]):
            args = parser.parse_args()
        self.assertEqual(args.timeout, 30.0)
        self.assertEqual(args.concurrency, 16)

    def test_load_domains_lowercases_input(self) -> None:  # issue #56
        args = SimpleNamespace(domain="  Example.COM ", domain_list=None)
        self.assertEqual(asyncio.run(_load_domains(args)), ["example.com"])

    def test_load_domains_lowercases_domain_list(self) -> None:  # issue #56
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "domains.txt"
            path.write_text("Example.COM\n\nTEST.org\n", encoding="utf-8")
            args = SimpleNamespace(domain=None, domain_list=str(path))
            self.assertEqual(asyncio.run(_load_domains(args)), ["example.com", "test.org"])


class OutputWriterRegressionTests(unittest.TestCase):
    def test_multi_domain_output_appends_without_blank_lines(self) -> None:  # issue #50
        writer = OutputWriter()
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "out.txt"

            async def scenario() -> None:
                await writer.write(_summary("a.com", ["x.a.com"]), output=output)
                await writer.write(_summary("empty.com", []), output=output, append=True)
                await writer.write(_summary("b.com", ["y.b.com"]), output=output, append=True)

            asyncio.run(scenario())
            self.assertEqual(output.read_text(encoding="utf-8"), "x.a.com\ny.b.com\n")

    def test_multi_domain_report_json_paths_are_per_domain(self) -> None:  # issue #50
        writer = OutputWriter()
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir) / "report.json"
            for domain in ("a.com", "b.com"):
                path = OutputWriter.resolve_report_path(base, domain, ".json", True)
                asyncio.run(writer.write(_summary(domain, [f"x.{domain}"]), report_json=path))

            for domain in ("a.com", "b.com"):
                data = json.loads((Path(tmpdir) / f"report.{domain}.json").read_text("utf-8"))
                self.assertEqual(data["root_domain"], domain)


class RepositoryRegressionTests(unittest.TestCase):
    def test_empty_scan_creates_no_row_and_empty_rows_can_be_deleted(self) -> None:  # issue #58
        with tempfile.TemporaryDirectory() as tmpdir:
            database = Database(Path(tmpdir) / "legacy.db")
            database.initialize()
            repository = EnumerationRepository(database)

            repository.save_findings("empty.com", [])
            self.assertEqual(repository.list_domains(), [])
            self.assertIsNone(repository.delete_domain("empty.com"))

            # Rows left empty by older versions must still be removable.
            with database.engine.begin() as connection:
                connection.exec_driver_sql(
                    "INSERT INTO subdomains(domain, subdomains) VALUES ('old.com', '')"
                )
            self.assertEqual(repository.delete_domain("old.com"), 0)
            self.assertEqual(repository.list_domains(), [])

            database.engine.dispose()


if __name__ == "__main__":
    unittest.main()
