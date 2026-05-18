from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from subdominator.core.settings import RuntimeSettings
from subdominator.storage.database import Database
from subdominator.storage.repository import EnumerationRepository


class DatabaseCompatibilityTests(unittest.TestCase):
    def test_defaults_always_use_legacy_cache_db_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            legacy_root = Path(tmpdir)
            legacy_db = legacy_root / "SubdominatorDB" / "subdominator.db"

            with patch("subdominator.core.settings.user_cache_dir", return_value=str(legacy_root)):
                settings = RuntimeSettings.defaults()

            self.assertEqual(settings.db_path, legacy_db)

    def test_initialize_creates_legacy_subdomains_table(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "legacy.db"
            database = Database(db_path)
            database.initialize()

            connection = sqlite3.connect(db_path)
            tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            connection.close()

            self.assertIn("subdomains", tables)
            self.assertTrue(database.uses_legacy_schema())
            database.engine.dispose()

    def test_repository_reads_and_writes_legacy_subdomains_table(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "legacy.db"
            connection = sqlite3.connect(db_path)
            connection.execute("CREATE TABLE subdomains (domain TEXT PRIMARY KEY, subdomains TEXT)")
            connection.execute(
                "INSERT INTO subdomains(domain, subdomains) VALUES (?, ?)",
                ("example.com", "a.example.com,b.example.com"),
            )
            connection.commit()
            connection.close()

            database = Database(db_path)
            database.initialize()
            repository = EnumerationRepository(database)

            self.assertTrue(database.uses_legacy_schema())
            domains = repository.list_domains()
            self.assertEqual(len(domains), 1)
            self.assertEqual(domains[0].root_domain, "example.com")
            self.assertEqual(domains[0].findings_count, 2)
            self.assertIsNone(domains[0].latest_run_id)

            findings = repository.get_findings("example.com")
            self.assertEqual([item.subdomain for item in findings], ["a.example.com", "b.example.com"])
            self.assertTrue(all(item.resource == "legacy-db" for item in findings))

            saved = repository.get_saved_findings("example.com")
            self.assertEqual([item.subdomain for item in saved], ["a.example.com", "b.example.com"])

            self.assertEqual(repository.list_runs("example.com"), [])
            repository.save_findings("example.com", saved)
            self.assertEqual([item.subdomain for item in repository.get_findings("example.com")], ["a.example.com", "b.example.com"])
            deleted = repository.delete_domain("example.com")
            self.assertEqual(deleted, 2)
            self.assertEqual(repository.list_domains(), [])

            database.engine.dispose()


if __name__ == "__main__":
    unittest.main()
