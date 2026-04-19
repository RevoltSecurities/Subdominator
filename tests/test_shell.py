from __future__ import annotations

import asyncio
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

from rich.console import Console

from subdominator.cli.shell import SubdominatorShell
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

    def test_parse_shell_command_raises_for_invalid_escape(self) -> None:
        with self.assertRaises(ValueError):
            parse_shell_command("help\\")

    def test_shell_run_exits_cleanly_on_eof(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            database = Database(Path(tmpdir) / "test.db")
            database.initialize()
            repository = EnumerationRepository(database)
            shell = SubdominatorShell(
                console=Console(record=True),
                repository=repository,
                db_path=Path(tmpdir) / "test.db",
                config_path=Path(tmpdir) / "provider-config.yaml",
                resource_metadata=[],
            )

            with patch.object(shell.console, "input", side_effect=EOFError):
                exit_code = asyncio.run(shell.run())

            self.assertEqual(exit_code, 0)
            self.assertIn("Exiting shell.", shell.console.export_text())
            database.engine.dispose()

    def test_shell_run_handles_parse_error_and_continues(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            database = Database(Path(tmpdir) / "test.db")
            database.initialize()
            repository = EnumerationRepository(database)
            shell = SubdominatorShell(
                console=Console(record=True),
                repository=repository,
                db_path=Path(tmpdir) / "test.db",
                config_path=Path(tmpdir) / "provider-config.yaml",
                resource_metadata=[],
            )

            with patch.object(shell.console, "input", side_effect=["help\\", "exit"]):
                exit_code = asyncio.run(shell.run())

            self.assertEqual(exit_code, 0)
            self.assertIn("Input parse error:", shell.console.export_text())
            database.engine.dispose()


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

            duplicate = Finding(
                domain="example.com",
                subdomain="a.example.com",
                resource="shell-add",
                query_target="example.com",
                recursion_depth=0,
                discovered_at=datetime.now(UTC),
            )
            new = Finding(
                domain="example.com",
                subdomain="b.example.com",
                resource="shell-add",
                query_target="example.com",
                recursion_depth=0,
                discovered_at=datetime.now(UTC),
            )
            repository.save_findings("example.com", [duplicate, new])
            findings = repository.get_findings("example.com")
            self.assertEqual([item.subdomain for item in findings], ["a.example.com", "b.example.com"])
            self.assertEqual(repository.count_findings("example.com"), 2)

            deleted = repository.delete_domain("example.com")
            self.assertEqual(deleted, 2)
            self.assertEqual(repository.list_domains(), [])

            database.engine.dispose()

    def test_shell_load_findings_file_filters_and_normalizes_text_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            database = Database(Path(tmpdir) / "test.db")
            database.initialize()
            repository = EnumerationRepository(database)
            shell = SubdominatorShell(
                console=Console(record=True),
                repository=repository,
                db_path=Path(tmpdir) / "test.db",
                config_path=Path(tmpdir) / "provider-config.yaml",
                resource_metadata=[],
            )
            input_path = Path(tmpdir) / "subs.txt"
            input_path.write_text(
                "\n".join(
                    [
                        "*.a.example.com",
                        "A.example.com",
                        "b.example.com",
                        "c.other.com",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            findings = shell._load_findings_file("example.com", input_path)
            self.assertEqual([item.subdomain for item in findings], ["a.example.com", "b.example.com"])
            self.assertTrue(all(item.resource == "shell-add" for item in findings))

            database.engine.dispose()


if __name__ == "__main__":
    unittest.main()
