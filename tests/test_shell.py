from __future__ import annotations

import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from subdominator.cli.shell import parse_shell_command
from subdominator.core.models import Finding
from subdominator.storage.database import Database
from subdominator.storage.repository import EnumerationRepository


class ShellCommandTests(unittest.TestCase):
    def test_parse_shell_command_handles_quotes(self) -> None:
        command = parse_shell_command('export example.com "/tmp/out file.json" json')
        assert command is not None
        self.assertEqual(command.name, "export")
        self.assertEqual(command.args, ["example.com", "/tmp/out file.json", "json"])

    def test_parse_shell_command_returns_none_for_blank(self) -> None:
        self.assertIsNone(parse_shell_command("   "))


class RepositoryShellSupportTests(unittest.TestCase):
    def test_repository_domain_queries_and_delete(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            database = Database(Path(tmpdir) / "test.db")
            database.initialize()
            repository = EnumerationRepository(database)

            finding = Finding(
                domain="example.com",
                subdomain="a.example.com",
                resource="crtsh",
                query_target="example.com",
                recursion_depth=0,
                discovered_at=datetime.now(UTC),
            )
            run_id = repository.save_findings("example.com", [finding])

            domains = repository.list_domains()
            self.assertEqual(len(domains), 1)
            self.assertEqual(domains[0].root_domain, "example.com")
            self.assertEqual(domains[0].findings_count, 1)
            self.assertEqual(domains[0].latest_run_id, run_id)

            stats = repository.get_domain_stats("example.com")
            assert stats is not None
            self.assertEqual(stats.findings_count, 1)
            self.assertEqual(stats.unique_resources, 1)
            self.assertIsNone(stats.latest_run_id)

            runs = repository.list_runs("example.com")
            self.assertEqual(runs, [])

            findings = repository.get_findings("example.com")
            self.assertEqual([item.subdomain for item in findings], ["a.example.com"])

            deleted = repository.delete_domain("example.com")
            self.assertEqual(deleted, 1)
            self.assertEqual(repository.list_domains(), [])

            database.engine.dispose()


if __name__ == "__main__":
    unittest.main()
