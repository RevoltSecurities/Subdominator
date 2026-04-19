from __future__ import annotations

import asyncio
import unittest
from datetime import UTC, datetime

from revoltlogger import LogLevel, Logger

from subdominator.cli.app import _merge_with_historical_findings
from subdominator.core.models import ResourceResult
from subdominator.core.models import Finding
from subdominator.resources.base import BaseResource
from subdominator.services.enumerator import EnumerationService


class FakeResource(BaseResource):
    name = "fake"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        if target == "example.com":
            return ResourceResult(self.name, target, recursion_depth, ["a.example.com", "b.example.com"])
        return ResourceResult(self.name, target, recursion_depth, [])


class FailingResource(BaseResource):
    name = "broken"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        raise RuntimeError("boom")


class EnumeratorSummaryTests(unittest.TestCase):
    def test_summary_contains_stats_and_findings(self) -> None:
        service = EnumerationService(Logger(name="test", level=LogLevel.NONE))
        fake = FakeResource(client=None, provider_config=None)  # type: ignore[arg-type]
        broken = FailingResource(client=None, provider_config=None)  # type: ignore[arg-type]

        summary = asyncio.run(service.enumerate("example.com", [fake, broken], recursive_depth=0))

        self.assertEqual(summary.total_unique_findings, 2)
        self.assertEqual(summary.total_resource_executions, 2)
        self.assertEqual(summary.failed_resource_executions, 1)
        self.assertEqual(summary.successful_resource_executions, 1)
        self.assertEqual([finding.subdomain for finding in summary.findings], ["a.example.com", "b.example.com"])
        self.assertEqual(summary.fresh_findings_count, 2)
        self.assertEqual(summary.new_findings_count, 2)

    def test_merge_with_historical_findings_tracks_delta(self) -> None:
        service = EnumerationService(Logger(name="test", level=LogLevel.NONE))
        fake = FakeResource(client=None, provider_config=None)  # type: ignore[arg-type]
        summary = asyncio.run(service.enumerate("example.com", [fake], recursive_depth=0))

        historical = [
            Finding(
                domain="example.com",
                subdomain="b.example.com",
                resource="legacy-db",
                query_target="example.com",
                recursion_depth=0,
                discovered_at=datetime.now(UTC),
            ),
            Finding(
                domain="example.com",
                subdomain="old.example.com",
                resource="legacy-db",
                query_target="example.com",
                recursion_depth=0,
                discovered_at=datetime.now(UTC),
            ),
        ]

        merged = _merge_with_historical_findings(summary, historical)

        self.assertEqual(
            [finding.subdomain for finding in merged.findings],
            ["a.example.com", "b.example.com", "old.example.com"],
        )
        self.assertEqual(merged.fresh_findings_count, 2)
        self.assertEqual(merged.historical_findings_count, 2)
        self.assertEqual(merged.new_findings_count, 1)
        self.assertEqual(merged.reused_historical_findings_count, 1)


if __name__ == "__main__":
    unittest.main()
